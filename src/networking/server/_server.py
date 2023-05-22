import pygame, threading, socket, traceback, time
from src.chars.character import SignalsSender, CharacterSignal
from src.chars.character_type import CharacterType
from src.networking.networking import ServerGame
from src.utils.utils import get_addr_from_str
from src.constants import *

class SessionServer:
    def __init__(self, server_addr, client1_addr, char_type_1, client2_addr, char_type_2) -> None:
        self.addr = server_addr
        self.addr_1 = client1_addr      
        self.addr_2 = client2_addr
        self.char_type_1 = char_type_1
        self.char_type_2 = char_type_2

        pygame.init()
        pygame.display.set_mode()

        self.game = ServerGame(CharacterType(self.char_type_1), CharacterType(self.char_type_2))

    def _show_game_result(self):
        TIME_OUT = 10
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(self.addr.get_addr())
                s.settimeout(TIME_OUT)
                s.listen(5)
                game_result = self.game.get_result()
                n_connection = 0

                while True:
                    conn, addr = s.accept()
                    n_connection += 1
                    with conn:
                        if addr == self.addr_1.get_addr():
                            conn.send(bytes([game_result[0].value]))
                        else:
                            conn.send(bytes([game_result[1].value]))

                    if n_connection == 2:
                        return
                    
        except TimeoutError as e:
            print("Time out of showing result")

    def run(self):
        def send_data(sock, event):
            clock = pygame.time.Clock()
            while not event.is_set():
                sock.sendto(self.game.get_chars_info(), self.addr_1.get_addr())
                sock.sendto(self.game.get_chars_info(True), self.addr_2.get_addr())
                self.game.update()
                clock.tick(FPS)

        TIME_OUT = 40
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as sock:
            sock.bind(self.addr.get_addr())
            time.sleep(9)
            print(self.addr.get_addr())
            # sock.settimeout(TIME_OUT)
            event = threading.Event()
            sending_thread = threading.Thread(target=send_data, args=(sock, event))
            sending_thread.start()

            sig_sender = SignalsSender()

            while not self.game.is_ended():
                try:
                    pygame.event.pump()
                    data, addr = sock.recvfrom(1024)
                    if addr == self.addr_1.get_addr():
                        self.game.char1.set_movs(data[0], data[1])
                        for i in range(2, len(data)):
                            sig_sender.send_sig(self.game.char1, CharacterSignal(data[i]))
                    else:
                        self.game.char2.set_movs(data[0], data[1])
                        for i in range(2, len(data)):
                            sig_sender.send_sig(self.game.char2, CharacterSignal(data[i]))
                except Exception as e:
                    traceback.print_exc()
                    break

            event.set()
            sending_thread.join()

        self._show_game_result()

def start_session_server(server_addr, client1_addr, char_type_1, client2_addr, char_type_2):
    session_server = SessionServer(server_addr, client1_addr, char_type_1, client2_addr, char_type_2)
    session_server.run()

    # SERVER_ADDRESS   = get_addr_from_str(server_addr_str)
    # CLIENT_ADDRESS_1 = get_addr_from_str(client1_addr_str)
    # CLIENT_ADDRESS_2 = get_addr_from_str(client2_addr_str)
    # print(SERVER_ADDRESS, CLIENT_ADDRESS_1, CLIENT_ADDRESS_2)
    # print(f"chtv1 = {char_type_value_1} chtv2 = {char_type_value_2}")

    # FPS = 60
    # N_LAST_PACKETS = 500

    # pygame.init()
    # pygame.display.set_mode()

    # game = ServerGame(CharacterType(char_type_value_1[0]), CharacterType(char_type_value_2[0]))
    # game.char1.set_start_pos()
    # game.char2.set_start_pos(False)

    # def send_data(sock, event):
    #     clock = pygame.time.Clock()
    #     while not event.is_set():
    #         sock.sendto(game.get_chars_info(), CLIENT_ADDRESS_1)
    #         sock.sendto(game.get_chars_info(True), CLIENT_ADDRESS_2)
    #         game.update()
    #         clock.tick(FPS)

    # with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as sock:
    #     sock.bind(SERVER_ADDRESS)

    #     connected = [False, False]
    #     while (not connected[0]) or (not connected[1]):
    #         data, addr = sock.recvfrom(1024)
    #         if addr == CLIENT_ADDRESS_1:
    #             connected[0] = True
    #         else:
    #             connected[1] = True
    #         print(connected)
    #         print(not connected[0])
    #         print(not connected[1])
        
    #     event = threading.Event()
    #     sending_thread = threading.Thread(target=send_data, args=(sock, event))
    #     sending_thread.start()
    #     sig_sender = SignalsSender()
    #     while not game.is_ended():
    #         try:
    #             pygame.event.pump()
    #             data, addr = sock.recvfrom(1024)
    #             if addr == CLIENT_ADDRESS_1:
    #                 game.char1.set_movs(data[0], data[1])
    #                 for i in range(2, len(data)):
    #                     sig_sender.send_sig(game.char1, CharacterSignal(data[i]))
    #             else:
    #                 game.char2.set_movs(data[0], data[1])
    #                 for i in range(2, len(data)):
    #                     sig_sender.send_sig(game.char2, CharacterSignal(data[i]))
    #         except Exception as e:
    #             print(e)
    #             event.set()
    #             sending_thread.join()

    # sock.settimeout(15)
    # if game.char1.hp > 0: