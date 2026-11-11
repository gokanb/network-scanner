# network-scanner

> A small collection of Python network scanning tools — port scanning and host discovery.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Topic](https://img.shields.io/badge/topic-network%20scanning-informational) ![License](https://img.shields.io/badge/License-MIT-lightgrey) ![Status](https://img.shields.io/badge/status-working-success)

## About

Four focused tools for finding live hosts and open ports — the first things you
reach for when mapping a network. They range from a minimal single-threaded
scanner to a faster threaded one and an nmap-powered version.

## Tools

| Script | What it does |
|--------|--------------|
| `simple_port_scanner.py` | Scans ports 1–1000 on one host, one at a time. |
| `threaded_port_scanner.py` | Scans a given list of ports in parallel; has a proper CLI. |
| `nmap_scanner.py` | Scans a port range using nmap for richer results. |
| `ping_sweep.py` | Pings every host in `ip_list.txt`, splits them into reachable / unreachable. |
| `banner_grabber.py` | Reads service banners from open ports to identify software/versions. |

## Getting started

```bash
pip install -r requirements.txt   # termcolor, python-nmap (nmap also needs the nmap program)
```

Examples:
```bash
# Single-host scan (prompts for the host)
python simple_port_scanner.py

# Threaded scan of specific ports
python threaded_port_scanner.py -H scanme.nmap.org -p 22,80,443

# Ping sweep of ip_list.txt
python ping_sweep.py
```

## Skills demonstrated

- TCP connect scanning with sockets (`connect_ex`, timeouts)
- Concurrency with threads for faster scans
- Using the nmap engine from Python
- Cross-platform ping and clean CLI design with `argparse`

## Disclaimer

For **educational purposes only**. Scan only hosts and networks you **own or are
explicitly authorized to test** — unauthorized port scanning can be illegal. The
author assumes **no liability** for misuse. (`scanme.nmap.org` is a host nmap
provides specifically for legal scan practice.)

## License

Released under the [MIT License](LICENSE).
