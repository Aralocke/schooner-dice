import argparse
import itertools
import os
from os.path import exists, join, realpath
import sys


rootPath = realpath(join(__file__, os.pardir))
if exists(join(rootPath, 'lib')):
    sys.path.insert(0, join(rootPath, 'lib'))


from schooner.dice import ExplicitRoll
from schooner.scoring import Category, TopCategories


def BruteSingleCategory(args: argparse.Namespace) -> bool:
    """

    :param args:
    :return:
    """
    count = 0
    gen = itertools.product(range(1, 8), repeat=args.rolls)
    for values in gen:
        values = [int(r.value) for r in ExplicitRoll(values)]
        categories = TopCategories(values)

        if args.category in categories:
            print('{} => {}'.format(values, [str(c) for c in categories]))
            if count >= args.count:
                break
            count = count + 1

    if count == 0:
        print('Failed to brute force a combination for category: {}'.format(args.category))

    return count > 0


def BruteAllCategories(args: argparse.Namespace) -> bool:
    """

    :param args:
    :return:
    """
    categories = {}
    gen = itertools.product(range(1, 9), repeat=args.rolls)

    for values in gen:
        values = [int(r.value) for r in ExplicitRoll(values)]
        results = TopCategories(values)

        for category in results:
            if category not in categories:
                categories[category] = list()
            categories[category].append(values)

    print('Discovered \'{}\' category permutations for \'{}\' rolls'.format(
        len(categories), args.rolls))

    count = 0
    for cat, values in categories.items():
        print('{} ({}) => {}'.format(
            cat,
            len(values),
            values[0 : min(args.count, len(values))]))
        count = count + len(values)

    print('Total possibilities: {}'.format(count))

    return True


def Main(args: argparse.Namespace) -> bool:
    if args.command == 'brute-category':
        return BruteSingleCategory(args)
    elif args.command == 'brute-all':
        return BruteAllCategories(args)

    return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser('schooner-cli')
    cmds = parser.add_subparsers(dest='command',
                                 help='Sub commands available to run')

    def BruteCommand(par, name: str, **kwargs):
        cmd = par.add_parser(name, **kwargs)
        cmd.add_argument('--rolls', '-r', default=5, type=int,
                         help='Number of rolls to generate for each combination')
        cmd.add_argument('--count', '-c', type=int, default=10,
                         help='Number of results to count before exiting')
        return cmd

    # Sub commands available on the parser

    #
    # Brute force a specific category
    #
    bruteCat = BruteCommand(cmds, 'brute-category',
                            help='attempt to brute force a combination of rolls to generate a specific result')
    bruteCat.add_argument('category', type=Category, choices=list(Category),
                          help='Category to try to brute force')

    #
    # Brute force all possible values and return an example of each category
    #
    bruteAllCats = BruteCommand(cmds, 'brute-all',
                                help='Brute force an example of every possible category')

    args = parser.parse_args()
    if not Main(args):
        sys.exit(1)
