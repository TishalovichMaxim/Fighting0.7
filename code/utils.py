def get_bytes_from_addr(addr):
    ip_address = addr[0]
    port = addr[1]
    ip_address_bytes = map(int, ip_address.split('.'))
    return bytes(ip_address_bytes) + int.to_bytes(port, 2)

def get_addr_from_bytes(addr_bytes):
    ip_address = str(addr_bytes[0]) + '.' + str(addr_bytes[1]) + '.' + str(addr_bytes[2]) + '.' + str(addr_bytes[3])
    port = addr_bytes[4]*256 + addr_bytes[5]
    return (ip_address, port)

def get_addr_from_str(addr_str):
    ip_address, port = addr_str.split(' ')
    return (ip_address, int(port))

def get_str_from_addr(addr):
    return addr[0] + ' ' + str(addr[1])

if __name__ == '__main__':
    # val = b'\x7f\x00\x00\x01\xff\x98'
    # print(get_bytes_from_addr(('127.0.0.1', 65432)))
    # print(get_addr_from_bytes(val))
    print(get_str_from_addr(('127.0.0.1', 65432)))