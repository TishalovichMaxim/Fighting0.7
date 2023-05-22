import socket, pygame, threading, traceback
from pygame.constants import *
from src.chars.character import CharacterState, Direction
from src.chars.char_info import CharInfo
from src.chars.character_type import CharacterType
from src.networking.networking import ClientGame, GameOverException, GameResult
from src.utils.background import BackgroundFactory, BackgroundType
from src.constants import *

class Client:
    def __init__(self, char_type, bg_type, screen) -> None:
        self.char_type = char_type
        self.curr_screen_sizes = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.bg_type = bg_type
        self.screen = screen

    def get_game_result(self, game_server_addr):
        TIME_OUT = 5
        try:
            with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as sock:
                sock.settimeout(TIME_OUT)
                sock.connect(game_server_addr)
                data = sock.recv(BUF_SIZE)
                try:
                    game_result = GameResult(data[0])
                    return game_result
                except:
                    print("Converting to game result error!")
        except TimeoutError as e:
            print("Time out error occurs")

        return GameResult.ERROR

    def run(self, temp_server_info):
        def getting(sock, event):
            try:
                while not event.is_set():
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
            except:
                event.set()

        game_server_addr, client_addr, enemy_char_type = temp_server_info

        print(f"self: {self.char_type} - enemy ct: {enemy_char_type}")
        clock = pygame.time.Clock()

        bg = BackgroundFactory.get_background(self.bg_type)
        client_game = ClientGame(self.char_type, enemy_char_type, self.screen, bg)

        try:
            with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as sock:
                sock.bind(client_addr)
                sock.settimeout(2.5)
                event = threading.Event()
                getting_thread = threading.Thread(target=getting, args=(sock, event))
                getting_thread.start()

                while not event.is_set():
                    user_input = client_game.get_input()
                    client_game.check_game_end()
                    sock.sendto(bytes(user_input), game_server_addr)
                    clock.tick(60)

        except GameOverException|TimeoutError as e:
            traceback.print_exc()
            event.set()
            getting_thread.join()

        return self.get_game_result(game_server_addr)

if __name__ == '__main__':
    client = Client(('127.0.0.1', 65532), CharacterType.AKO, BackgroundType.ROAD)
    client.run()