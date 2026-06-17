import requests
from scapy.all import ARP, Ether, srp

def local_network_scan(ip_range):
    # Thụt lề khối lệnh xử lý tạo và gửi gói tin ARP
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        # Thụt lề bên trong vòng lặp for để thêm thiết bị quét được vào danh sách
        devices.append({
            'ip': received.psrc,
            'mac': received.hwsrc,
            'vendor': get_vendor_by_mac(received.hwsrc)
        })

    return devices

def get_vendor_by_mac(mac):
    try:
        # Thụt lề khối kiểm tra API MacVendors
        response = requests.get(f"https://api.macvendors.com/{mac}")
        if response.status_code == 200:
            return response.text
        else:
            return "Unknown"
    except Exception as e:
        print("Error fetching vendor information:", e)
        return "Unknown"

def main():
    # Thụt lề hàm main điều khiển chính
    ip_range = "192.168.88.1/24"  # Bạn có thể sửa dải IP này cho đúng với phòng máy nếu cần
    devices = local_network_scan(ip_range)

    print("Devices on the local network:")
    for device in devices:
        print(f"IP: {device['ip']}, MAC: {device['mac']}, Vendor: {device['vendor']}")

if __name__ == '__main__':
    main()