from .kirito import Kirito
from .ako import Ako
from src.chars.character_type import CharacterType

class CharFactory:
    @staticmethod
    def get_char(char_type):
        char_mirror = {
            CharacterType.AKO: Ako("./images/characters/ako/"),
            CharacterType.KIRITO: Kirito("./images/characters/kirito/")
        }
        return char_mirror[char_type]