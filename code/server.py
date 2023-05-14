import socket
from utils import get_str_from_addr, get_bytes_from_addr
import multiprocessing
from _server import aboba
from constants import *

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 65532

    GAME_SERVER_ADDR = ('127.0.0.1', 61288)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(2)
        
        while True:
            conn1, addr1 = s.accept()
            conn2, addr2 = s.accept()
            with conn1, conn2:
                client1_addr_str = get_str_from_addr(addr1)
                client2_addr_str = get_str_from_addr(addr2)

                char_type_value_1 = conn1.recv(BUF_SIZE)
                print("chv1 = ", char_type_value_1)
                
                char_type_value_2 = conn2.recv(BUF_SIZE)
                print("chv2 = ", char_type_value_2)

                server_addr_str = get_str_from_addr(GAME_SERVER_ADDR)
                
                print(server_addr_str)
                print(client1_addr_str)
                print(client2_addr_str)
                p = multiprocessing.Process(target=aboba,
                                        args=(server_addr_str, client1_addr_str, char_type_value_1, client2_addr_str, char_type_value_2))
                p.start()
                conn1.send(get_bytes_from_addr(GAME_SERVER_ADDR) + get_bytes_from_addr(addr1) + char_type_value_2)
                conn2.send(get_bytes_from_addr(GAME_SERVER_ADDR) + get_bytes_from_addr(addr2) + char_type_value_1)
                GAME_SERVER_ADDR = (GAME_SERVER_ADDR[0], GAME_SERVER_ADDR[1] + 1)