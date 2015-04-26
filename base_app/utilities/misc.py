__author__ = 'Michael Redmond'

import sys
import os


def new_name(names, prefix='Document'):
    i = len(names) + 1

    _first_name = '%s%d' % (prefix, i)

    if _first_name in names:
        i = 1
        while True:
            _name = '%s(%d)' % (_first_name, i)

            if _name not in names:
                _first_name = _name
                break

    return _first_name


def get_path():
    if hasattr(sys, "frozen"):
        main_dir = os.path.dirname(sys.executable)
        full_real_path = os.path.realpath(sys.executable)
    else:
        script_dir = os.path.dirname(__file__)
        main_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
        full_real_path = os.path.realpath(sys.argv[0])

    return main_dir