__author__ = 'Michael Redmond'


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