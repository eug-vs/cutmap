from time import time
from components import Kit


class Vector:
    def __init__(self, *args):
        if args:
            assert len(args) == 2, 'Wrong args'
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
    def __init__(self, cut, first, second):
        """
        Cut is a number which represents an offset of the cut.
        It is positive in horizontal case and negative in vertical.
        If cut == 0, no cut needed.
        """
        self.cut = cut
        self.first = first
        self.second = second

    def cut2str(self, cut):
        direction = 'Horizontal' if cut > 0 else 'Vertical'
        return f'{direction} cut at {abs(cut)}'

    def report(self, level=0):
        if not level:
            print('Cutting map:')
        tab = ' ' * 6
        if self.cut:
            dir1, dir2 = ('Bottom', 'Upper') if self.cut > 0 else ('Left', 'Right')
            print(tab * (level + 1) + self.cut2str(self.cut))

            print(tab * (level + 2) + dir1 + ' section:')
            self.first.report(level=level+2)

            print(tab * (level + 2) + dir2 + ' section:')
            self.second.report(level=level+2)
        else:
            print(tab * (level + 1) + 'It is a detail!')
            print(tab * (level + 1) + self.cut2str(self.first))
            print(tab * (level + 1) + self.cut2str(self.second))


def f_vertical(w, kit, index, point):
    """
    This is the same as f(w, kit, index, point), but it assumes that the first
    guillotine cut is vertical.
    """
    minimum = None
    cuts = None
    for d1, d2 in kit.iterate(index):
        if minimum and (kit.index_area(d1) > minimum * w or kit.index_area(d2) > minimum * w):
            continue
        for z in kit.index_sizes(index, w):
            left, l_cuts = f(z, kit, d1, point)
            if minimum and left >= minimum:
                continue
            new_point = point + Vector(z, 0)
            right, r_cuts = f(w - z, kit, d2, new_point)
            m = max(left, right)
            if not minimum or m < minimum:
                minimum = m
                cuts = Instruction(-z, l_cuts, r_cuts)
            if minimum and minimum == kit.index_area(index):
                break
    if not minimum:
        return 100000, Instruction(None, None, None)
    return minimum, cuts


def f_horizontal(w, kit, index, point):
    """
    This is the same as f(w, kit, index, point), but it assumes that the first
    guillotine cut is horizontal.
    """
    minimum = None
    cuts = None
    for d1, d2 in kit.iterate(index):
        bottom, b_cuts = f(w, kit, d1, point)
        if minimum and bottom >= minimum:
            continue
        new_point = point + Vector(0, bottom)
        top, t_cuts = f(w, kit, d2, new_point)
        m = bottom + top
        if not minimum or m < minimum:
            minimum = m
            cuts = Instruction(bottom, b_cuts, t_cuts)
        if minimum and minimum == kit.index_area(index):
            break
    return minimum, cuts


def f(w, kit, index=0, point=Vector(0, 0)):
    """
    :param w: Width of the roll.
    :param kit: Kit object that stores information about details.
    :param index: Index of a subset in a kit.
    :param point: Vector object - coordinate of left-bottom point on the roll.
    :return: Minimum height of the roll of given width, which is enough for
    guillotine allocation of detail collection, linked to a detail subset by index.
    """
    if not kit.validate_detail(index, w):
        return 100000, Instruction(None, None, None)
    single = kit.is_single(index)
    if single:
        if single.a <= w:
            first = -single.a
            second = single.b
            cuts = Instruction(None, first, second)
            return single.b, cuts
        else:
            first = single.b
            second = -single.a
            cuts = Instruction(None, first, second)
            return single.a, cuts
    else:
        vertical, v_cuts = f_vertical(w, kit, index, point)
        if vertical * w == kit.index_area(index):
            return vertical, v_cuts
        horizontal, h_cuts = f_horizontal(w, kit, index, point)
        if vertical < horizontal:
            return vertical, v_cuts
        else:
            return horizontal, h_cuts


def process(width, details):
    """Solve the Guillotine problem and generate report"""
    k = Kit(details)
    print(k)
    t = time()
    length, instruction = f(width, k)
    instruction.report()
    print(f'{k.n} details successfully packed in {time() - t} seconds. \nTotal roll length: {length}.')
