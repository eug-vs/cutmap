import itertools
import numpy


class Detail:
    def __init__(self, a, b):
        if a > b:
            self.a = a
            self.b = b
        else:
            self.a = b
            self.b = a

    def __str__(self):
        return f'({self.a} x {self.b})'

    def __repr__(self):
        return str(self)


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

        
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
    :param D: Collection of Details.
    :return: Generator of all possible splits into 2 sub-collections.
    """
    for left_size in range(1, int(len(D) / 2) + 1):
        for i in itertools.combinations(D, left_size):
            yield i, diff(D, i)


def table_repr(func):
    """
    Wraps the function so it's evaluated at every X point and
    represented as a stair-step function as a numpy-table.
    """
    def wrapper(D):
        table = numpy.array([[], []], dtype='int')
        maximum = 0
        max_b = 0
        for detail in D:
            maximum += detail.a
            if detail.b > max_b:
                max_b = detail.b
        for x in range(max_b, maximum):
            result = func(x, D)
            if table.size:
                last_column = table[:, len(table[0])-1]
            if not table.size or result != last_column[1]:
                column = numpy.array([[x], [result]])
                table = numpy.append(table, column, axis=1)
            if result == max_b:
                return table
    return wrapper


def f_vertical(x, D):
    """
    This is the same as function f(x, D), but it assumes that the first
    guillotine cut is vertical.
    """
    minimum = None
    for D1, D2 in R(D):
        for z in range(int(x/2)+1):
            m = max(f(z, D1), f(x - z, D2))
            if not minimum or m < minimum:
                minimum = m
    return minimum


def f_horizontal(x, D):
    """
    This is the same as function f(x, D), but it assumes that the first
    guillotine cut is horizontal.
    """
    minimum = None
    for D1, D2 in R(D):
        m = f(x, D1) + f(x, D2)
        if not minimum or m < minimum:
            minimum = m
    return minimum


def f(x, D):
    """
    :param x: Width of the strip.
    :param D: Collection of Details.
    :return: Minimum height (y) of the strip of width x, which is enough
    for guillotine allocation for collection D.
    """
    max_b = 0
    for detail in D:
        if detail.b > max_b:
            max_b = detail.b
    if max_b > x:
        return 100000
    elif len(D) == 1:
        if D[0].a <= x:
            return D[0].b
        else:
            return D[0].a
    else:
        return min(f_vertical(x, D), f_horizontal(x, D))


GAF = table_repr(f)
