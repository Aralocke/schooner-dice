import os
from os.path import exists, join, realpath
import sys


rootPath = realpath(join(__file__, os.pardir, os.pardir))
if exists(join(rootPath, 'lib')):
    sys.path.insert(0, join(rootPath, 'lib'))

from test_dice_rolls import run_roll_tests
from test_dice_score import run_score_tests


if __name__ == '__main__':
    print('Running tests ...git add cli ')

    try:
        run_roll_tests()
        run_score_tests()
    except AssertionError as e:
        print('Assertion failed')
        raise e
    except Exception as e:
        print('Unexpected exception: {}'.format(e))
        raise e
    else:
        print('All tests completed successfully')
