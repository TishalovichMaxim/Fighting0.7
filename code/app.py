import pygame, asyncio
from pygame_widgets.button import Button
import pygame_widgets, sys
from imgs_loading import ImgLoader
from chars.charater_type import CharacterType
from background import BackgroundType
from constants import *
from networking import GameResult

def quit(app):
    app.is_running = False
    sys.exit()

chosen_char_type = CharacterType.KIRITO
chosen_map_type = BackgroundType.ROAD

class App:
    def __init__(self, start_scene):
        pygame.init()
        pygame.mixer.init()
        sound = pygame.mixer.Sound("./music/menu.mp3")
        # sound.play(loops=-1)
        self.screen = pygame.display.set_mode((SCREEN_SIZE))
        self.is_running = True
        self.FPS = 60
        self.scene = start_scene
        self.background_image = ImgLoader.load_image("./images/backgrounds/main.png")

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.scene.draw(self.screen)

    def run(self):
        clock = pygame.time.Clock()
        while self.is_running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    quit(self)
                    pygame.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    #self.quit()
                    pass

            self.draw()
            pygame_widgets.update(events)
            pygame.display.update()
            clock.tick(self.FPS)

if __name__ == "__main__":
    pygame.font.init()
    FONT = pygame.font.Font(None, 36)
    app = App(None)

    from scene import Scene
    from imgs_loading import ImgLoader

    img_active = pygame.transform.scale2x(ImgLoader.load_image("./images/ui/buttons/btn_disable.png"))
    img_disabled = ImgLoader.load_image("./images/ui/buttons/btn_disable.png")
    img_hover = ImgLoader.load_image("./images/ui/buttons/btn_disable.png")
    img_normal = pygame.transform.scale2x(ImgLoader.load_image("./images/ui/buttons/btn_normal.png"))

    def change_scene(to):
        for widget in all_widgets:
            widget.hide()

        for widget in to.widgets_grp:
            widget.show()
        app.scene = to

    def choose_char(new_char_type):
        global chosen_char_type
        chosen_char_type = new_char_type
        choose_pers_scene.surfaces[0] = (chosen_characters[new_char_type], (0, 0))

    def choose_map(new_map_type):
        global chosen_map_type
        chosen_map_type = new_map_type
        choose_map_scene.surfaces[0] = (chosen_maps[new_map_type], (250, 70))

    def play():
        from client import Client
        client = Client(('127.0.0.1', 65532), chosen_char_type, chosen_map_type, app.screen)
        try:
            print("Running client")
            game_result = asyncio.run(client.run())
            print(f"Game result = {game_result}")
            if game_result == GameResult.ERROR:
                print("Error result")
                change_scene(choose_map_scene)
            else:
                print("No error result")
                get_game_result_scene(game_result, chosen_char_type)
                change_scene(game_result_scene)
        except Exception as e:
            print(e)
            # print("Aboba")
            change_scene(choose_map_scene)

    def get_game_result_scene(game_result, char_type):
        global game_result_scene
        game_result_scene.surfaces = []
    
        match char_type:
            case CharacterType.KIRITO:
                game_result_scene.surfaces.append((ImgLoader.load_image("./images/characters/kirito/winner/kirito_win.png"), (0, 0)))
            case CharacterType.AKO:        
                game_result_scene.surfaces.append((ImgLoader.load_image("./images/characters/ako/winner/ako_win.png"), (0, 0)))
        
        game_result_scene.surfaces.append((ImgLoader.load_image("./images/backgrounds/result_caption.png"), (0, 0)))
        
        match game_result:
            case GameResult.WIN:
                game_result_scene.surfaces.append((ImgLoader.load_image("./images/backgrounds/winners/winner_caption.png"), (0, 0)))
            case GameResult.LOSE:
                game_result_scene.surfaces.append((ImgLoader.load_image("./images/backgrounds/losers/game_over.png"), (0, 0)))
        
    all_widgets = set()
    start_scene = Scene()
    choose_pers_scene = Scene()
    choose_map_scene = Scene()
    game_result_scene = Scene()

    btn_start_game = Button(app.screen,
                            600,
                            200,
                            img_active.get_rect().width,
                            img_active.get_rect().height,
                            image = img_normal,
                            radius = 20,
                            text="Start game",
                            textColour = (255, 255, 255),
                            font=FONT,
                            hoverColor=(255, 0, 0),
                            onClick=change_scene,
                            onClickParams=(choose_pers_scene,)
                            )
    
    btn_settings = Button(app.screen,
                            600,
                            400,
                            img_active.get_rect().width,
                            img_active.get_rect().height,
                            image = img_normal,
                            radius = 20,
                            text="Settings",
                            textColour = (255, 255, 255),
                            font=FONT
                            )

    btn_exit = Button(app.screen,
                            600,
                            600,
                            img_active.get_rect().width,
                            img_active.get_rect().height,
                            radius = 20,
                            textColour = (255, 255, 255),
                            image = img_normal,
                            font=FONT,
                            text="Exit",
                            onClick=quit,
                            onClickParams=(app,)
                            )

    btn_kirito = Button(app.screen,
                            400,
                            200,
                            img_active.get_rect().width,
                            img_active.get_rect().height,
                            image = img_normal,
                            radius = 20,
                            text="Kirito",
                            textColour = (255, 255, 255),
                            font=FONT,
                            hoverColor=(255, 0, 0),
                            onClick=choose_char,
                            onClickParams=(CharacterType.KIRITO,)
                            )
    
    btn_ako = Button(app.screen,
                            800,
                            200,
                            img_active.get_rect().width,
                            img_active.get_rect().height,
                            image = img_normal,
                            radius = 20,
                            text="Ako",
                            textColour = (255, 255, 255),
                            font=FONT,
                            onClick=choose_char,
                            onClickParams=(CharacterType.AKO,)
                            )
    
    btn_to_map = Button(app.screen,
                            800,
                            600,
                            img_active.get_rect().width,
                            img_active.get_rect().height,
                            image = img_normal,
                            radius = 20,
                            text="Next",
                            textColour = (255, 255, 255),
                            font=FONT,
                            onClick=change_scene,
                            onClickParams=(choose_map_scene,)
                            )
    btn_to_menu = Button(app.screen,
                            400,
                            600,
                            img_active.get_rect().width,
                            img_active.get_rect().height,
                            image = img_normal,
                            radius = 20,
                            text="Prev",
                            textColour = (255, 255, 255),
                            font=FONT,
                            onClick=change_scene,
                            onClickParams=(start_scene,) 
                            )
    
    btn_to_game = Button(app.screen,
                            800,
                            600,
                            img_active.get_rect().width,
                            img_active.get_rect().height,
                            image = img_normal,
                            radius = 20,
                            text="Play",
                            textColour = (255, 255, 255),
                            font=FONT,
                            onClick=play
                            )
    
    btn_to_choose_char = Button(app.screen,
                            400,
                            600,
                            img_active.get_rect().width,
                            img_active.get_rect().height,
                            image = img_normal,
                            radius = 20,
                            text="Prev",
                            textColour = (255, 255, 255),
                            font=FONT,
                            onClick=change_scene,
                            onClickParams=(choose_pers_scene,) 
                            )
    
    btn_dojo = Button(app.screen,
                            300,
                            200,
                            img_active.get_rect().width,
                            img_active.get_rect().height,
                            image = img_normal,
                            radius = 20,
                            text="Dojo",
                            textColour = (255, 255, 255),
                            font=FONT,
                            onClick=choose_map,
                            onClickParams=(BackgroundType.DOJO,) 
                            )
    
    btn_road = Button(app.screen,
                            600,
                            200,
                            img_active.get_rect().width,
                            img_active.get_rect().height,
                            image = img_normal,
                            radius = 20,
                            text="Road",
                            textColour = (255, 255, 255),
                            font=FONT,
                            onClick=choose_map,
                            onClickParams=(BackgroundType.ROAD,) 
                            )
    
    btn_temple = Button(app.screen,
                            900,
                            200,
                            img_active.get_rect().width,
                            img_active.get_rect().height,
                            image = img_normal,
                            radius = 20,
                            text="Land",
                            textColour = (255, 255, 255),
                            font=FONT,
                            onClick=choose_map,
                            onClickParams=(BackgroundType.TEMPLE,) 
                            )

    btn_ok = Button(app.screen,
                        650,
                        700,
                        img_active.get_rect().width,
                        img_active.get_rect().height,
                        image = img_normal,
                        radius = 20,
                        text="OK",
                        textColour = (255, 255, 255),
                        font=FONT,
                        onClick=change_scene,
                        onClickParams=(choose_map_scene, ) 
                        )

    chosen_characters = {
        CharacterType.KIRITO: ImgLoader.load_image('images/characters/kirito/menus/kirito.png'),
        CharacterType.AKO: ImgLoader.load_image('images/characters/ako/menus/ako.png'),
    }

    chosen_maps = {
        BackgroundType.ROAD: pygame.transform.scale(ImgLoader.load_image('images/backgrounds/road.jpg'), (1000, 500)),
        BackgroundType.DOJO: pygame.transform.scale(ImgLoader.load_image('images/backgrounds/dojo.jpg'), (1000, 500)),
        BackgroundType.TEMPLE: pygame.transform.scale(ImgLoader.load_image('images/backgrounds/temple.jpg'), (1000, 500))
    }

    app.scene = start_scene
    all_widgets |= {btn_start_game, btn_settings, btn_exit,
                btn_ako, btn_kirito, btn_to_map, btn_to_menu,
                btn_dojo, btn_road, btn_temple, btn_to_game, btn_to_choose_char, btn_ok}
    
    choose_pers_scene.surfaces.append((chosen_characters[chosen_char_type], (0, 0)))
    choose_map_scene.surfaces.append((chosen_maps[chosen_map_type], (250, 70)))
    print(choose_pers_scene.surfaces)
    start_scene.add_widget((btn_start_game, btn_settings, btn_exit))
    choose_pers_scene.add_widget((btn_to_map, btn_to_menu, btn_kirito, btn_ako))
    choose_map_scene.add_widget((btn_dojo, btn_temple, btn_road, btn_to_game, btn_to_choose_char))
    game_result_scene.add_widget((btn_ok, ))

    change_scene(start_scene)
    app.run()