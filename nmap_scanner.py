#!/usr/bin/env python3
"""Interactive port scanner built on the python-nmap wrapper.

Prompts for an IP address and a port range, then scans each port with nmap and
reports its state. Requires the `nmap` program and the `python-nmap` package.
"""

import re

import nmap

# ^(\d{1,3}\.){3}\d{1,3}$  — four dot-separated groups of 1-3 digits.
IP_PATTERN = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
# Match "<int>-<int>", ignoring surrounding spaces.
PORT_RANGE_PATTERN = re.compile(r"^([0-9]+)-([0-9]+)$")


def prompt_ip():
    while True:
        ip = input("\nEnter the IP address to scan: ").strip()
        if IP_PATTERN.match(ip):
            return ip
        print("  That is not a valid IPv4 address, try again.")


def prompt_port_range():
    while True:
        raw = input("Enter port range (e.g. 60-120): ").replace(" ", "")
        match = PORT_RANGE_PATTERN.match(raw)
        if match:
            return int(match.group(1)), int(match.group(2))
        print("  Please use the format <int>-<int>.")


def main():
    ip = prompt_ip()
    port_min, port_max = prompt_port_range()

    scanner = nmap.PortScanner()
    for port in range(port_min, port_max + 1):
        try:
            result = scanner.scan(ip, str(port))
            state = result["scan"][ip]["tcp"][port]["state"]
            print(f"Port {port} is {state}")
        except Exception:
            print(f"Could not scan port {port}")


if __name__ == "__main__":
    main()
