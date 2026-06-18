from enum import Enum

class ActionType(Enum):

    MOVE = "MOVE"

    EAT = "EAT"

    REPRODUCE = "REPRODUCE"

    EXPLORE = "EXPLORE"

    SEARCH_FOOD = "SEARCH_FOOD"

    ESCAPE = "ESCAPE"