#!/usr/bin/env python3
"""Banner grabber.

Connects to each open port on a host and reads the first bytes the service
sends back (its "banner"). Banners often reveal the software and version
running on a port, which is a basic reconnaissance step.
"""

import socket


def grab_banner(ip, port, timeout=2):
    """Return the banner bytes from a port, or None if nothing is read."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((ip, port))
            return sock.recv(1024)
    except OSError:
        return None


def main():
    ip = input("Enter target IP: ").strip()
    start, end = 20, 1000
    print(f"Grabbing banners on {ip} ports {start}-{end} ...")

    for port in range(start, end + 1):
        banner = grab_banner(ip, port)
        if banner:
            text = banner.decode(errors="ignore").strip()
            print(f"[+] {ip}:{port} -> {text}")
    print("Done.")


if __name__ == "__main__":
    main()
