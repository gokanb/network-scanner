#!/usr/bin/env python3
"""Ping each host in ip_list.txt and split them into reachable / unreachable.

Writes the results to reachable.txt and unreachable.txt.
"""

import platform
import subprocess


def ping(ip):
    """Return True if the host replies to a ping."""
    count_flag = "-n" if platform.system().lower() == "windows" else "-c"
    # Pass the command as a list (no shell), so arguments are handled safely.
    try:
        result = subprocess.call(
            ["ping", count_flag, "4", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        print("[-] 'ping' command not found on this system.")
        return False
    return result == 0


def main(list_file="ip_list.txt"):
    online, offline = [], []

    with open(list_file, encoding="utf-8") as fh:
        for line in fh:
            ip = line.strip()
            if not ip:
                continue
            (online if ping(ip) else offline).append(ip)

    with open("reachable.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(online) + "\n")
    with open("unreachable.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(offline) + "\n")

    print(f"Reachable: {len(online)}  |  Unreachable: {len(offline)}")


if __name__ == "__main__":
    main()
