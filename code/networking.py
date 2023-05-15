from chars.character import CharacterState, CharacterSignal
from chars.kirito import Kirito
from chars.char_factory import CharFactory
from chars.char_info import CharInfo
import pygame, threading
from imgs_loading import ImgLoader
from chars.ako import Ako
from pygame.constants import (
    KEYDOWN,
    KEYUP,
    K_d,
    K_LEFT,
    K_RIGHT,
    K_DOWN,
    K_UP,
    K_f,
    K_s
)

class HealthBars:
    def __init__(self, char1, char2, screen) -> None:
        self.char1 = char1
        self.char2 = char2
        self.screen = screen

        width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
        print(f"width={width} height={height}")
        self.height = height // 20
        self.width = width // 5
        self.left_rect = pygame.rect.Rect(50, 100, self.width*self.char1.hp/100, self.height)
        self.right_rect = pygame.rect.Rect(width - 50 - self.width*self.char2.hp/100, 100, self.width*self.char2.hp/100, self.height)
        print(f"left_rect = {self.left_rect} right_rect = {self.right_rect}")

    def draw(self):
        def draw_health_bar(rect, hp):
            pygame.draw.rect(self.screen, (0, 0, 0), rect)
            pygame.draw.rect(self.screen, (255, 0, 0), (rect.topleft, (rect.width*hp/100, rect.height)))        
        draw_health_bar(self.left_rect, self.char1.hp)
        draw_health_bar(self.right_rect, self.char2.hp)

class SessionGame:
    def __init__(self, char_type_1, char_type_2) -> None:
        self.char1 = CharFactory.get_char(char_type_1)
        self.char2 = CharFactory.get_char(char_type_2)
        
        info_object = pygame.display.Info()
        self.sizes = (info_object.current_w, info_object.current_h)

        self.char1.enemy = self.char2
        self.char2.enemy = self.char1
        
        self.char_grp = pygame.sprite.Group(self.char1, self.char2)
        
    def is_ended(self):
        return self.char1.hp <= 0 or self.char2.hp <= 0

    # def get_char1_info(self):
    #     return bytes(self.char1.get_info(), encoding=ascii)
    
    # def get_char2_info(self):
    #     return bytes(self.char2.get_info(), encoding=ascii)
        
    def update(self):
        self.char_grp.update()

    def set_chars(self, char_info_1, char_info_2):
        def set_char(char, char_info):
            char.rect.x = char_info.rect_x
            char.rect.y = char_info.rect_y
            char.image_counter = char_info.image_counter
            char.state = char_info.state
            char.direction = char_info.direction
            char.hp = char_info.hp

        set_char(self.char1, char_info_1)
        set_char(self.char2, char_info_2)

class ServerGame(SessionGame):
    def __init__(self, char_type_1, char_type_2) -> None:
        super().__init__(char_type_1, char_type_2)

    def get_chars_info(self, reverse=False):
        if not reverse:
            return bytes(self.char1.get_info() + ',' + self.char2.get_info(), encoding='ascii')
        else:
            return bytes(self.char2.get_info() + ',' + self.char1.get_info(), encoding='ascii')
        
class ClientGame(SessionGame):
    def __init__(self, char_type_1, char_type_2, screen, surf_background) -> None:
        super().__init__(char_type_1, char_type_2)
        self.screen = screen
        self.background = surf_background
        self.health_bars = HealthBars(self.char1, self.char2, self.screen)

    def get_input(self):
        message = []
        move_l = False
        move_r = False

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_d:
                    message.append(CharacterSignal.ATTACK1)
                elif event.key == K_f:
                    message.append(CharacterSignal.ATTACK2)
                elif event.key == K_s:
                    message.append(CharacterSignal.BLOCK)
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    message.append(CharacterSignal.END_MOVE_L)
                elif event.key == K_RIGHT:
                    message.append(CharacterSignal.END_MOVE_R)
                elif event.key == K_DOWN:
                    message.append(CharacterSignal.END_SIT)
                elif event.key == K_s:
                    message.append(CharacterSignal.END_BLOCK)

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            message.append(CharacterSignal.MOVE_L)
            move_l = True
        elif keys[K_RIGHT]:
            message.append(CharacterSignal.MOVE_R)
            move_r = True

        if keys[K_DOWN]:
            message.append(CharacterSignal.SIT)
        if keys[K_UP]:
            message.append(CharacterSignal.JUMP)
 
        result = [move_l, move_r]
        for i in range(len(message)):
            result.append(message[i].value)

        return result
            
    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.char_grp.draw(self.screen)
        self.health_bars.draw()