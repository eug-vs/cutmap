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


def Num(d1, d2):
    return 0


class Entry:
    def __init__(self, x, y, r, N):
        self.x = x
        self.y = y
        self.r = r
        self.N = N

    def __str__(self):
        return f'{self.x} {self.y} {self.r} {self.N}'


class EGAF:
    def __init__(self, D, entries):
        self.D = D
        self.entries = entries

    def n(self):
        return len(self.entries)

    def __getitem__(self, item):
        return self.entries[item]

    def __setitem__(self, key, value):
        self.entries[key] = value
        return value

    def add_entry(self, entry):
        self.entries.append(entry)


class Operator:
    def __init__(self, EGAF1, EGAF2):
        self.f1 = EGAF1
        self.f2 = EGAF2
        self.f = EGAF([], [])
        self.n1, self.n2 = self.f1.n(), self.f2.n()
        self.i1, self.i2, self.i = 1, 1, 1

    def sum(self):
        while self.c1() or self.c2() or self.c3() or self.c4():
            if self.c1() and self.c2():
                if self.c5():
                    self.a1()
                else:
                    if self.c6():
                        self.a2()
                    else:
                        self.a3()
            if self.c1() and not self.c2():
                if self.c4():
                    if self.c5():
                        self.a4()
                    else:
                        if self.c6():
                            self.a2()
                        else:
                            self.a3()
                else:
                    self.a4()
            if not self.c1() and self.c2():
                if self.c3():
                    if self.c5():
                        self.a1()
                    else:
                        if self.c6():
                            self.a5()
                        else:
                            self.a3()
                else:
                    self.a5()
            else:
                if self.c3() and self.c4():
                    if self.c5():
                        self.a4()
                    else:
                        if self.c6():
                            self.a5()
                        else:
                            self.a3()
                elif self.c3() and not self.c4():
                    self.a4()
                elif not self.c3() and self.c4():
                    self.a5()

    def minimum(self):
        while self.c3() or self.c4():
            if self.c3() and self.c4():
                if self.c5():
                    if self.c8():
                        self.b1()
                    else:
                        self.b2()
                else:
                    if self.c6():
                        if self.c7():
                            self.b3()
                        else:
                            self.b4()
                    else:
                        if self.c7():
                            self.b2()
                        else:
                            if self.c8():
                                self.b4()
                            else:
                                self.b5()
            else:
                if self.c3():
                    self.b1()
                elif self.c4():
                    self.b2()

    def c1(self):
        return self.i1 == 1

    def c2(self):
        return self.i2 == 1

    def c3(self):
        return self.i1 <= self.n1

    def c4(self):
        return self.i2 <= self.n2

    def c5(self):
        return self.f1[self.i1].x < self.f2[self.i2].x

    def c6(self):
        return self.f1[self.i1].x > self.f2[self.i2].x

    def c7(self):
        return self.f1[self.i1].y < self.f2[self.i2].y

    def c8(self):
        return self.f1[self.i1].y > self.f2[self.i2].y

    def a1(self):
        self.i1 += 1

    def a2(self):
        self.i2 += 1

    def a3(self):
        self.f[self.i].x = self.f1[self.i1].x
        self.f[self.i].y = self.f1[self.i1].y + self.f2[self.i2].y
        self.f[self.i].r = self.f1[self.i1].y
        self.f[self.i].N = Num(self.f1.D, self.f2.D)  # ????
        self.i1 += 1
        self.i2 += 1
        self.i += 1

    def a4(self):
        self.f[self.i].x = self.f1[self.i1].x
        self.f[self.i].y = self.f1[self.i1].y + self.f2[self.i2 - 1].y
        self.f[self.i].r = self.f1[self.i1].y
        self.f[self.i].N = Num(self.f1.D, self.f2.D)  # ????
        self.i1 += 1
        self.i += 1

    def a5(self):
        self.f[self.i].x = self.f2[self.i2].x
        self.f[self.i].y = self.f1[self.i1 - 1].y + self.f2[self.i2].y
        self.f[self.i].r = self.f1[self.i1 - 1].y
        self.f[self.i].N = Num(self.f1.D, self.f2.D)  # ????
        self.i2 += 1
        self.i += 1

    def b1(self):
        self.f[self.i].x = self.f1[self.i1].x
        self.f[self.i].y = self.f1[self.i1].y
        self.f[self.i].r = self.f1[self.i1].r
        self.f[self.i].N = self.f1[self.i1].N
        self.i += 1
        self.i1 += 1

    def b2(self):
        self.f[self.i].x = self.f1[self.i1].x
        self.f[self.i].y = self.f1[self.i1].y
        self.f[self.i].r = self.f1[self.i1].r
        self.f[self.i].N = self.f1[self.i1].N
        self.i += 1
        self.i1 += 1
        maximum = 0
        for k in range(self.n2):
            if self.f2[k].y >= self.f[self.i].y:
                maximum = k
        self.i2 = maximum + 1

    def b3(self):
        self.f[self.i].x = self.f2[self.i2].x
        self.f[self.i].y = self.f2[self.i2].y
        self.f[self.i].r = self.f2[self.i2].r
        self.f[self.i].N = self.f2[self.i2].N
        self.i += 1
        self.i2 += 1

    def b4(self):
        self.f[self.i].x = self.f2[self.i2].x
        self.f[self.i].y = self.f2[self.i2].y
        self.f[self.i].r = self.f2[self.i2].r
        self.f[self.i].N = self.f2[self.i2].N
        self.i += 1
        self.i2 += 1
        maximum = 0
        for k in range(self.n1):
            if self.f1[k].y >= self.f[self.i].y:
                maximum = k
        self.i1 = maximum + 1

    def b5(self):
        self.b1()
        self.i2 += 1
