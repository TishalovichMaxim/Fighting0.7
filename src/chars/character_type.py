from enum import Enum

class CharacterType(Enum):
    KIRITO = 0
    AKO = 1

if __name__ == "__main__":
    a = 1
    a = CharacterType(1)
    print(a)