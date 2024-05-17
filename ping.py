import subprocess
import platform
import concurrent.futures

def scan_ip(ip):
    if platform.system().lower() == 'windows':
        command = ['ping', '-n', '1', ip]
    else:
        command = ['ping', '-c', '1', ip]
    
    result = subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result == 0

def scan_ip_range(ip_range):
    live_ips = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        ip_addresses = [f"{ip_range}.{i}" for i in range(1, 255)]
        results = executor.map(scan_ip, ip_addresses)
        
    for ip, result in zip(ip_addresses, results):
        if result:
            print(f'{ip} is live')
            live_ips.append(ip)
    
    return live_ips

def scan_ip_range_from_file(file_path):
    live_ips = []
    
    with open(file_path, 'r') as file:
        ip_ranges = [line.strip() for line in file]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(scan_ip_range, ip_ranges)
        
    for result in results:
        live_ips.extend(result)

    return live_ips

file_path = 'ip_ranges.txt'  # 文件中每行为一个IP段，例如：192.168.1
live_ips = scan_ip_range_from_file(file_path)

with open('live_ips.txt', 'w') as file:
    for ip in live_ips:
        file.write(ip + '\n')

print('扫描完成，存活的IP地址已保存在live_ips.txt中。')
