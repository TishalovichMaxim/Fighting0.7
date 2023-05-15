import pygame
from enum import Enum
from imgs_loading import ImgLoader
from collections import deque
from dataclasses import dataclass
from constants import *

class CharacterState(Enum):
    STAND        = 0 
    MOVE_L       = 1
    MOVE_R       = 2
    ATTACK1      = 3
    ATTACK2      = 4
    BLOCK        = 5
    SIT          = 6
    JUMP         = 7
    SIT_ATTACK1  = 8
    JUMP_ATTACK1 = 9
    STAND_HURT   = 10

class CharacterSignal(Enum):
    RUN         = 0
    EMPTY       = 1
    BLOCK       = 2
    ATTACK1     = 3
    END_ATTACK  = 4
    END_RUN     = 5
    END_BLOCK   = 6
    ATTACK2     = 7
    END_JUMP    = 8
    JUMP        = 9
    MOVE_L      = 10
    MOVE_R      = 11
    END_MOVE_L  = 12
    END_MOVE_R  = 13
    SIT         = 14
    END_SIT     = 15
    ATTACKED    = 16
    END_ATTACKED = 17

class StateInfoType(Enum):
    HANDLER = 0
    TRANSITIONS = 1
    IMAGE_SPEED = 2
    SOUND = 3

class Direction(Enum):
    LEFT = 0
    RIGHT = 1

class SignalsSender():
    def send_sig(self, character, sig, add_info = []):
        character.signals_queue.append(Message(sig, add_info))

    def send_run_sig(self, character, direction):
        character.direction = direction
        character.signals_queue.append(Message(CharacterSignal.RUN, [direction]))

    def send_attack1_sig(self, character):
        character.signals_queue.append(Message(CharacterSignal.ATTACK1, []))

    def send_block_sig(self, character):
        character.signals_queue.append(Message(CharacterSignal.BLOCK, []))

    def send_end_run_sig(self, character, direction):
        if direction == character.direction:
            character.signals_queue.append(Message(CharacterSignal.END_RUN, []))

    def send_end_attack1_sig(self, character):
        character.signals_queue.append(Message(CharacterSignal.END_ATTACK, []))

    def send_end_block_sig(self, character):
        character.signals_queue.append(Message(CharacterSignal.END_BLOCK, []))

    def send_end_attack2_sig(self, character):
        character.signals_queue.append(Message(CharacterSignal.END_ATTACK, []))

    def send_attack2_sig(self, character):
        character.signals_queue.append(Message(CharacterSignal.ATTACK2, []))

    def send_jump_sig(self, character):
        character.signals_queue.append(Message(CharacterSignal.JUMP, []))        

@dataclass
class Message():
    signal: CharacterSignal
    add_info: list

