from toolkit import *

type11 = [Detail(1, 1)]
type21 = [Detail(2, 1)]
type31 = [Detail(3, 1)]
type41 = [Detail(4, 1)]

type22 = [Detail(2, 2)]
type32 = [Detail(3, 2)]
type42 = [Detail(4, 2)]

type33 = [Detail(3, 3)]
type43 = [Detail(4, 3)]

type44 = [Detail(4, 4)]


D = type31 * 2 + type21 + type22 + type32


length, instruction = f(4, D, Vector())
instruction.report()
