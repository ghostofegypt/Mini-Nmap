# Mini Nmap (Python)

A simple Nmap-style port scanner written in Python. It performs a TCP connect scan on an IPv4 address and reports which ports are open, closed, or filtered, using only the standard library.


## Features

- Scan single ports, ranges, or both at once 
- Input validation for IP addresses and port numbers
- Fast scanning with a thread pool (100 ports at a time)
- Nmap-style port states:
  - **open**: the connection succeeded
  - **closed**: the connection was refused
  - **filtered**: no answer, usually a firewall dropping packets
- Duplicate ports are removed automatically
- No external dependencies

## Requirements

- Python 3.6 or newer

## Usage

```bash
python nmap_scanner.py
```

The script asks for an IP address and the ports to scan:

```
Enter the IP address to scan: 127.0.0.1
Enter the ports to scan (e.g. 22,80,1000-1010): 22,80,443,8000-8010
```

### Example output

```
Port 80 is open on 127.0.0.1.

--- Scan Summary for 127.0.0.1 ---
Total ports scanned: 14
Open (1): [80]
Closed (13): [22, 443, 8000, 8001, ...]
Filtered (0): None
```

## How it works

Like Nmap's `-sT` mode, the scanner performs a TCP connect scan: it tries to open a normal connection to each port using `socket.connect_ex()`. A result of `0` means the port is open, a "connection refused" error means it is closed, and any other result (such as a timeout) is reported as filtered.
