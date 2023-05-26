import socket, pygame, threading, traceback, time, pygame_widgets
from pygame.constants import *
from src.chars.character import CharacterState, Direction
from src.chars.char_info import CharInfo
from src.chars.character_type import CharacterType
from src.networking.networking import ClientGame, GameOverException, GameResult
from src.utils.background import BackgroundFactory, BackgroundType
from src.constants import *
from src.networking.address import AddressFactory
from src.utils.logger import Logger

class Client:
    def __init__(self, char_type, bg_type, screen, main_server_addr, cm) -> None:
        self.char_type = char_type
        self.curr_screen_sizes = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.bg_type = bg_type
        self.screen = screen
        self.main_server_addr = main_server_addr
        self.logger = Logger("client")
        self.cm = cm

    def _get_session_info(self):
        def getting_info(self, event):
            try:
                with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as sock:
                    # sock.settimeout(TIME_OUT)
                    sock.settimeout(5)
                    sock.connect(self.main_server_addr.get_addr())
                    self.logger.log("connected to main server")
                    sock.sendall(bytes([self.char_type.value]))
                    data = sock.recv(BUF_SIZE)
                    sock.sendall(data)

                    data = sock.recv(BUF_SIZE)

                    session_server_addr = AddressFactory.create_by_bytes(data[:6])
                    new_client_addr = AddressFactory.create_by_bytes(data[6:12])
                    enemy_char_type = CharacterType(data[12])

                    self.temp_server_info = (session_server_addr, new_client_addr, enemy_char_type)
            except:
                self.temp_server_info = None    

            event.set()

        event = threading.Event()        
        info_thread = threading.Thread(target=getting_info, args=(self, event))
        info_thread.start()

        FPS = 60
        clock = pygame.time.Clock()
        print("I'm in drawing thread")    
        
        while not event.is_set():
            print("I'm in drawing loop...")
            self.cm.draw()
            events = pygame.event.get()
            # pygame.event.pump()#maybe i can to remove it at all
            for _ in pygame.event.get():
                pass
            pygame_widgets.update(events)
            pygame.display.update()
            clock.tick(FPS)

        return self.temp_server_info
       
    def get_game_result(self, game_server_addr):
        TIME_OUT = 5
        try:
            with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as sock:
                sock.bind(self.client_addr.get_addr())
                sock.settimeout(TIME_OUT)
                sock.connect(game_server_addr.get_addr())
                data = sock.recv(BUF_SIZE)
                try:
                    game_result = GameResult(data[0])
                    return game_result
                except:
                    print("Converting to game result error!")
        except TimeoutError as e:
            print("Time out error occurs")

        return GameResult.ERROR

    def run(self):
        def getting(sock, event):
            try:
                while not event.is_set():
                    try:
                        data, addr = sock.recvfrom(1024)
                        data = str(data, encoding='ascii')
                        data = data.split(',')
                        data = map(int, data)
                        rect_x1, rect_y1, image_counter1, state_val1, dir_val1, hp1, rect_x2, rect_y2, image_counter2, state_val2, dir_val2, hp2 = data
                        char_info_1 = CharInfo(rect_x1, rect_y1, image_counter1, CharacterState(state_val1), Direction(dir_val1), hp1)
                        char_info_2 = CharInfo(rect_x2, rect_y2, image_counter2, CharacterState(state_val2), Direction(dir_val2), hp2)
                        client_game.set_chars(char_info_1, char_info_2)
                        client_game.update()
                        client_game.draw()
                        pygame.display.update()
                    except ConnectionResetError:
                        self.logger.log("Connection reset error occurs")
                        break
            except:
                traceback.print_exc()
                #event.set()
            event.set()
            
        temp_server_info = self._get_session_info()
        if not temp_server_info:
            return GameResult.SESSION_BREAK

        game_server_addr, client_addr, enemy_char_type = temp_server_info
        self.client_addr = client_addr

        print(f"self: {self.char_type} - enemy ct: {enemy_char_type}")
        clock = pygame.time.Clock()

        bg = BackgroundFactory.get_background(self.bg_type)
        client_game = ClientGame(self.char_type, enemy_char_type, self.screen, bg)

        try:
            with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as sock:
                sock.bind(client_addr.get_addr())
                sock.settimeout(3)
                event = threading.Event()
                getting_thread = threading.Thread(target=getting, args=(sock, event))
                time.sleep(1.5)
                getting_thread.start()
                self.logger.log("Game starts run")

                while not event.is_set():
                    user_input = client_game.get_input()
                    # client_game.check_game_end()
                    sock.sendto(bytes(user_input), game_server_addr.get_addr())
                    clock.tick(60)

        #i want to catch TimeOutExceptino and GameOver exception but get: TypeError: catching classes that do not inherit from BaseException is not allowed
        except Exception as e:
            self.logger.log("exception getting in game")
            traceback.print_exc()
            event.set()
            getting_thread.join()

        return self.get_game_result(game_server_addr)

if __name__ == '__main__':
    client = Client(('127.0.0.1', 65532), CharacterType.AKO, BackgroundType.ROAD)
    client.run()