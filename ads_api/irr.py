import sys

from services import PATH_TO_DJANGO


sys.path.append(PATH_TO_DJANGO)
from core import Core

if __name__ == '__main__':
    test = Core(2, [2, 4, 5, 7], '', 5)
    test.start()
