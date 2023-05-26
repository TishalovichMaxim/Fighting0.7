import sys
sys.path.append(sys.path[0] + "\\..\\..\\..")
# print(sys.path)
import socket, multiprocessing, traceback
from session_server import start_session_server
from src.chars.character_type import CharacterType
from src.networking.operation_result import OperationResult
from src.constants import BUF_SIZE
from src.networking.address import AddressFactory
from src.utils.logger import Logger

class MainServer:
    def __init__(self, host, port, start_game_server_port) -> None:
        self.addr = (host, port)
        self.game_server_addr = (host, start_game_server_port)
        self.logger = Logger("Main")

    def run(self):
        def close_connections(conn1, conn2):
            def close_connection(conn):
                try:
                    conn.close()
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
                    self.logger.log(f"First connected = {addr1}")
                    conn2, addr2 = s.accept()
                    self.logger.log(f"Second connected = {addr2}")

                    addr1 = AddressFactory.create_by_addr(addr1)
                    addr2 = AddressFactory.create_by_addr(addr2)
                    game_server_addr = AddressFactory.create_by_addr(self.game_server_addr)

                    char_type_value_1_bytes = conn1.recv(BUF_SIZE)
                    char_type_value_1 = char_type_value_1_bytes[0]
                    self.logger.log(f"getting chv1 = {char_type_value_1}")

                    char_type_value_2_bytes = conn2.recv(BUF_SIZE)
                    char_type_value_2 = char_type_value_2_bytes[0]
                    self.logger.log(f"getting chv2 = {char_type_value_2}")

                    conn1.sendall(bytes("test", encoding='ascii'))
                    conn2.sendall(bytes("test", encoding='ascii'))

                    conn1.settimeout(1)
                    conn2.settimeout(1)
                    conn1.recv(BUF_SIZE)
                    conn2.recv(BUF_SIZE)

                    conn1.sendall(bytes(game_server_addr) + bytes(addr1) + char_type_value_2_bytes)
                    self.logger.log("sent game info to 1")
                    conn2.sendall(bytes(game_server_addr) + bytes(addr2) + char_type_value_1_bytes)
                    self.logger.log("sent game info to 2")

                    start_game_server(game_server_addr, addr1, char_type_value_1, addr2, char_type_value_2)
                    self.logger.log("started game server")
                    # conn1.sendall(bytes((OperationResult.GAME_PREPARED.value, )))
                    # conn2.sendall(bytes((OperationResult.GAME_PREPARED.value, )))

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