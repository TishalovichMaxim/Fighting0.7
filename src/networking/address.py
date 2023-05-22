class AddressFactory:
    class Address:
        def __init__(self, host, port) -> None:
            self.host = host
            self.port = port

        def get_addr(self):
            return (self.host, self.port)

        def __str__(self) -> str:
            return self.host + ' ' + str(self.port)

        def __bytes__(self):
            ip_address_bytes = map(int, self.host.split('.'))
            return bytes(ip_address_bytes) + int.to_bytes(self.port, 2)

    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port

    @classmethod
    def create_by_addr(cls, addr):
        return cls.Address(addr[0], addr[1])
    
    @classmethod
    def create_by_bytes(cls, addr_bytes):
        ip_address = str(addr_bytes[0]) + '.' + str(addr_bytes[1]) + '.' + str(addr_bytes[2]) + '.' + str(addr_bytes[3])
        port = addr_bytes[4]*256 + addr_bytes[5]
        return cls.Address(ip_address, port)
    
    @classmethod
    def create_by_str(cls, addr_str):
        ip_address, port_str = addr_str.split(' ')
        port = int(port_str)
        return cls.Address(ip_address, port)
