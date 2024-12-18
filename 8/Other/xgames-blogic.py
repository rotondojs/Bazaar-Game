import asyncio
import json
import sys

import ijson
import argparse

from Bazaar.Common.JSON.deserializer import BazaarDeserializer
from Bazaar.Common.scoring import ScoringType
from Bazaar.Referee.observer import Observer
from Bazaar.Referee.referee import Referee


def read_json():
    parser = ijson.items(sys.stdin.buffer, "", buf_size=1, multiple_values=True)

    return next(parser), next(parser), next(parser)


class BazaarSerializer:
    @staticmethod
    def serialize(winner: list[str], misbehaved: list[str]) -> tuple[str, str]:
        return json.dumps(sorted(winner)), json.dumps(sorted(misbehaved))


def main() -> None:
    parsed = read_json()
    mechanisms, _, game_state = BazaarDeserializer.m8_entry(*parsed)
    parser = argparse.ArgumentParser()
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()

    if args.show:
        referee = Referee(mechanisms, game_state, [Observer(game_state)])
    else:
        referee = Referee(mechanisms, ScoringType.NORMAL, game_state)

    winner, misbehaved = BazaarSerializer.serialize(*asyncio.run(referee.play()))

    print(json.dumps([winner, misbehaved]))


if __name__ == "__main__":
    main()
