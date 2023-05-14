from chars.character import CharacterState, Character, Direction
import pygame

class Ako(Character):
    def __init__(self, dir_name):
        super().__init__(dir_name)
        self.hurt_boxes = {
            Direction.RIGHT:{
                CharacterState.MOVE_L:{
                    0: (375, 240, 30, 320),
                    1: (375, 240, 30, 320),
                    2: (375, 240, 30, 320),
                    3: (375, 240, 30, 320),
                    4: (375, 240, 30, 320),
                    5: (375, 240, 30, 320),
                    6: (375, 240, 30, 320),
                    7: (375, 240, 30, 320),
                    8: (375, 240, 30, 320),
                    9: (375, 240, 30, 320)
                },
                CharacterState.MOVE_R:{
                    0: (384, 240, 30, 320),
                    1: (384, 240, 30, 320),
                    2: (384, 240, 30, 320),
                    3: (384, 240, 30, 320),
                    4: (384, 240, 30, 320),
                    5: (384, 240, 30, 320),
                    6: (384, 240, 30, 320),
                    7: (384, 240, 30, 320),
                    8: (384, 240, 30, 320),
                    9: (384, 240, 30, 320)
                },
                CharacterState.STAND:{
                    0: (384, 240, 30, 320),
                    1: (384, 240, 30, 320),
                    2: (384, 240, 30, 320),
                    3: (384, 240, 30, 320),
                    4: (384, 240, 30, 320),
                    5: (384, 240, 30, 320),
                    6: (384, 240, 30, 320)
                },
                CharacterState.JUMP:{
                    0: (384, 240, 30, 300),
                    1: (384, 240, 30, 300),
                    2: (384, 240, 30, 300),
                    3: (384, 240, 30, 300),
                    4: (384, 240, 30, 300),
                    5: (384, 240, 30, 300),
                    6: (384, 240, 30, 300),
                    7: (384, 240, 30, 300),
                    8: (384, 240, 30, 300),
                    9: (384, 240, 30, 300),
                    10: (384, 240, 30, 300),
                    11: (384, 240, 30, 300)
                },
                CharacterState.SIT:{
                    0: (384, 370, 30, 200),
                    1: (384, 370, 30, 200)
                },
                CharacterState.BLOCK:{
                    0: (384, 240, 40, 320)
                },
                CharacterState.ATTACK1:{
                    0: (384, 240, 30, 320),
                    1: (384, 240, 30, 320),
                    2: (384, 240, 30, 320),
                    3: (384, 240, 30, 320),
                    4: (384, 240, 30, 320),
                    5: (384, 240, 30, 320),
                    6: (384, 240, 30, 320),
                    7: (384, 240, 30, 320)
                },
                CharacterState.ATTACK2:{
                    0: (384, 240, 30, 320),
                    1: (384, 240, 30, 320),
                    2: (384, 240, 30, 320),
                    3: (384, 240, 30, 320),
                    4: (384, 240, 30, 320),
                    5: (384, 240, 30, 320),
                    6: (384, 240, 30, 320),
                    7: (384, 240, 30, 320),
                    8: (384, 240, 30, 320)
                }
            },
            Direction.LEFT:{
                CharacterState.MOVE_L:{
                    0: (375, 240, 30, 320),
                    1: (375, 240, 30, 320),
                    2: (375, 240, 30, 320),
                    3: (375, 240, 30, 320),
                    4: (375, 240, 30, 320),
                    5: (375, 240, 30, 320),
                    6: (375, 240, 30, 320),
                    7: (375, 240, 30, 320),
                    8: (375, 240, 30, 320),
                    9: (375, 240, 30, 320)
                },
                CharacterState.MOVE_R:{
                    0: (384, 240, 30, 320),
                    1: (384, 240, 30, 320),
                    2: (384, 240, 30, 320),
                    3: (384, 240, 30, 320),
                    4: (384, 240, 30, 320),
                    5: (384, 240, 30, 320),
                    6: (384, 240, 30, 320),
                    7: (384, 240, 30, 320),
                    8: (384, 240, 30, 320),
                    9: (384, 240, 30, 320)
                },
                CharacterState.STAND:{
                    0: (384, 240, 30, 320),
                    1: (384, 240, 30, 320),
                    2: (384, 240, 30, 320),
                    3: (384, 240, 30, 320),
                    4: (384, 240, 30, 320),
                    5: (384, 240, 30, 320),
                    6: (384, 240, 30, 320)
                },
                CharacterState.JUMP:{
                    0: (384, 240, 30, 300),
                    1: (384, 240, 30, 300),
                    2: (384, 240, 30, 300),
                    3: (384, 240, 30, 300),
                    4: (384, 240, 30, 300),
                    5: (384, 240, 30, 300),
                    6: (384, 240, 30, 300),
                    7: (384, 240, 30, 300),
                    8: (384, 240, 30, 300),
                    9: (384, 240, 30, 300),
                    10: (384, 240, 30, 300),
                    11: (384, 240, 30, 300)
                },
                CharacterState.SIT:{
                    0: (384, 370, 30, 200),
                    1: (384, 370, 30, 200)
                },
                CharacterState.BLOCK:{
                    0: (384, 240, 40, 320)
                },
                CharacterState.ATTACK1:{
                    0: (384, 240, 30, 320),
                    1: (384, 240, 30, 320),
                    2: (384, 240, 30, 320),
                    3: (384, 240, 30, 320),
                    4: (384, 240, 30, 320),
                    5: (384, 240, 30, 320),
                    6: (384, 240, 30, 320),
                    7: (384, 240, 30, 320)
                },
                CharacterState.ATTACK2:{
                    0: (384, 240, 30, 320),
                    1: (384, 240, 30, 320),
                    2: (384, 240, 30, 320),
                    3: (384, 240, 30, 320),
                    4: (384, 240, 30, 320),
                    5: (384, 240, 30, 320),
                    6: (384, 240, 30, 320),
                    7: (384, 240, 30, 320),
                    8: (384, 240, 30, 320)
                }
            }
        }
        self.hit_boxes = {
            Direction.RIGHT:{
                CharacterState.ATTACK1: {
                    0: (0, 0, 0, 0),
                    1: (0, 0, 0, 0),
                    2: (0, 0, 0, 0),
                    3: (470, 170, 170, 400),
                    4: (0, 0, 0, 0),
                    5: (0, 0, 0, 0),
                    6: (0, 0, 0, 0),
                    7: (0, 0, 0, 0)
                },
                CharacterState.ATTACK2: {
                    0: (0, 0, 0, 0),
                    1: (0, 0, 0, 0),
                    2: (300, 500, 40, 40),
                    3: (300, 450, 300, 100),
                    4: (0, 0, 0, 0),
                    5: (0, 0, 0, 0),
                    6: (0, 0, 0, 0),
                    7: (0, 0, 0, 0),
                    8: (0, 0, 0, 0)
                }
            },
            Direction.LEFT:{
                CharacterState.ATTACK1: {
                    0: (0, 0, 0, 0),
                    1: (0, 0, 0, 0),
                    2: (0, 0, 0, 0),
                    3: (140, 170, 170, 400),
                    4: (0, 0, 0, 0),
                    5: (0, 0, 0, 0),
                    6: (0, 0, 0, 0),
                    7: (0, 0, 0, 0)
                },
                CharacterState.ATTACK2: {
                    0: (0, 0, 0, 0),
                    1: (0, 0, 0, 0),
                    2: (230, 500, 40, 40),
                    3: (150, 450, 300, 100),
                    4: (0, 0, 0, 0),
                    5: (0, 0, 0, 0),
                    6: (0, 0, 0, 0),
                    7: (0, 0, 0, 0),
                    8: (0, 0, 0, 0)
                }
            }
        }
        sounds = {CharacterState.ATTACK1: 'music/ako/battle-cry.wav', CharacterState.STAND_HURT: 'music/ako/damage.wav'}
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