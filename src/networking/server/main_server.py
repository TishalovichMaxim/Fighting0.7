import sys
sys.path.append(sys.path[0] + "\\..\\..\\..")
# print(sys.path)

import socket, multiprocessing, traceback
from _server import start_session_server
from src.chars.character_type import CharacterType
from src.networking.operation_result import OperationResult
from src.constants import BUF_SIZE
from src.networking.address import AddressFactory

class MainServer:
    def __init__(self, host, port, start_game_server_port) -> None:
        self.addr = (host, port)
        self.game_server_addr = (host, start_game_server_port)

    def run(self):
        def close_connections(conn1, conn2):
            def close_connection(conn):
                try:
                    conn.close
                except Exception as e:
                    print(e)

            close_connection(conn1)
            close_connection(conn2)

        def start_game_server(server_addr, addr1, char_type_value_1, addr2, char_type_value_2):
            p = multiprocessing.Process(target=start_session_server,
                        args=(server_addr, addr1, CharacterType(char_type_value_1), addr2, CharacterType(char_type_value_2)))
            p.start()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.addr)
            s.listen(2)
            
            while True:
                try:
                    conn1, addr1 = s.accept()
                    print("First connected")
                    conn2, addr2 = s.accept()
                    print("Second connected")

                    addr1 = AddressFactory.create_by_addr(addr1)
                    addr2 = AddressFactory.create_by_addr(addr2)
                    game_server_addr = AddressFactory.create_by_addr(self.game_server_addr)

                    char_type_value_1_bytes = conn1.recv(BUF_SIZE)
                    char_type_value_1 = char_type_value_1_bytes[0]
                    print("chv1 = ", char_type_value_1)
                    
                    char_type_value_2_bytes = conn2.recv(BUF_SIZE)
                    char_type_value_2 = char_type_value_2_bytes[0]
                    print("chv2 = ", char_type_value_2)

                    conn1.sendall(bytes(game_server_addr) + bytes(addr1) + char_type_value_2_bytes)
                    conn2.sendall(bytes(game_server_addr) + bytes(addr2) + char_type_value_1_bytes)
                    
                    start_game_server(game_server_addr, addr1, char_type_value_1, addr2, char_type_value_2)
                    
                    conn1.sendall(bytes((OperationResult.GAME_PREPARED.value, )))
                    conn2.sendall(bytes((OperationResult.GAME_PREPARED.value, )))

                except Exception as e:
                    traceback.print_exc()

                finally:
                    close_connections(conn1, conn2)

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 65532

    GAME_SERVER_PORT = 61288

    main_server = MainServer(HOST, PORT, GAME_SERVER_PORT)
    main_server.run()

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.bind((HOST, PORT))
    #     s.listen(2)
        
    #     while True:
    #         try:
    #             conn1, addr1 = s.accept()
    #             conn2, addr2 = s.accept()
    #             with conn1, conn2:
    #                 addr1 = AddressFactory.create_by_addr(addr1)
    #                 addr2 = AddressFactory.create_by_addr(addr2)

    #                 char_type_value_1 = conn1.recv(BUF_SIZE)
    #                 print("chv1 = ", char_type_value_1)
                    
    #                 char_type_value_2 = conn2.recv(BUF_SIZE)
    #                 print("chv2 = ", char_type_value_2)

    #                 server_addr_str = get_str_from_addr(GAME_SERVER_ADDR)
    #                 print(server_addr_str)
    #                 print(addr1)
    #                 print(addr2)

    #                 conn1.sendall(get_bytes_from_addr(GAME_SERVER_ADDR) + get_bytes_from_addr(addr1) + char_type_value_2)
    #                 conn2.sendall(get_bytes_from_addr(GAME_SERVER_ADDR) + get_bytes_from_addr(addr2) + char_type_value_1)
                    
    #                 p = multiprocessing.Process(target=aboba,
    #                             args=(server_addr_str, client1_addr_str, char_type_value_1, client2_addr_str, char_type_value_2))
    #                 p.start()

    #                 conn1.sendall(bytes((OperationResult.GAME_PREPARED.value, )))
    #                 conn2.sendall(bytes((OperationResult.GAME_PREPARED.value, )))

    #                 GAME_SERVER_ADDR = (GAME_SERVER_ADDR[0], GAME_SERVER_ADDR[1] + 1)
    #         except:
    #             print("session skip")