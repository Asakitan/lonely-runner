"""Exact interval certificate for the six-speed lonely-runner slice. Python 3.9+."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations


@lru_cache(None)
def good(v):
    return [(F(7*j+1, 7*v), F(7*j+6, 7*v)) for j in range(v)]


def intersect(A, B):
    out = []
    i = j = 0
    while i < len(A) and j < len(B):
        x, y = A[i]
        u, v = B[j]
        lo, hi = max(x, u), min(y, v)
        if lo < hi:
            out.append((lo, hi))
        i += y <= v
        j += v <= y
    return out


def floor(x):
    return x.numerator // x.denominator


def hits(I, b):
    for x, y in I:
        j = floor(b*x - F(6, 7)) + 1
        if j + F(1, 7) < b*y:
            return True
    return False


def runners():
    count4 = count5 = count6 = max_a = max_b = 0
    residual = []
    for vs in combinations(range(1, 13), 4):
        count4 += 1
        I = [(F(0), F(1))]
        for v in vs:
            I = intersect(I, good(v))
        L = max(y-x for x, y in I)
        for a in range(vs[-1]+1, floor(4/(3*L))+1):
            count5 += 1
            max_a = max(max_a, a)
            J = intersect(I, good(a))
            M = max(y-x for x, y in J)
            for b in range(a+1, floor(2/(7*M))+1):
                count6 += 1
                max_b = max(max_b, b)
                if not hits(J, b):
                    residual.append(vs + (a, b))
    expected = [tuple(d*i for i in range(1, 7)) for d in (1, 2, 3)]
    if residual != expected:
        raise AssertionError(residual)
    print(f"runners: prefixes4={count4}, prefixes5={count5}, sextuples={count6}, "
          f"max_a_checked={max_a}, max_b_checked={max_b}, residual={residual}")


if __name__ == "__main__":
    runners()
