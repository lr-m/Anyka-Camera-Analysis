###############################################################
# Script for using the 'ap_bind' operator to allow the camera #
# to connect to an access point via port 6000 hosted by       #
# anyka_ipc process (libcloudapi.so)                          #
###############################################################

import json
import base64
import socket
from pwn import hexdump

ssid = b'hello'
password = b'world'
bind_key = 'CN'
xor_key = b'89JFSjo8HUbhou5776NJOMp9i90ghg7Y78G78t68899y79HY7g7y87y9ED45Ew30O0jkkl'

# XOR function
def xor_encode(input_bytes, key):
    encoded_bytes = bytearray(len(input_bytes))
    key_length = len(key)

    for i in range(len(input_bytes)):
        encoded_byte = input_bytes[i] ^ key[i % key_length]
        encoded_bytes[i] = encoded_byte

    return encoded_bytes

# Create the JSON structure
json_data = {
    "operator": "ap_bind",
    "data": f"b={bind_key}&s={base64.b64encode(ssid).decode()}&p={base64.b64encode(xor_encode(password, xor_key)).decode()}"
}

# Convert JSON to string
json_string = json.dumps(json_data)

print(json_string)

# IP address and port of the server
server_ip = "192.168.10.1"
server_port = 6000

# Create a socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Send the JSON data to the server
client_socket.sendall(json_string.encode())

# Receive and print the response
response = client_socket.recv(1024).decode()
print("Response from server:", response)

# Close the socket
client_socket.close()
