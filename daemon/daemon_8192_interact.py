######################################################################
# Script for interacting with port 8192 hosted by the daemon process #
######################################################################

import socket

target_ip = "192.168.10.1"
target_port = 8192
message = "Anyka IPC ,Get IP Address!"

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout for the socket (in seconds) to wait for a response
sock.settimeout(5)

# Send the message to the target IP and port
sock.sendto(message.encode(), (target_ip, target_port))

# Wait for response
try:
    response, addr = sock.recvfrom(1024)
    print(f"Received response from {addr} of length {len(response.decode())}: {response.decode()}")
except socket.timeout:
    print("No response received within the timeout period.")

# Close the socket
sock.close()