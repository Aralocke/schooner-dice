import random


class Dice(object):

    def __init__(self, value: int = None):
        self. value = value or random.randint(1, 8)

    def __repr__(self) -> str:
        return '<Dice: {}>'.format(self.value)


def RandomRoll(count: int = 5) -> list[Dice]:
    """
    Generate a dice roll of the given count of a default of 5.

    :param count: int for the number of Dice values
    :return: list of dice rolls
    """
    rolls = []
    for _ in range(count):
        rolls.append(Dice())
    return rolls


def ExplicitRoll(rolls: list[int]) -> list[Dice]:
    """
    Convert a list of rolls into a list of Dice rolls

    :param rolls: list of roll values
    :return: list of Dice rolls equal in len(rolls)
    """
    return [Dice(n) for n in rolls]

