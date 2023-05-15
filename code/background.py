from imgs_loading import ImgLoader
from enum import Enum

class BackgroundType(Enum):
    DOJO = 0
    ROAD = 1
    TEMPLE = 2

class BackgroundFactory():
    @staticmethod
    def get_background(background_type):
        type_to_background = {
            BackgroundType.DOJO: ImgLoader().load_image('./images/backgrounds/dojo.jpg'),
            BackgroundType.ROAD: ImgLoader().load_image('./images/backgrounds/road.jpg'),
            BackgroundType.TEMPLE: ImgLoader().load_image('./images/backgrounds/temple.jpg')
        }
        return type_to_background[background_type]

class Background:
    def __init__(self, bg_image_name):
        self.bg_image = ImgLoader.load_image(bg_image_name)
    
    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))

if __name__ == "__main__":
    import pygame
    pygame.display.init()
    pygame.display.set_mode()
    print(BackgroundFactory.get_background(BackgroundType.DOJO).get_rect())
    print(pygame.display.Info())