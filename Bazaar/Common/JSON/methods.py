from enum import StrEnum


class Methods(StrEnum):
    SETUP = "setup"
    REQUEST_P_OR_T = "request-pebble-or-trades"
    REQUEST_CARDS = "request-cards"
    WIN = "win"
