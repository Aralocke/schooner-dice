import enum
from typing import TypeAlias

Rolls: TypeAlias = list[int]


class Category(enum.Enum):
    Ones = 'ONES'
    Twos = 'TWOS'
    Threes = 'THREES'
    Fours = 'FOURS'
    Fives = 'FIVES'
    Sixes = 'SIXES'
    Sevens = 'SEVENS'
    Eights = 'EIGHTS'
    ThreeOfAKind = 'THREE_OF_A_KIND'
    FourOfAKind = 'FOUR_OF_A_KIND'
    FullHouse = 'FULL_HOUSE'
    SmallStraight = 'SMALL_STRAIGHT'
    AllDifferent = 'ALL_DIFFERENT'
    LargeStraight = 'LARGE_STRAIGHT'
    Schooner = 'SCHOONER'
    Chance = 'CHANCE'

    def __str__(self) -> str:
        return str(self.value)


def CategoryToValue(category: Category) -> [int, None]:
    """
    Match a Category to an integer value (1-8).

    :param category: Category enum value
    :return: numeric value if One through Eight inclusive or None
    """
    match category:
        case Category.Ones:
            return 1
        case Category.Twos:
            return 2
        case Category.Threes:
            return 3
        case Category.Fours:
            return 4
        case Category.Fives:
            return 5
        case Category.Sixes:
            return 6
        case Category.Sevens:
            return 7
        case Category.Eights:
            return 8
    return None


def ValueToCategory(value: int) -> [Category, None]:
    """
    Match an integer value to a category (1-8)

    :param value: Integer value
    :return: Category enum (Ones to Eights) or None
    """
    match value:
        case 1:
            return Category.Ones
        case 2:
            return Category.Twos
        case 3:
            return Category.Threes
        case 4:
            return Category.Fours
        case 5:
            return Category.Fives
        case 6:
            return Category.Sixes
        case 7:
            return Category.Sevens
        case 8:
            return Category.Eights
    return None


def IsFullHouse(values: dict, lhs: int, rhs: int) -> bool:
    """
    Predicate to check if the mapped values are a full house combination.

    :param values: Mapped roll values (see MapValues)
    :param lhs:
    :param rhs:
    :return:
    """
    if values[lhs] == 2 and values[rhs] == 3:
        return True
    if values[lhs] == 3 and values[rhs] == 2:
        return True
    return False


def CountSequence(rolls: Rolls, predicate: callable) -> int:
    """
    Iterate the rolls [1->N) passing the current value (rolls[i]) and the previous
    value (rolls[i - 1]) to a predicate to check if they are sequential values.

    :param rolls: list of integer rolls
    :param predicate: Callable type corresponding to `predicate(rolls[i], rolls[i - 1])`.
    :return: length of the detected sequence
    """
    if len(rolls) != 5:
        return 0

    length = 1
    index = 1
    while index < len(rolls):
        last = rolls[index - 1]
        curr = rolls[index]

        if predicate(last, curr):
            length = length + 1
        elif length < 3:
            length = 1

        index = index + 1

    return length


def _DecrementPredicate(a: int, b: int) -> bool:
    return b + 1 == a


def _IncrementPredicate(a: int, b: int) -> bool:
    return a + 1 == b


def IsLargeStraight(rolls: Rolls) -> bool:
    """
    Check if rolls is a large straight (sequential 5 values).

    :param rolls: list of integer rolls
    :return: boolean indicating if the rolls is a sequence of 5 or more
    """
    return (CountSequence(rolls, _IncrementPredicate) == 5
            or CountSequence(rolls, _DecrementPredicate) == 5)


def IsSmallStraight(rolls: Rolls) -> bool:
    """
    Check if rolls is a small straight (sequential 3 values).

    :param rolls: list of integer rolls
    :return: boolean indicating if the rolls is a sequence of 3 or more
    """
    return (CountSequence(rolls, _IncrementPredicate) >= 3
            or CountSequence(rolls, _DecrementPredicate) >= 3)


def MapValues(rolls: Rolls) -> dict:
    """
    Count duplicates in a list of rolls and map by value.

    :param rolls: list of integer rolls
    :return: dictionary of values and their occurence count
    """
    values = {}
    for r in rolls:
        if r not in values:
            values[r] = 1
        else:
            values[r] = values[r] + 1
    return values


def Score(category: Category, rolls: Rolls) -> int:
    """
    Score a list of rolls for a given category. This function does not evaluate
    if the rolls match the category or calculate a value.

    :param category: Category to calculate
    :param rolls: list of integer rolls
    :return: score for the given category and rolls
    """
    match category:
        case Category.ThreeOfAKind | Category.FourOfAKind | Category.Chance:
            return sum(rolls)
        case Category.FullHouse:
            return 25
        case Category.SmallStraight:
            return 30
        case Category.AllDifferent:
            return 35
        case Category.LargeStraight:
            return 40
        case Category.Schooner:
            return 50

    value = CategoryToValue(category)
    values = MapValues(rolls)

    if value in values and values[value] > 1:
        return value * values[value]

    return 0


def TopCategories(rolls: Rolls) -> list[Category]:
    """
    Determine the highest scoring category for a given set of rolls. This function
    will return a list of categories if there is a tie in the score.

    :param rolls: list of integer rolls
    :return: list of top scoring categories
    """
    results = []
    values = MapValues(rolls)

    duplicates = []
    for [value, count] in values.items():
        if count > 1:
            duplicates.append(value)

    if len(duplicates) == 0:
        # Account for: ALL_DIFFERENT
        results.append((Category.AllDifferent, Score(Category.AllDifferent, rolls)))
    else:
        for dup in duplicates:
            count = values[dup]
            # Account for: ONES, TWOS, THREES, FOURS, FIVES, SIXES, SEVENS, EIGHTS
            cat = ValueToCategory(dup)
            results.append((cat, Score(cat, rolls)))
            if count == 3:
                # Account for: THREE_OF_A_KIND
                results.append((Category.ThreeOfAKind, Score(Category.ThreeOfAKind, rolls)))
            if count == 4:
                # Account for: FOUR_OF_A_KIND
                results.append((Category.FourOfAKind, Score(Category.FourOfAKind, rolls)))
            if count == 5:
                # Account for: SCHOONER
                results.append((Category.Schooner, Score(Category.Schooner, rolls)))

        # Account for FULL_HOUSE
        if len(duplicates) == 2 and IsFullHouse(values, duplicates[0], duplicates[1]):
            results.append((Category.FullHouse, Score(Category.FullHouse, rolls)))

    # Account for SMALL_STRAIGHT (4-seq) and LARGE_STRAIGHT (5-seq)

    if IsSmallStraight(rolls):
        results.append((Category.SmallStraight, Score(Category.SmallStraight, rolls)))
    if IsLargeStraight(rolls):
        results.append((Category.LargeStraight, Score(Category.LargeStraight, rolls)))

    # Account for: CHANCE

    if results and len(duplicates) != 0:
        results.append((Category.Chance, Score(Category.Chance, rolls)))

    results.sort(key=lambda r: r[1], reverse=True)
    return [r[0] for r in results if r[1] == results[0][1]]
