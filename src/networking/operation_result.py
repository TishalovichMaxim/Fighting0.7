from enum import Enum, auto

class OperationResult(Enum):
    GAME_PREPARED = auto()
    GAME_FAILED = auto()