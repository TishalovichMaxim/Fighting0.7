import sys
sys.path.append(sys.path[0] + "\\..\\..")

from enum import Enum, auto
from pygame_widgets.button import Button
from collections import deque
import pygame, pygame_widgets, traceback
from src.utils.imgs_loading import ImgLoader
from src.chars.character_type import CharacterType
from src.utils.background import BackgroundType
from src.constants import *
from src.networking.networking import GameResult
from src.networking.client.client import Client
from src.utils.logger import Logger
from src.networking.address import AddressFactory

class ClientState(Enum):
    MAIN_MENU = auto()
    CHAR_CHOOSE = auto()
    MAP_CHOOSE = auto()
    WAITING_GAME = auto()
    WIN = auto()
    LOSE = auto()
    EXIT = auto()
    ERROR = auto()

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
            ClientState.LOSE: self._lose_handler,
            ClientState.ERROR: self._error_handler,
            ClientState.WAITING_GAME: self._waiting_game_handler
        }

        self.scene_widgets = {
            ClientState.MAIN_MENU: main_menu_btns,
            ClientState.CHAR_CHOOSE: char_choose_btns,
            ClientState.MAP_CHOOSE: map_choose_btns,
            ClientState.LOSE: set((self.btn_ok, )),
            ClientState.WIN: set((self.btn_ok, )),
            ClientState.ERROR: set((self.btn_ok, )),
            ClientState.WAITING_GAME: set((self.btn_cancel, ))
        }

        self.drawing_layers = {
            'kirito': ImgLoader.load_image('images/characters/kirito/winner/kirito_win.png'),
            'ako': ImgLoader.load_image('images/characters/ako/winner/ako_win.png'),
            'error-caption': ImgLoader.load_image('images/backgrounds/error/error-caption.png'),
            'dojo': ImgLoader.load_image('images/backgrounds/dojo.jpg'),
            'road': ImgLoader.load_image('images/backgrounds/road.jpg'),
            'temple': ImgLoader.load_image('images/backgrounds/temple.jpg'),
            'win': ImgLoader.load_image('images/backgrounds/winners/winner_caption.png'),
            'lose': ImgLoader.load_image('images/backgrounds/losers/game_over.png'),
            'choose_kirito': ImgLoader.load_image('images/characters/kirito/default/kirito.png'),
            'choose_ako': ImgLoader.load_image('images/characters/ako/default/ako.png')
        }

        self.add_layers = []
        self.is_running = True
        self.chosen_char = CharacterType.KIRITO
        self.chosen_map = BackgroundType.ROAD
        self._change_state(ClientState.MAIN_MENU)
        self.temp_server_info = None

        self.logger = Logger("Client")

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        for layer in self.add_layers:
            self.screen.blit(layer[0], layer[1])

    def run(self):
        while self.is_running:
            handler = self.handlers[self.state]
            handler()

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
        if self.chosen_char == CharacterType.KIRITO:
            self.add_layers.append((self.drawing_layers['choose_kirito'], (0, 0)))
        else:
            self.add_layers.append((self.drawing_layers['choose_ako'], (0, 0)))

        self._scene_handler()

    def _error_handler(self):
        self.add_layers.append((self.drawing_layers['error-caption'], (0, 0)))
        self._scene_handler()

    def _map_choose_handler(self):
        match self.chosen_map:
            case BackgroundType.DOJO:
                self.add_layers.append((self.drawing_layers['dojo'], (0, 0)))
            case BackgroundType.ROAD:
                self.add_layers.append((self.drawing_layers['road'], (0, 0)))
            case BackgroundType.TEMPLE:
                self.add_layers.append((self.drawing_layers['temple'], (0, 0)))

        self._scene_handler()

    def _waiting_game_handler(self):
        try:
            client = Client(self.chosen_char, self.chosen_map, self.screen, AddressFactory.create_by_addr(self.MAIN_SERVER_ADDR), self)
            res = client.run()
        except:
            traceback.print_exc()
            print("Error in client running")
            res = GameResult.ERROR
        print("play is ended...")
        print(res)

        match res:
            case GameResult.WIN:
                self._change_state(ClientState.WIN)
            case GameResult.LOSE:
                self._change_state(ClientState.LOSE)
            case GameResult.ERROR:
                self._change_state(ClientState.ERROR)

    def _win_handler(self):
        match self.chosen_char:
            case CharacterType.KIRITO:
                self.add_layers.append((self.drawing_layers['kirito'], (0, 0)))
            case CharacterType.AKO:
                self.add_layers.append((self.drawing_layers['ako'], (0, 0)))
        
        self.add_layers.append((self.drawing_layers['win'], (0, 0)))
        self._scene_handler()

    def _lose_handler(self):
        match self.chosen_char:
            case CharacterType.KIRITO:
                self.add_layers.append((self.drawing_layers['kirito'], (0, 0)))
            case CharacterType.AKO:
                self.add_layers.append((self.drawing_layers['ako'], (0, 0)))
        
        self.add_layers.append((self.drawing_layers['lose'], (0, 0)))
        self._scene_handler()

    def _init_widgets(self):
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
            choose_pers('choose_ako')

        def kirito_click():
            nonlocal self
            self.chosen_char = CharacterType.KIRITO
            choose_pers('choose_kirito')

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

        def cancel_click():
            nonlocal self
            self._change_state(ClientState.MAP_CHOOSE)

        def play():
            nonlocal self
            self._change_state(ClientState.WAITING_GAME)
            # print(f"server addr = {self.temp_server_info}")

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
        
        self.btn_cancel = Button(self.screen,
                                650,
                                700,
                                BUTTON_WIDTH,
                                BUTTON_HEIGHT,
                                radius = 20,
                                text="Cancel",
                                textColour = (255, 255, 255),
                                font=FONT,
                                onClick=cancel_click,
                                )
        
        return set((self.btn_ok, self.btn_temple, self.btn_road, self.btn_dojo, self.btn_to_choose_char,
                self.btn_to_game, self.btn_to_menu, self.btn_to_map, self.btn_ako, self.btn_kirito,
                self.btn_exit, self.btn_settings, self.btn_start_game, self.btn_cancel))

if __name__ == "__main__":
    cm = ClientMachine()
    cm.run()