import sys
sys.path.append(sys.path[0] + "\\..\\..")

from enum import Enum, auto
from pygame_widgets.button import Button
from collections import deque
import pygame, pygame_widgets, socket, threading, time
from src.utils.imgs_loading import ImgLoader
from src.chars.character_type import CharacterType
from src.utils.background import BackgroundType
from src.constants import *
from src.networking.operation_result import OperationResult
from src.networking.client.client import Client

class ClientState(Enum):
    MAIN_MENU = auto()
    CHAR_CHOOSE = auto()
    MAP_CHOOSE = auto()
    WAITING_GAME = auto()
    WIN = auto()
    LOSE = auto()
    EXIT = auto()

class ClientMachine():
    MAIN_SERVER_ADDR = ('127.0.0.1', 65532)

    def __init__(self) -> None:
        # self.screen = pygame.display.init()
        pygame.init()
        self.screen = pygame.display.set_mode()
        self.signals = deque()
        self.widgets = self._init_widgets()
        self.bg_image = ImgLoader.load_image("images/backgrounds/main.png")

        main_menu_btns = set((self.btn_start_game, self.btn_settings, self.btn_exit))
        char_choose_btns = set((self.btn_to_menu, self.btn_to_map, self.btn_ako, self.btn_kirito))
        map_choose_btns = set((self.btn_to_choose_char, self.btn_to_game, self.btn_dojo, self.btn_road, self.btn_temple))

        self.handlers = {
            ClientState.MAIN_MENU: self._main_menu_handler,
            ClientState.CHAR_CHOOSE: self._char_choose_handler,
            ClientState.MAP_CHOOSE: self._map_choose_handler,
            ClientState.WIN: self._win_handler,
            ClientState.LOSE: self._lose_handler
        }

        self.scene_widgets = {
            ClientState.MAIN_MENU: main_menu_btns,
            ClientState.CHAR_CHOOSE: char_choose_btns,
            ClientState.MAP_CHOOSE: map_choose_btns,
            ClientState.LOSE: set((self.btn_ok, )),
            ClientState.WIN: set((self.btn_ok, ))
        }

        self.drawing_layers = {
            'kirito': ImgLoader.load_image('images/characters/kirito/winner/kirito_win.png'),
            'ako': ImgLoader.load_image('images/characters/ako/winner/ako_win.png'),
            'dojo': ImgLoader.load_image('images/backgrounds/dojo.jpg'),
            'road': ImgLoader.load_image('images/backgrounds/road.jpg'),
            'temple': ImgLoader.load_image('images/backgrounds/temple.jpg'),
        }

        self.add_layers = []
        self.is_running = True
        self.chosen_char = CharacterType.KIRITO
        self.chosen_map = BackgroundType.ROAD
        self._change_state(ClientState.MAIN_MENU)
        self.temp_server_info = None

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        for layer in self.add_layers:
            self.screen.blit(layer[0], layer[1])

    def run(self):
        while self.is_running:
            handler = self.handlers[self.state]
            handler()

    def get_server_addr(self):
        def getting_addr(main_server_addr, char_type, waiting_time, client):
            #add more precise exception handling
            client.temp_server_info = None
            try:
                with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as sock:
                    sock.settimeout(waiting_time)
                    sock.connect(main_server_addr)
                    sock.sendall(bytes([char_type.value]))
                    data = sock.recv(13)

                    session_server_ip_address = str(data[0]) + '.' + str(data[1]) + '.' + str(data[2]) + '.' + str(data[3])
                    session_server_port = data[4]*256 + data[5]
                    
                    new_client_ip_address = str(data[6]) + '.' + str(data[7]) + '.' + str(data[8]) + '.' + str(data[9])
                    new_client_port = data[10]*256 + data[11]

                    enemy_char_type = CharacterType(data[12])
                    
                    operation_result_value = sock.recv(BUF_SIZE)
                    print(operation_result_value)
                    if operation_result_value[0] == OperationResult.GAME_PREPARED.value:
                        print("Getting value !!!")
                        client.temp_server_info = ((session_server_ip_address, session_server_port), (new_client_ip_address, new_client_port), enemy_char_type)
            except Exception as e:
                print(e)
                print("Getting main server addr error!")
                client.temp_server_info = None
            
        WATING_TIME = 10
        addr_getting_thread = threading.Thread(target=getting_addr, args=(self.MAIN_SERVER_ADDR, self.chosen_char, WATING_TIME//2, self))
        addr_getting_thread.start()
        start_time = time.time()
        while time.time() - start_time < WATING_TIME:
            events = pygame.event.get()
            pygame.event.pump()#maybe i can to remove it at all
            self.draw()
            pygame.display.update()
    
        addr_getting_thread.join()
        print(self.temp_server_info)
        if self.temp_server_info:
            self._change_state(ClientState.WIN)
        else:
            self._change_state(ClientState.LOSE)
            
    def _change_state(self, new_state):
        self.add_layers = []
        def hide_widgets(widgets):
            for widget in widgets:
                widget.hide()

        def show_widgets(widgets):
            for widget in widgets:
                widget.show()

        hide_widgets(self.widgets)
        if self.scene_widgets[new_state]:
            show_widgets(self.scene_widgets[new_state])

        self.state = new_state

    def _scene_handler(self):
        FPS = 60
        state = self.state
        clock = pygame.time.Clock()
        while self.state == state:
            self.draw()
            events = pygame.event.get()
            pygame.event.pump()#maybe i can to remove it at all
            pygame_widgets.update(events)
            pygame.display.update()
            clock.tick(FPS)

    def _main_menu_handler(self):
        self._scene_handler()

    def _char_choose_handler(self):
        self.add_layers.append((self.drawing_layers['kirito'], (0, 0)))
        self._scene_handler()

    def _map_choose_handler(self):
        self.add_layers.append((self.drawing_layers['dojo'], (0, 0)))
        self._scene_handler()

    def _waiting_game_handler(self):
        self._scene_handler()

    def _win_handler(self):
        self.add_layers.append((self.drawing_layers['kirito'], (0, 0)))
        self._scene_handler()

    def _lose_handler(self):
        self.add_layers.append((self.drawing_layers['ako'], (0, 0)))
        self._scene_handler()

    def _init_widgets(self):
        BUTTON_WIDTH = 250
        BUTTON_HEIGHT = 80
        FONT = pygame.font.SysFont('rubik', 36)

        def start_game_click():
            nonlocal self
            self._change_state(ClientState.CHAR_CHOOSE)

        def exit_click():
            nonlocal self
            self.is_running = False
            self.state = ClientState.EXIT

        def choose_pers(key):
            nonlocal self
            self.add_layers[0] = (self.drawing_layers[key], (0,0))

        def choose_map(key):
            nonlocal self
            self.add_layers[0] = (self.drawing_layers[key], (0,0))

        def ako_click():
            nonlocal self
            self.chosen_char = CharacterType.AKO
            choose_pers('ako')

        def kirito_click():
            nonlocal self
            self.chosen_char = CharacterType.KIRITO
            choose_pers('kirito')

        def to_menu_click():
            nonlocal self
            self._change_state(ClientState.MAIN_MENU)

        def to_map_click():
            nonlocal self
            self._change_state(ClientState.MAP_CHOOSE)

        def road_click():
            nonlocal self
            choose_map('road')
            self.chosen_map = BackgroundType.ROAD

        def temple_click():
            nonlocal self
            choose_map('temple')
            self.chosen_map = BackgroundType.TEMPLE

        def dojo_click():
            nonlocal self
            choose_map('dojo')
            self.chosen_map = BackgroundType.DOJO

        def to_choose_char():
            nonlocal self
            self._change_state(ClientState.CHAR_CHOOSE)

        def play():
            nonlocal self
            self.get_server_addr()
            if self.temp_server_info:
                try:
                    client = Client(self.chosen_char, self.chosen_map, self.screen)
                    client.run(self.temp_server_info)
                except:
                    print("Error in game executing")
            print(f"server addr = {self.temp_server_info}")

        self.btn_start_game = Button(self.screen,
                            600,
                            200,
                            BUTTON_WIDTH,
                            BUTTON_HEIGHT,
                            # image = img_normal,
                            radius = 20,
                            text="Start game",
                            textColour = (255, 255, 255),
                            font=FONT,
                            hoverColor=(255, 0, 0),
                            onClick=start_game_click,
                            # onClickParams=(choose_pers_scene,)
                            )
    
        self.btn_settings = Button(self.screen,
                            600,
                            400,
                            BUTTON_WIDTH,
                            BUTTON_HEIGHT,
                            radius = 20,
                            text="Settings",
                            textColour = (255, 255, 255),
                            font=FONT
                            )

        self.btn_exit = Button(self.screen,
                            600,
                            600,
                            BUTTON_WIDTH,
                            BUTTON_HEIGHT,
                            radius = 20,
                            textColour = (255, 255, 255),
                            font=FONT,
                            text="Exit",
                            onClick=exit_click,
                            # onClickParams=(self,)
                            )

        self.btn_kirito = Button(self.screen,
                            400,
                            200,
                            BUTTON_WIDTH,
                            BUTTON_HEIGHT,
                            radius = 20,
                            text="Kirito",
                            textColour = (255, 255, 255),
                            font=FONT,
                            hoverColor=(255, 0, 0),
                            onClick=kirito_click,
                            # onClickParams=(CharacterType.KIRITO,)
                            )
    
        self.btn_ako = Button(self.screen,
                            800,
                            200,
                            BUTTON_WIDTH,
                            BUTTON_HEIGHT,
                            radius = 20,
                            text="Ako",
                            textColour = (255, 255, 255),
                            font=FONT,
                            onClick=ako_click,
                            # onClickParams=(CharacterType.AKO,)
                            )
    
        self.btn_to_map = Button(self.screen,
                            800,
                            600,
                            BUTTON_WIDTH,
                            BUTTON_HEIGHT,
                            radius = 20,
                            text="Next",
                            textColour = (255, 255, 255),
                            font=FONT,
                            onClick=to_map_click,
                            # onClickParams=(choose_map_scene,)
                            )
        self.btn_to_menu = Button(self.screen,
                            400,
                            600,
                            BUTTON_WIDTH,
                            BUTTON_HEIGHT,
                            radius = 20,
                            text="Prev",
                            textColour = (255, 255, 255),
                            font=FONT,
                            onClick=to_menu_click,
                            # onClickParams=(start_scene,) 
                            )
    
        self.btn_to_game = Button(self.screen,
                            800,
                            600,
                            BUTTON_WIDTH,
                            BUTTON_HEIGHT,
                            radius = 20,
                            text="Play",
                            textColour = (255, 255, 255),
                            font=FONT,
                            onClick=play
                            )
    
        self.btn_to_choose_char = Button(self.screen,
                            400,
                            600,
                            BUTTON_WIDTH,
                            BUTTON_HEIGHT,
                            # img_active.get_rect().width,
                            # img_active.get_rect().height,
                            # image = img_normal,
                            radius = 20,
                            text="Prev",
                            textColour = (255, 255, 255),
                            font=FONT,
                            onClick=to_choose_char,
                            # onClickParams=(choose_pers_scene,) 
                            )
    
        self.btn_dojo = Button(self.screen,
                            300,
                            200,
                            BUTTON_WIDTH,
                            BUTTON_HEIGHT,
                            radius = 20,
                            text="Dojo",
                            textColour = (255, 255, 255),
                            font=FONT,
                            onClick=dojo_click,
                            # onClickParams=(BackgroundType.DOJO,) 
                            )
    
        self.btn_road = Button(self.screen,
                            600,
                            200,
                            BUTTON_WIDTH,
                            BUTTON_HEIGHT,
                            radius = 20,
                            text="Road",
                            textColour = (255, 255, 255),
                            font=FONT,
                            onClick=road_click,
                            # onClickParams=(BackgroundType.ROAD,) 
                            )
    
        self.btn_temple = Button(self.screen,
                            900,
                            200,
                            BUTTON_WIDTH,
                            BUTTON_HEIGHT,
                            radius = 20,
                            text="Land",
                            textColour = (255, 255, 255),
                            font=FONT,
                            onClick=temple_click,
                            # onClickParams=(BackgroundType.TEMPLE,) 
                            )

        self.btn_ok = Button(self.screen,
                        650,
                        700,
                        BUTTON_WIDTH,
                        BUTTON_HEIGHT,
                        radius = 20,
                        text="OK",
                        textColour = (255, 255, 255),
                        font=FONT,
                        onClick=to_map_click,
                        # onClickParams=(choose_map_scene, ) 
                        )
        
        return set((self.btn_ok, self.btn_temple, self.btn_road, self.btn_dojo, self.btn_to_choose_char,
                self.btn_to_game, self.btn_to_menu, self.btn_to_map, self.btn_ako, self.btn_kirito,
                self.btn_exit, self.btn_settings, self.btn_start_game))
    
if __name__ == "__main__":
    cm = ClientMachine()
    cm.run()