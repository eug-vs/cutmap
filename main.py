from toolkit import *

type1 = [Detail(3, 5)] * 2
type2 = [Detail(2, 4)] * 2
D = [type1, type2]
print(D)
print(flatten(D))
for d in R(D):
    print(d)
