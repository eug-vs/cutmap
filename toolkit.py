import itertools


class Detail:
    def __init__(self, width, height):
        if width > height:
            self.w = width
            self.h = height
        else:
            self.w = height
            self.h = width

    def __str__(self):
        return f'({self.w} x {self.h})'

    def __repr__(self):
        return str(self)


def flatten(D):
    """
    :param D: Collection of unique types. Type is a list of identical Details.
    :return: Generator of all Details.
    """
    result = []
    for type in D:
        for detail in type:
            result.append(detail)
    return result


def diff(lst, sub):
    """
    :param lst: List
    :param sub: It's sublist
    :return: Their exact difference
    """
    result = []
    for i in lst:
        if i not in result:
            for j in range(lst.count(i) - sub.count(i)):
                result.append(i)
    return result


def R(D):
    """
    :param D: Collection of unique types. Type is a list of identical Details.
    :return: Generator of all possible splits into 2 sub-collections.
    """
    flat = flatten(D)
    for left_size in range(1, int(len(flat) / 2) + 1):
        for i in itertools.combinations(flat, left_size):
            yield i, diff(flat, i)


def f_vertical(x, D):
    """
    This is the same as function f(x, D), but it assumes that the first
    guillotine cut is vertical.
    """
    pass


def f_horizontal(x, D):
    """
    This is the same as function f(x, D), but it assumes that the first
    guillotine cut is horizontal.
    """
    pass


def f(x, D):
    """
    :param x: Width of the strip.
    :param D: Collection of unique types. Type is a list of identical Details.
    :return: Minimum height (y) of the strip of width x, which is enough
    for guillotine allocation for collection D.
    """

    # If collection D has exactly one Detail, return its height
    if len(D) == 1 and len(D[0]) == 1:
        return D[0][0].height
    else:
        return min(f_vertical(x, D), f_horizontal(x, D))
