from chars.character import CharacterState, Direction
from dataclasses import dataclass

@dataclass
class CharInfo:
    rect_x: int
    rect_y: int
    image_counter: int
    state: CharacterState
    direction: Direction