from chars.kirito import Kirito
from chars.ako import Ako
from chars.charater_type import CharacterType

class CharFactory:
    @staticmethod
    def get_char(char_type):
        char_mirror = {
            CharacterType.AKO: Ako("./images/characters/ako/"),
            CharacterType.KIRITO: Kirito("./images/characters/kirito/")
        }
        return char_mirror[char_type]