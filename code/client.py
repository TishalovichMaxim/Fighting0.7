import socket, pygame, threading, time
from pygame.constants import *
from chars.character import CharacterSignal, CharacterState, Direction
from chars.char_info import CharInfo
from chars.kirito import Kirito
from imgs_loading import ImgLoader
from chars.ako import Ako
from chars.charater_type import CharacterType
#from game import Game
from networking import ClientGame
from background import BackgroundFactory, BackgroundType

class Client:
    BUF_SIZE = 1024

    def __init__(self, main_server_address, char_type, bg_type, screen) -> None:
        # pygame.mixer.init()
        self.char_type = char_type
        # sound = pygame.mixer.Sound("./music/stage_sonic.mp3")
        # sound.play(loops=-1)
        self.main_server_address = main_server_address
        self.bg_type = bg_type
        self.screen = screen

    # def gen_port(self):
    #     return 50123 + random.randrange(0, 10_000)

    def get_game_server_addr(self):
        # try:
            with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as sock:
                sock.connect(self.main_server_address)
                sock.sendall(bytes([self.char_type.value]))
                data = sock.recv(Client.BUF_SIZE)

                session_server_ip_address = str(data[0]) + '.' + str(data[1]) + '.' + str(data[2]) + '.' + str(data[3])
                session_server_port = data[4]*256 + data[5]
                
                new_client_ip_address = str(data[6]) + '.' + str(data[7]) + '.' + str(data[8]) + '.' + str(data[9])
                new_client_port = data[10]*256 + data[11]

                enemy_char_type = CharacterType(data[12])
                
                return ((session_server_ip_address, session_server_port), (new_client_ip_address, new_client_port), enemy_char_type)
        # except Exception as e:
        #     print(e)
        #     print("Here")
        #     return None   

    def run(self):

        game_server_addr, client_addr, enemy_char_type = self.get_game_server_addr()
        print(f"self: {self.char_type} - enemy ct: {enemy_char_type}")
        # screen = pygame.display.set_mode()
        clock = pygame.time.Clock()

        def getting(sock):
            # try:
                while True:
                    data, addr = sock.recvfrom(1024)
                    data = str(data, encoding='ascii')
                    data = data.split(',')
                    data = map(int, data)
                    rect_x1, rect_y1, image_counter1, state_val1, dir_val1, hp1, rect_x2, rect_y2, image_counter2, state_val2, dir_val2, hp2 = data
                    char_info_1 = CharInfo(rect_x1, rect_y1, image_counter1, CharacterState(state_val1), Direction(dir_val1))
                    char_info_2 = CharInfo(rect_x2, rect_y2, image_counter2, CharacterState(state_val2), Direction(dir_val2))
                    client_game.set_chars(char_info_1, char_info_2)
                    client_game.update()
                    client_game.draw()
                    pygame.display.update()
            # except Exception as e:
                # print(e.with_traceback())


        
        bg = BackgroundFactory.get_background(self.bg_type)
        client_game = ClientGame(self.char_type, enemy_char_type, self.screen, bg)

        with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as sock:
            sock.bind(client_addr)
            # user_input = client_game.get_input()
            # sock.sendto(bytes(user_input), SERVER_ADDRESS)
            thread = threading.Thread(target=getting, args=(sock, ))
            thread.start()
            time.sleep(2)

            while True:
                user_input = client_game.get_input()
                sock.sendto(bytes(user_input), game_server_addr)
                clock.tick(60)

if __name__ == '__main__':
    client = Client(('127.0.0.1', 65532), CharacterType.AKO, BackgroundType.ROAD)
    client.run()