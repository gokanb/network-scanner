# Walkthrough — network-scanner

How each scanner works, and the bugs fixed during cleanup.

## simple_port_scanner.py

The core is `scan_port`:
```python
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.settimeout(timeout)
    return sock.connect_ex((host, port)) == 0
```
`connect_ex` returns `0` if the connection succeeds (port open) and an error
code otherwise — handy because it doesn't raise on a closed port. A `with` block
makes a **fresh socket per port** and closes it automatically.

> **What was wrong before:** the old script did `socket = socket.socket(...)` once
> (overwriting the module name) and reused that single socket for every port. A
> socket can only be connected once, so every port after the first was scanned
> with a dead socket. Creating a new socket per call fixes it, and a timeout was
> added so closed ports don't hang.

## threaded_port_scanner.py

Resolves the host, prints a reverse-DNS name if there is one, then starts one
thread per port so the scan runs in parallel. Driven by `argparse`:
`-H <host> -p 22,80,443`.

> **What was wrong before:** it read `options.tgtPorts` but the option was defined
> as `tgtPort` (an `AttributeError`), and a reverse-DNS message had `+ tgtIP`
> inside the quotes so it printed the literal text. It was also moved from the
> deprecated `optparse` to `argparse`, with real exception types instead of bare
> `except:`.

## nmap_scanner.py

Prompts for an IP and a port range, validates both with regular expressions,
then scans each port with the `python-nmap` wrapper and prints its state.

> **What was wrong before:** the IP regex used `[0:9]` (a literal colon) instead of
> `[0-9]`, so it rejected every valid address, and the port-range regex had stray
> spaces (`([0-9] +)`) so it never matched `60-120`. Both were corrected, and a
> stray `from os import tcgetpgrp` was removed.

## ping_sweep.py

Reads hosts from `ip_list.txt`, pings each (cross-platform flags), and writes the
results to `reachable.txt` and `unreachable.txt`.

> **What was wrong before:** it called `subprocess.call(f'ping -c 4 {ip}')` with a
> single string and no `shell=True`, which fails; and IPs kept their trailing
> newline. Now the command is passed as a list, IPs are stripped, Windows/Unix
> flags are handled, and a missing `ping` binary is caught instead of crashing.
