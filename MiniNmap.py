import socket
import errno
import ipaddress
from concurrent.futures import ThreadPoolExecutor


def is_valid_ip(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ValueError:
        return False


def parse_ports(text):
    """Turn '22,80,1000-1010' into a sorted list with no duplicates.
    Returns None if the input is invalid."""
    ports = set()
    try:
        for part in text.split(","):
            part = part.strip()
            if "-" in part:
                start, end = part.split("-")
                start, end = int(start), int(end)
                if not (1 <= start <= end <= 65535):
                    return None
                ports.update(range(start, end + 1))
            else:
                port = int(part)
                if not (1 <= port <= 65535):
                    return None
                ports.add(port)
    except ValueError:
        return None
    return sorted(ports)


def scan_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))

    if result == 0:
        return port, "open"
    if result == errno.ECONNREFUSED:
        return port, "closed"
    return port, "filtered"  # no answer, probably a firewall


def main():
    ip = input("Enter the IP address to scan: ").strip()
    if not is_valid_ip(ip):
        print("Invalid IP address.")
        return

    ports = parse_ports(input("Enter the ports to scan (e.g. 22,80,1000-1010): "))
    if ports is None:
        print("Invalid port numbers.")
        return

    # Scan many ports at the same time
    with ThreadPoolExecutor(max_workers=100) as pool:
        results = list(pool.map(lambda p: scan_port(ip, p), ports))

    open_ports = [p for p, s in results if s == "open"]
    closed_ports = [p for p, s in results if s == "closed"]
    filtered_ports = [p for p, s in results if s == "filtered"]

    for port in open_ports:
        print(f"Port {port} is open on {ip}.")

    print(f"\n--- Scan Summary for {ip} ---")
    print(f"Total ports scanned: {len(ports)}")
    print(f"Open ({len(open_ports)}): {open_ports or 'None'}")
    print(f"Closed ({len(closed_ports)}): {closed_ports or 'None'}")
    print(f"Filtered ({len(filtered_ports)}): {filtered_ports or 'None'}")


if __name__ == "__main__":
    main()