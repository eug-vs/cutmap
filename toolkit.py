import itertools
import numpy as np


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

    def __mul__(self, other):
        if type(other) is int:
            return [self] * other
        elif type(other) is bool:
            return [self] if other else []

    def validate(self, x):
        return self.b <= x


class Kit:
    def __init__(self, d):
        types = []
        for dtype in d:
            if dtype not in types:
                types.append(dtype)
        self.n = len(d)
        self.t = np.array(types)
        self.q = np.array([d.count(dtype) for dtype in types])

        # Building pick-map
        unit_matrix = np.identity(len(self.t), dtype=int)
        self.map = np.zeros((1, len(self.t)), dtype=int)
        last_pos = 0
        size = 1
        for sum_block in range(1, self.n):
            last_block = self.map[last_pos:]
            last_pos = len(self.map)
            for unit_row in unit_matrix:
                for row in last_block:
                    new_row = row + unit_row
                    if np.all(new_row <= self.q):
                        self.map = np.vstack([self.map, new_row])
        unique_idx = np.unique(self.map, axis=0, return_index=True)[1]
        self.map = self.map[np.sort(unique_idx)]
        self.map = np.vstack([self.map, self.q])

    def validate_index(self, index):
        if index not in self.map or np.all(index == 0):
            index = self.q - index
        return index

    def iterate(self, index):
        key = self.validate_index(index)
        lower_half = self.map[:int(len(self.map) / 2)]
        for row in lower_half:
            if np.any(row):
                if np.any(row - key) and np.any(self.q - row - key):
                    if np.all(row <= key):
                        yield row, key - row

    def validate_detail(self, index, x):
        key = self.validate_index(index)
        uniques = key != 0
        types = np.dot(self.t, uniques)
        for dtype in types:
            if not dtype.validate(x):
                return False
        return True

    def is_single(self, index):
        key = self.validate_index(index)
        total = 0
        for item in key:
            total += item
        if total != 1:
            return False
        return np.dot(self.t, key)

    def flat(self):
        return np.dot(self.t, self.q)

    def __str__(self):
        return self.flat()


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


class Instruction:
    def __init__(self, slice, first, second):
        """
        Slice is a number which represents an offset of the slice.
        It is positive in horizontal case and negative in vertical.
        If slice == 0, no slice needed.
        """
        self.slice = slice
        self.first = first
        self.second = second

    def slice2str(self, slice):
        direction = 'Horizontal' if slice > 0 else 'Vertical'
        return f'{direction} slice at {abs(slice)}'

    def report(self, level=0):
        tab = ' ' * 6
        if self.slice:
            dir1, dir2 = ('Bottom', 'Up') if self.slice > 0 else ('Left', 'Right')
            print(tab * level + self.slice2str(self.slice))

            print(tab * (level + 1) + dir1 + ' part:')
            self.first.report(level=level+2)

            print(tab * (level + 1) + dir2 + ' part:')
            self.second.report(level=level+2)
        else:
            print(tab * level + 'It is a detail!')
            print(tab * level + self.slice2str(self.first))
            print(tab * level + self.slice2str(self.second))


def f_vertical(x, kit, index, C):
    """
    This is the same as function f(x, D), but it assumes that the first
    guillotine cut is vertical.
    """
    minimum = None
    slices = None
    for D1, D2 in kit.iterate(index):
        for z in range(int(x/2)+1):
            left, l_slices = f(z, kit, D1, C)
            point = C + Vector(z, 0)
            right, r_slices = f(x - z, kit, D2, point)
            m = max(left, right)
            if not minimum or m < minimum:
                minimum = m
                slices = Instruction(-z, l_slices, r_slices)
    return minimum, slices


def f_horizontal(x, kit, index, C):
    """
    This is the same as function f(x, D), but it assumes that the first
    guillotine cut is horizontal.
    """
    minimum = None
    slices = None
    for D1, D2 in kit.iterate(index):
        bottom, b_slices = f(x, kit, D1, C)
        point = C + Vector(0, bottom)
        top, t_slices = f(x, kit, D2, point)
        m = bottom + top
        if not minimum or m < minimum:
            minimum = m
            slices = Instruction(bottom, b_slices, t_slices)
    return minimum, slices


def f(x, kit, index, C):
    """
    :param x: Width of the strip.
    :param D: Collection of Details.
    :param C: Vector object - left-bottom point of the strip.
    :return: Minimum height (y) of the strip of width x, which is enough
    for guillotine allocation for collection D.
    """
    if not kit.validate_detail(index, x):
        return 100000, Instruction(None, None, None)
    single = kit.is_single(index)
    if single:
        single = single[0]
        if single.a <= x:
            first = -single.a
            second = single.b
            slices = Instruction(None, first, second)
            return single.b, slices
        else:
            first = single.b
            second = -single.a
            slices = Instruction(None, first, second)
            return single.a, slices
    else:
        vertical, v_slices = f_vertical(x, kit, index, C)
        horizontal, h_slices = f_horizontal(x, kit, index, C)
        # Finding minimum
        if vertical < horizontal:
            return vertical, v_slices
        else:
            return horizontal, h_slices
