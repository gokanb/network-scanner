#!/usr/bin/env python3
"""Simple TCP port scanner.

Scans a range of ports on a single host by trying to open a TCP connection to
each one. A fresh socket is used per port (a socket can only be connected once).
"""

import socket

from termcolor import colored


def scan_port(host, port, timeout=0.5):
    """Return True if the TCP port is open on the host."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        # connect_ex returns 0 on success (port open), an error code otherwise.
        return sock.connect_ex((host, port)) == 0


def main():
    host = input("[+] Enter a host to scan: ").strip()
    start, end = 1, 1000

    print(f"Scanning {host} ports {start}-{end} ...")
    for port in range(start, end + 1):
        if scan_port(host, port):
            print(colored(f"[+] Port {port} is OPEN", "green"))
    print("Done.")


if __name__ == "__main__":
    main()
