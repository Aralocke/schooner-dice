from schooner.scoring import Category, Score, TopCategories


def DeepCompare(results: list[Category], cmp: list[Category]) -> bool:
    """
    Ensure that the list of given result Categories exists within the list of expected
    result Categories.

    :param results: list of result categories
    :param cmp: list of categories to compare against
    :return: True if each result exists in the compareable list
    """
    if len(results) != len(cmp):
        return False
    for result in results:
        if result not in cmp:
            return False
    return True


def test_given_samples():
    """
    These are the given examples in the project documentation

    :return:
    """
    score = Score(Category.FullHouse, [1, 1, 1, 7, 7])  # Given Example
    assert score == 25

    results = TopCategories([3, 3, 3, 6, 7])
    assert DeepCompare(results, [Category.ThreeOfAKind, Category.Chance])


def test_scoring_sums():
    """
    Test for scorable cases which result in a full sum of the provided rolls.

    :return:
    """
    assert Score(Category.ThreeOfAKind, [1, 1, 1, 2, 3]) == 8
    assert Score(Category.FourOfAKind, [1, 1, 1, 1, 2]) == 6
    assert Score(Category.Chance, [1, 8, 2, 7, 3]) == 21


def test_scoring_explicit_values():
    """
    Test for the known explicit provided scores for the provided rolls.

    :return:
    """
    assert Score(Category.FullHouse, [1, 1, 1, 2, 2]) == 25
    assert Score(Category.SmallStraight, [1, 2, 3, 4, 8]) == 30
    assert Score(Category.LargeStraight, [1, 2, 3, 4, 5]) == 40
    assert Score(Category.AllDifferent, [1, 8, 2, 7, 3]) == 35
    assert Score(Category.Schooner, [1, 1, 1, 1, 1]) == 50


def test_scoring_any_combination():
    """
    Test for the pair combinations for the provided rolls

    :return:
    """
    assert Score(Category.Ones, [1, 1, 3, 5, 7]) == 2
    assert Score(Category.Eights, [8, 8, 7, 5, 4]) == 16


def test_scoring():
    """
    Alias to run all scoring tests

    :return:
    """
    test_scoring_sums()
    test_scoring_explicit_values()
    test_scoring_any_combination()


def test_categories():
    """
    Test calculating the TopCategories for the given rolls.

    :return:
    """
    results = TopCategories([1, 2, 7, 4, 6])
    assert DeepCompare(results, [Category.AllDifferent])

    results = TopCategories([7, 7, 7, 7, 7])
    assert DeepCompare(results, [Category.Schooner])

    results = TopCategories([1, 1, 1, 1, 2])
    assert DeepCompare(results, [Category.FourOfAKind, Category.Chance])

    results = TopCategories([1, 2, 3, 4, 4])
    assert DeepCompare(results, [Category.SmallStraight])

    results = TopCategories([1, 1, 2, 3, 4])
    assert DeepCompare(results, [Category.SmallStraight])

    results = TopCategories([1, 2, 3, 4, 5])
    assert DeepCompare(results, [Category.LargeStraight])


def test_reverse_straights():
    """
    Test to ensure we handle decreasing sequences for small and large straights

    :return:
    """
    results = TopCategories([4, 4, 3, 2, 1])
    assert DeepCompare(results, [Category.SmallStraight])

    results = TopCategories([4, 3, 2, 1, 1])
    assert DeepCompare(results, [Category.SmallStraight])

    results = TopCategories([5, 4, 3, 2, 1])
    assert DeepCompare(results, [Category.LargeStraight])


def run_score_tests():
    print('Running score tests ...')

    # The following are the only scorable categories we can verify given the example
    # scorebook. We have tests for each category.

    # Given 5 rolls of an 8-sided dice (1-8 inclusive) the following is the possibility
    # table for a complete brute forcing of the probable options.
    #
    # SCHOONER (8)
    # FOUR_OF_A_KIND (280)
    # CHANCE (25706)
    # FULL_HOUSE (350)
    # THREE_OF_A_KIND (3590)
    # LARGE_STRAIGHT (8)
    # ALL_DIFFERENT (6712)
    # SMALL_STRAIGHT (4)

    test_given_samples()
    test_scoring()
    test_categories()
    test_reverse_straights()

    print('All score tests completed successfully')


if __name__ == '__main__':
    run_score_tests()
