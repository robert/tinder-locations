from utils import _distance

# [200~40.59.36 73.22.36 73.21.40[201~
h1 = 73
m1 = 22
s1 = 36

h2 = 73
m2 = 21
s2 = 40

hh = 40
mm = 59
ss = 36


def conv(h, m, s):
    return h + m/60.0 + s/3600.0

l1 = (conv(hh, mm, ss), conv(h1, m1, s1))
l2 = (conv(hh, mm, ss), conv(h2, m2, s2))

print _distance(l1, l2)