class Character(pygame.sprite.Sprite):    

    def __init__(self, dir_name, is_left = True):
        super().__init__()
        self.hp = 100
        self.enemy = None
        self.image_counter = 0
        self.state = CharacterState.STAND
        self.image = None
        self.images = None
        self.load_imgs(dir_name)
        self.rect = self.images[self.state][0].get_rect()
        self.rect.y = 200
        self.direction = Direction.RIGHT
        self.speed = 10
        self.signals_queue = deque()
        self.is_moving = False
        self.movs = [False, False]
        
        self.state_info = {     
            CharacterState.STAND:
            { 
                StateInfoType.HANDLER: self.stand_state_handler,
                StateInfoType.TRANSITIONS: {
                        CharacterSignal.MOVE_L: CharacterState.MOVE_L,
                        CharacterSignal.MOVE_R: CharacterState.MOVE_R,
                        CharacterSignal.ATTACK2: CharacterState.ATTACK2,
                        CharacterSignal.JUMP: CharacterState.JUMP,
                        CharacterSignal.ATTACK1: CharacterState.ATTACK1,
                        CharacterSignal.SIT: CharacterState.SIT,
                        CharacterSignal.BLOCK: CharacterState.BLOCK,
                        CharacterSignal.ATTACKED: CharacterState.STAND_HURT
                    },
                StateInfoType.IMAGE_SPEED: 5,
                StateInfoType.SOUND: None
            },
            CharacterState.MOVE_L:
            { 
                StateInfoType.HANDLER: self.move_l_state_handler,
                StateInfoType.TRANSITIONS: {
                        CharacterSignal.END_MOVE_L: CharacterState.STAND,  
                        CharacterSignal.JUMP: CharacterState.JUMP
                    },
                StateInfoType.IMAGE_SPEED: 6,
                StateInfoType.SOUND: None
            },
            CharacterState.MOVE_R:
            { 
                StateInfoType.HANDLER: self.move_r_state_handler,
                StateInfoType.TRANSITIONS: {
                        CharacterSignal.END_MOVE_R: CharacterState.STAND,
                        CharacterSignal.JUMP: CharacterState.JUMP  
                    },
                StateInfoType.IMAGE_SPEED: 6,
                StateInfoType.SOUND: None
            },
            CharacterState.ATTACK1:
            { 
                StateInfoType.HANDLER: self.attack2_state_handler,
                StateInfoType.TRANSITIONS: {
                        CharacterSignal.END_ATTACK: CharacterState.STAND,  
                    },
                StateInfoType.IMAGE_SPEED: 5,
                StateInfoType.SOUND: None
            },
            CharacterState.ATTACK2:
            { 
                StateInfoType.HANDLER: self.attack2_state_handler,
                StateInfoType.TRANSITIONS: {
                        CharacterSignal.END_ATTACK: CharacterState.STAND,  
                    },
                StateInfoType.IMAGE_SPEED: 5,
                StateInfoType.SOUND: None
            },
            CharacterState.JUMP:
            { 
                StateInfoType.HANDLER: self.jump_state_handler,
                StateInfoType.TRANSITIONS: {
                        CharacterSignal.END_JUMP: CharacterState.STAND, 
                    },
                StateInfoType.IMAGE_SPEED: 9,
                StateInfoType.SOUND: None
            },
            CharacterState.SIT:
            { 
                StateInfoType.HANDLER: self.block_state_handler,
                StateInfoType.TRANSITIONS: {
                        CharacterSignal.END_SIT: CharacterState.STAND, 
                    },
                StateInfoType.IMAGE_SPEED: 30,
                StateInfoType.SOUND: None
            },
            CharacterState.BLOCK:
            { 
                StateInfoType.HANDLER: self.block_state_handler,
                StateInfoType.TRANSITIONS: {
                        CharacterSignal.END_BLOCK: CharacterState.STAND, 
                    },
                StateInfoType.IMAGE_SPEED: 4,
                StateInfoType.SOUND: None
            },
            CharacterState.STAND_HURT:
            { 
                StateInfoType.HANDLER: self.attacked_state_handler,
                StateInfoType.TRANSITIONS: {
                        CharacterSignal.END_ATTACKED: CharacterState.STAND, 
                    },
                StateInfoType.IMAGE_SPEED: 4,
                StateInfoType.SOUND: None
            }
        }

    def set_start_pos(self, is_left=True):
        self.rect.x = 0
        if not is_left:
            # self.rect.x = SCREEN_SIZE[0] - self.images[self.state][0].get_rect().width
            self.rect.right = SCREEN_SIZE[0]

        print(f"char rect = {self.rect}")

    def load_sounds(self, sounds_dict):
        for key in sounds_dict:
            self.state_info[key][StateInfoType.SOUND] = pygame.mixer.Sound(sounds_dict[key])

    def set_movs(self, move_l = False, move_r = False):
        self.movs[0] = move_l
        self.movs[1] = move_r

    def load_imgs(self, dir_name):
        """This directory must contain directories: run, stand, attack1, attack2"""
        loading_dirs = {
                        CharacterState.STAND: "stand",
                        CharacterState.MOVE_L: "run",
                        CharacterState.MOVE_R: "run",
                        CharacterState.ATTACK1: "attack1",
                        CharacterState.BLOCK: "block",
                        CharacterState.ATTACK2: "attack2",
                        CharacterState.JUMP: "jump",
                        CharacterState.SIT: "sit",
                        CharacterState.STAND_HURT: "stand-hurt"
                        
                        # CharacterState.CS_SIT: "sit",
                        # CharacterState.CS_SIT_ATTACK1: "sit-attack1",
                        # CharacterState.CS_JUMP_ATTACK1: 'jump-attack1'
                    }        

        self.images = {state: ImgLoader.load_ordered_imgs(dir_name + loading_dirs[state]) for state in loading_dirs}
        
    def update(self):
        super().update()

        while self.signals_queue:
            curr_sig = self.signals_queue.popleft()
            if curr_sig.signal in self.state_info[self.state][StateInfoType.TRANSITIONS]: #self.state_transitions[self.state]:
                self.change_state(self.state_info[self.state][StateInfoType.TRANSITIONS][curr_sig.signal])
        
        curr_img_list = self.images[self.state]
        try:
            self.image = curr_img_list[self.image_counter//self.get_image_speed()]
        except:
            print(self.state)
            print(curr_img_list)
            print(self.images)
            print(self.image_counter)
            print(self.get_image_speed())

        X_DELTA = 150
        self.rect.right = min(self.rect.right, SCREEN_SIZE[0] + X_DELTA)
        self.rect.left = max(self.rect.left, 0 - X_DELTA)

        if self.direction == Direction.LEFT:
            self.image = pygame.transform.flip(self.image, True, False)
        
        (self.state_info[self.state][StateInfoType.HANDLER])()
        self.image_counter += 1
        self.image_counter %= len(curr_img_list*self.get_image_speed())
        
    def change_state(self, new_state):
        self.state = new_state
        sound = self.state_info[new_state][StateInfoType.SOUND]
        if sound:
            sound.play()
        self.image_counter = 0

    def block_state_handler(self):
        return

    def stand_state_handler(self):
        return

    def attack1_state_handler(self):
        #DELETE IT!!!!
        if self.enemy != None:
            if self.enemy.get_hurt_box().colliderect(self.get_hit_box()):
                self.enemy.hp -= 10
                self.enemy.signals_queue.append(Message(CharacterSignal.ATTACKED, []))
        if self.image_counter == len(self.images[self.state]) - 1:
            self.signals_queue.append(Message(CharacterSignal.END_ATTACK, []))

    def attack2_state_handler(self):
        #DELETE IT!!!!
        if self.enemy != None:
            if self.enemy.get_hurt_box().colliderect(self.get_hit_box()):
                self.enemy.hp -= 15
                self.enemy.signals_queue.append(Message(CharacterSignal.ATTACKED, []))
        if self.image_counter == len(self.images[self.state])*self.state_info[self.state][StateInfoType.IMAGE_SPEED] - 1:
            self.signals_queue.append(Message(CharacterSignal.END_ATTACK, []))

    def move_l_state_handler(self):
        self.rect.move_ip(-self.speed, 0)
        self.direction = Direction.LEFT

    def move_r_state_handler(self):
        self.rect.move_ip(self.speed, 0)
        self.direction = Direction.RIGHT

    def attacked_state_handler(self):
        if self.image_counter == len(self.images[self.state])*self.state_info[self.state][StateInfoType.IMAGE_SPEED] - 1:
            self.signals_queue.append(Message(CharacterSignal.END_ATTACKED, []))

    def jump_state_handler(self):
        T = 40
        H = 250
        g = -8*H/T**2
        v_0 = -g*T/2

        y_0 = 200
        t = self.image_counter
        y = y_0 + v_0*t + g*t*t//2

        self.rect.y = y_0 - y

        dx = 0
        if self.movs[0]:
            dx = -self.speed
            self.direction = Direction.LEFT
        elif self.movs[1]:
            dx = self.speed
            self.direction = Direction.RIGHT

        self.rect.x += dx

        if self.image_counter == T:
            self.signals_queue.append(Message(CharacterSignal.END_JUMP, []))
            self.rect.y = 200

    def get_image_speed(self):
        return self.state_info[self.state][StateInfoType.IMAGE_SPEED]
    
    def get_hit_box(self):
        pass

    def get_hurt_box(self):
        pass

    def get_info(self)->str:
        return str(self.rect.x) + ',' + str(self.rect.y) + ',' + str(self.image_counter)+ ',' + str(self.state.value) + ',' + str(self.direction.value) + ',' + str(self.hp)
    
    def set_image(self):
        curr_img_list = self.images[self.state]
        self.image = curr_img_list[self.image_counter//self.get_image_speed()]
        if self.direction == Direction.LEFT:
            self.image = pygame.transform.flip(self.image, True, False)