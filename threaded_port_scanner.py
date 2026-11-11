#!/usr/bin/env python3
"""Threaded TCP port scanner with a command-line interface.

Scans several ports at once (one thread per port) for speed.

Usage:
    python threaded_port_scanner.py -H scanme.nmap.org -p 22,80,443
"""

import argparse
import socket
from threading import Thread


def conn_scan(host, port, timeout=1.0):
    """Try to connect to one port and report whether it's open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((host, port))
            print(f"[+] {port}/tcp open")
    except (socket.timeout, ConnectionRefusedError, OSError):
        print(f"[-] {port}/tcp closed")


def port_scan(host, ports):
    """Resolve the host and start a scan thread for each port."""
    try:
        target_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"[-] Unknown host: {host}")
        return

    # Reverse DNS is best-effort; fall back to the IP if there's no PTR record.
    try:
        target_name = socket.gethostbyaddr(target_ip)[0]
        print(f"[+] Scan results for: {target_name} ({target_ip})")
    except socket.herror:
        print(f"[+] Scan results for: {target_ip}")

    for port in ports:
        Thread(target=conn_scan, args=(host, int(port))).start()


def main():
    parser = argparse.ArgumentParser(description="Threaded TCP port scanner")
    parser.add_argument("-H", "--host", required=True, help="target host")
    parser.add_argument("-p", "--ports", required=True,
                        help="comma-separated ports, e.g. 22,80,443")
    args = parser.parse_args()

    ports = [p.strip() for p in args.ports.split(",") if p.strip()]
    port_scan(args.host, ports)


if __name__ == "__main__":
    main()
