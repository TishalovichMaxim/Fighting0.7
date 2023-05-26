from src.chars.character import CharacterState, Character, Direction
import pygame

class Kirito(Character):
    def __init__(self, dir_name):
        super().__init__(dir_name)
        self.hurt_boxes = {
            Direction.RIGHT:{
                CharacterState.MOVE_L:{
                    0: (445, 240, 30, 320),
                    1: (445, 240, 30, 320),
                    2: (445, 240, 30, 320),
                    3: (445, 240, 30, 320),
                    4: (445, 240, 30, 320),
                    5: (445, 240, 30, 320)
                },
                CharacterState.MOVE_R:{
                    0: (445, 240, 30, 320),
                    1: (445, 240, 30, 320),
                    2: (445, 240, 30, 320),
                    3: (445, 240, 30, 320),
                    4: (445, 240, 30, 320),
                    5: (445, 240, 30, 320)
                },
                CharacterState.STAND:{
                    0: (450, 240, 30, 320),
                    1: (450, 240, 30, 320),
                    2: (450, 240, 30, 320),
                    3: (450, 240, 30, 320),
                    4: (450, 240, 30, 320),
                    5: (450, 240, 30, 320),
                    6: (450, 240, 30, 320),
                    7: (450, 240, 30, 320)
                },
                CharacterState.JUMP:{
                    0: (450, 240, 30, 300),
                    1: (450, 240, 30, 300),
                    2: (450, 240, 30, 300),
                    3: (450, 240, 30, 300),
                    4: (450, 240, 30, 300),
                    5: (450, 240, 30, 300),
                    6: (450, 240, 30, 300)
                },
                CharacterState.SIT:{
                    0: (450, 370, 30, 200),
                    1: (450, 370, 30, 200)
                },
                CharacterState.BLOCK:{
                    0: (443, 240, 40, 320)
                },
                CharacterState.ATTACK1:{
                    0: (460, 330, 40, 210),
                    1: (470, 330, 40, 210),
                    2: (490, 330, 40, 210),
                    3: (500, 330, 40, 210),
                    4: (510, 330, 40, 210),
                    5: (430, 330, 40, 210),
                    6: (420, 330, 40, 210),
                    7: (410, 330, 40, 210)
                },
                CharacterState.ATTACK2:{
                    0: (460, 330, 40, 210),
                    1: (470, 330, 40, 210),
                    2: (490, 330, 40, 210),
                    3: (500, 330, 40, 210),
                    4: (510, 330, 40, 210),
                    5: (430, 330, 40, 210),
                    6: (420, 330, 40, 210),
                    7: (410, 330, 40, 210)
                }
            },
            Direction.LEFT:{
                CharacterState.MOVE_L:{
                    0: (445, 240, 30, 320),
                    1: (445, 240, 30, 320),
                    2: (445, 240, 30, 320),
                    3: (445, 240, 30, 320),
                    4: (445, 240, 30, 320),
                    5: (445, 240, 30, 320)
                },
                CharacterState.MOVE_R:{
                    0: (445, 240, 30, 320),
                    1: (445, 240, 30, 320),
                    2: (445, 240, 30, 320),
                    3: (445, 240, 30, 320),
                    4: (445, 240, 30, 320),
                    5: (445, 240, 30, 320)
                },
                CharacterState.STAND:{
                    0: (450, 240, 30, 320),
                    1: (450, 240, 30, 320),
                    2: (450, 240, 30, 320),
                    3: (450, 240, 30, 320),
                    4: (450, 240, 30, 320),
                    5: (450, 240, 30, 320),
                    6: (450, 240, 30, 320),
                    7: (450, 240, 30, 320)
                },
                CharacterState.JUMP:{
                    0: (450, 240, 30, 300),
                    1: (450, 240, 30, 300),
                    2: (450, 240, 30, 300),
                    3: (450, 240, 30, 300),
                    4: (450, 240, 30, 300),
                    5: (450, 240, 30, 300),
                    6: (450, 240, 30, 300)
                },
                CharacterState.SIT:{
                    0: (450, 370, 30, 200),
                    1: (450, 370, 30, 200)
                },
                CharacterState.BLOCK:{
                    0: (443, 240, 40, 320)
                },
                CharacterState.ATTACK1:{
                    0: (460, 330, 40, 210),
                    1: (450, 330, 40, 210),
                    2: (430, 330, 40, 210),
                    3: (420, 330, 40, 210),
                    4: (410, 330, 40, 210),
                    5: (430, 330, 40, 210),
                    6: (420, 330, 40, 210),
                    7: (410, 330, 40, 210)
                },
                CharacterState.ATTACK2:{
                    0: (460, 330, 40, 210),
                    1: (450, 330, 40, 210),
                    2: (430, 330, 40, 210),
                    3: (420, 330, 40, 210),
                    4: (410, 330, 40, 210),
                    5: (430, 330, 40, 210),
                    6: (420, 330, 40, 210),
                    7: (410, 330, 40, 210)
                }
            }
        }
        self.hit_boxes = {
            Direction.RIGHT:{
                CharacterState.ATTACK1: {
                    0: (0, 0, 0, 0),
                    1: (0, 0, 0, 0),
                    2: (450, 350, 30, 30),
                    3: (450, 350, 180, 30),
                    4: (450, 350, 400, 30),
                    5: (0, 0, 0, 0),
                    6: (420, 350, 30, 30),
                    7: (270, 350, 180, 30)
                },
                CharacterState.ATTACK2: {
                    0: (0, 0, 0, 0),
                    1: (0, 0, 0, 0),
                    2: (630, 300, 70, 30),
                    3: (640, 300, 70, 30),
                    4: (635, 300, 70, 30),
                    5: (655, 300, 70, 30),
                    6: (665, 300, 70, 30),
                    7: (660, 300, 70, 30)
                }
            },
            Direction.LEFT:{
                CharacterState.ATTACK1: {
                    0: (0, 0, 0, 0),
                    1: (0, 0, 0, 0),
                    2: (420, 350, 30, 30),
                    3: (270, 350, 180, 30),
                    4: (50, 350, 400, 30),
                    5: (0, 0, 0, 0),
                    6: (420, 350, 30, 30),
                    7: (270, 350, 180, 30)
                },
                CharacterState.ATTACK2: {
                    0: (0, 0, 0, 0),
                    1: (0, 0, 0, 0),
                    2: (240, 300, 70, 30),
                    3: (230, 300, 70, 30),
                    4: (235, 300, 70, 30),
                    5: (215, 300, 70, 30),
                    6: (205, 300, 70, 30),
                    7: (210, 300, 70, 30)
                }
            }
        }
        sounds = {
                CharacterState.ATTACK1: 'music/kirito/long-sword.wav',
                CharacterState.BLOCK: 'music/kirito/def.wav',
                CharacterState.ATTACK2: 'music/kirito/attack2.wav',
                CharacterState.STAND_HURT: 'music/kirito/damage.wav',
                CharacterState.JUMP: 'music/kirito/jump.wav'
                }
        self.load_sounds(sounds)
        
    def get_hit_box(self):
        if self.state in self.hit_boxes[self.direction]:
            rect_vals = self.hit_boxes[self.direction][self.state][self.image_counter//self.get_image_speed()]
            return pygame.Rect((self.rect.x + rect_vals[0], self.rect.y + rect_vals[1]), (rect_vals[2], rect_vals[3]))
        else:
            return pygame.Rect((self.rect.x, self.rect.y), (10, 10))

    def get_hurt_box(self):
        if self.state in self.hurt_boxes[self.direction]:
            #print(self.image_counter//self.get_image_speed())
            rect_vals = self.hurt_boxes[self.direction][self.state][self.image_counter//self.get_image_speed()]
            return pygame.Rect((self.rect.x + rect_vals[0], self.rect.y + rect_vals[1]), (rect_vals[2], rect_vals[3]))
        else:
            return pygame.Rect((self.rect.x, self.rect.y), (10, 10))