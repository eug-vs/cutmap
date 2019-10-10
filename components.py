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
        if isinstance(other, int):
            return [self] * other
        elif isinstance(other, bool):
            return [self] if other else []

    def validate(self, width):
        return self.b <= width

    def area(self):
        return self.a * self.b


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

    def index_area(self, index):
        key = self.validate_index(index)
        details = np.dot(self.t, key)
        area = 0
        for detail in details:
            area += detail.area()
        return area

    def index_sizes(self, index, x):
        key = self.validate_index(index)
        details = np.dot(self.t, key)
        sizes = []
        for detail in details:
            if detail.a <= x / 2:
                sizes.append(detail.a)
            if detail.b <= x / 2:
                sizes.append(detail.b)
        sizes = np.unique(sizes)
        return sizes

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

    def __str__(self):
        return f'Detail kit:\n\tDetail types: {self.t}\n\tQuantities:   {self.q}'
