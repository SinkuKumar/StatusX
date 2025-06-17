import socket
import psutil


def get_system_info():
    hostname = socket.gethostname()
    ram = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)  # Use interval=1 for accurate measurement
    net = psutil.net_io_counters()

    # Get disk usage for all drives
    disk_info = {}
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            disk_info[part.device] = {
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent
            }
        except PermissionError:
            continue

    return {
        "hostname": hostname,
        "total_ram": ram.total,
        "used_ram": ram.used,
        "free_ram": ram.available,
        "ram_percent": ram.percent,
        "cpu_percent": cpu,
        "bytes_sent": net.bytes_sent,
        "bytes_recv": net.bytes_recv,
        "disks": disk_info
    }


def format_bytes(size):
    power = 2 ** 10
    n = 0
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    while size >= power and n < len(units) - 1:
        size /= power
        n += 1
    return f"{size:.2f} {units[n]}"


if __name__ == "__main__":
    info = get_system_info()
    print(f"Hostname: {info['hostname']}")
    for key, value in info.items():
        if key in ["ram_percent", "cpu_percent"]:
            print(f"{key}: {value}%")
        elif "ram" in key or "bytes" in key:
            print(f"{key}: {format_bytes(value)}")
    for disk, usage in info["disks"].items():
        print(f"Disk {disk}: Total: {format_bytes(usage['total'])}, "
              f"Used: {format_bytes(usage['used'])}, "
              f"Free: {format_bytes(usage['free'])}, "
              f"Percent: {usage['percent']}%")
