import socket, pygame, threading, time, asyncio
from pygame.constants import *
from chars.character import CharacterState, Direction
from chars.char_info import CharInfo
from chars.charater_type import CharacterType
from networking import ClientGame, GameOverException, GameResult
from background import BackgroundFactory, BackgroundType
from constants import *
from imgs_loading import ImgLoader

async def get_game_server_addr(main_server_address, char_type):
    # return "Aboba"
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as sock:
        sock.setblocking(False)
        sock.connect(main_server_address)
        sock.sendall(bytes([char_type.value]))
        data = sock.recv(BUF_SIZE)

        session_server_ip_address = str(data[0]) + '.' + str(data[1]) + '.' + str(data[2]) + '.' + str(data[3])
        session_server_port = data[4]*256 + data[5]
        
        new_client_ip_address = str(data[6]) + '.' + str(data[7]) + '.' + str(data[8]) + '.' + str(data[9])
        new_client_port = data[10]*256 + data[11]

        enemy_char_type = CharacterType(data[12])
        
        return ((session_server_ip_address, session_server_port), (new_client_ip_address, new_client_port), enemy_char_type)
    

class Client:
    waiting_img = ImgLoader.load_image('./images/backgrounds/main.png')

    def __init__(self, main_server_address, char_type, bg_type, screen) -> None:
        self.char_type = char_type
        self.curr_screen_sizes = (pygame.display.Info().current_w, pygame.display.Info().current_h) 
        self.main_server_address = main_server_address
        self.bg_type = bg_type
        self.screen = screen

    def get_game_server_addr(self):
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as sock:
            sock.connect(self.main_server_address)
            sock.sendall(bytes([self.char_type.value]))
            data = sock.recv(BUF_SIZE)

            session_server_ip_address = str(data[0]) + '.' + str(data[1]) + '.' + str(data[2]) + '.' + str(data[3])
            session_server_port = data[4]*256 + data[5]
            
            new_client_ip_address = str(data[6]) + '.' + str(data[7]) + '.' + str(data[8]) + '.' + str(data[9])
            new_client_port = data[10]*256 + data[11]

            enemy_char_type = CharacterType(data[12])
            
            return ((session_server_ip_address, session_server_port), (new_client_ip_address, new_client_port), enemy_char_type)

    def update_waiting_screen(self):
        pygame.event.pump()
        self.screen.blit(Client.waiting_img, (0, 0))
        pygame.display.update()
        
    async def run(self):
        task = asyncio.create_task(
            get_game_server_addr(self.main_server_address, self.char_type)
        )

        SECONDS_LIMIT = 10
        n_seconds = 0
        print("Here")
        while not task.done() and n_seconds < SECONDS_LIMIT:
            print("Point")
            self.update_waiting_screen()
            print("In loop")
            # print(f"delta = {delta} start = {start_time}")
            # print(delta)
            n_seconds += 1
            await asyncio.sleep(1)
            print("Loop end")

        print(f"n seconds = {n_seconds}")
    
        if not task.done():
            task.cancel()
            return GameResult.ERROR
        else:
            print(f"Game server addr = {await task}")
            return GameResult.WIN
            game_server_addr, client_addr, enemy_char_type = await task
        
        print(f"self: {self.char_type} - enemy ct: {enemy_char_type}")
        clock = pygame.time.Clock()

        def getting(sock, event):
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

        bg = BackgroundFactory.get_background(self.bg_type)
        client_game = ClientGame(self.char_type, enemy_char_type, self.screen, bg)

        try:
            with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as sock:
                sock.bind(client_addr)
                event = threading.Event()
                thread = threading.Thread(target=getting, args=(sock, event))
                thread.start()
                time.sleep(2)

                while True:
                    user_input = client_game.get_input()
                    client_game.check_game_end()
                    sock.sendto(bytes(user_input), game_server_addr)
                    clock.tick(60)
        except GameOverException as e:
            event.set()
            return e.game_result

if __name__ == '__main__':
    client = Client(('127.0.0.1', 65532), CharacterType.AKO, BackgroundType.ROAD)
    client.run()