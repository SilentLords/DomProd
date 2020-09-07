import sys
DEBUG = False
if DEBUG:
    PATH_TO_DJANGO = '/Users/nikitatonkoskurov/PycharmProjects/domofound2/'
else:
    PATH_TO_DJANGO = '/var/www/dom/src/'
sys.path.append(PATH_TO_DJANGO)
from core import Core

if __name__ == '__main__':
    test = Core(7, [2, 4, 5, 7], '', 5)
    test.start()
