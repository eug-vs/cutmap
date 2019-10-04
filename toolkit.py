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
    def __init__(self, *args):
        if args:
            assert len(args) == 2, "Wrong args"
            self.x = args[0]
            self.y = args[1]
        else:
            self.x = 0
            self.y = 0

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f'({self.x}, {self.y})'


class Slice:
    def __init__(self, point, direction):
        self.point = point
        self.direction = direction

    def __str__(self):
        return f'Slice at {self.point} in {self.direction} direction.'

    def __repr__(self):
        return str(self)


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


def f_vertical(x, D, C):
    """
    This is the same as function f(x, D), but it assumes that the first
    guillotine cut is vertical.
    """
    minimum = None
    slices = None
    for D1, D2 in R(D):
        for z in range(int(x/2)+1):
            left, l_slices = f(z, D1, C)
            point = C + Vector(z, 0)
            right, r_slices = f(x - z, D2, point)
            m = max(left, right)
            if not minimum or m < minimum:
                minimum = m
                slices = l_slices
                slices.append(Slice(point, 'vertical'))
                slices += r_slices
    return minimum, slices


def f_horizontal(x, D, C):
    """
    This is the same as function f(x, D), but it assumes that the first
    guillotine cut is horizontal.
    """
    minimum = None
    slices = None
    for D1, D2 in R(D):
        bottom, b_slices = f(x, D1, C)
        point = C + Vector(0, bottom)
        top, t_slices = f(x, D2, point)
        m = bottom + top
        if not minimum or m < minimum:
            minimum = m
            slices = b_slices
            slices.append(Slice(point, 'horizontal'))
            slices += t_slices
    return minimum, slices


def f(x, D, C):
    """
    :param x: Width of the strip.
    :param D: Collection of Details.
    :param C: Vector object - left-bottom point of the strip.
    :return: Minimum height (y) of the strip of width x, which is enough
    for guillotine allocation for collection D.
    """
    max_b = 0
    for detail in D:
        if detail.b > max_b:
            max_b = detail.b
    if max_b > x:
        return 100000, []
    elif len(D) == 1:
        slices = []
        if D[0].a <= x:
            if D[0].a < x:
                #slices.append(Slice(C + Vector(D[0].a, 0), 'vertical'))
                pass
            #slices.append(Slice(C + Vector(0, D[0].b), 'horizontal'))
            return D[0].b, slices
        else:
            if D[0].b < x:
                #slices.append(Slice(C + Vector(D[0].b, 0), 'vertical'))
                pass
            #slices.append(Slice(C + Vector(0, D[0].a), 'horizontal'))
            return D[0].a, slices
    else:
        vertical, v_slices = f_vertical(x, D, C)
        horizontal, h_slices = f_horizontal(x, D, C)
        # Finding minimum
        if vertical < horizontal:
            return vertical, v_slices
        else:
            return horizontal, h_slices


GAF = table_repr(f)
