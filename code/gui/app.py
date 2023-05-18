import pygame, pygame_widgets
from constants import *
from imgs_loading import ImgLoader

class App:
    def __init__(self, start_scene):
        pygame.init()
        pygame.mixer.init()
        sound = pygame.mixer.Sound("./music/menu.mp3")
        sound.play(loops=-1)
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