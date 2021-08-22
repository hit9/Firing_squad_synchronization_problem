"""
Firing squad synchronization problem - Python solution.

Algorithm of John McCarthy and Marvin Minsky, 15 States.

https://en.wikipedia.org/wiki/Firing_squad_synchronization_problem
"""

import sys
import time

I = "·"
G = "G"
L = "L"
R = "R"
A = "A"
B = "B"
C = "C"
a = "a"
b = "b"
c = "c"
bB = "bB"
cC = "cC"
RL = "RL"
LR = "LR"
F = "F"


def next(l, s, r):
    if s == A:
        if r[0] == "L":
            return G
        return B
    if s == B:
        return C
    if s == C:
        if r[0] == "L":
            return G
        return I
    if s == a:
        if l[-1] == "R":
            return G
        return b
    if s == b:
        return c
    if s == c:
        if l[-1] == "R":
            return G
        return I
    if s == "bB":
        return cC
    if s == "cC":
        if l[-1] == "R":
            return G
        if r[0] == "L":
            return G
        return I
    if s == G:
        if (l + r) in ("$$", "$G", "G$", "GG"):
            return F
        if r == I and l == I:
            return bB
        if r == I:
            return B
        if l == I:
            return b
    if s == L:
        if l == "$":
            return R
        if l[-1] == "R":
            return R
        if l[-1] == "C":
            return G
        if r == G:
            return L
        return I
    if s == R:
        if r == "$":
            return L
        if r[0] == "L":
            return L
        if r[0] == "c":
            return G
        return I
    if s == LR:
        if l[-1] == "C" or r[0] == "c":
            return G
        return I
    if s == RL:
        return LR
    if s == I:
        if l == G or l[-1] == "R":
            if r == G or r[0] == "L":
                return RL
            return R
        if r == G or r[0] == "L":
            if l == G or l[-1] == "R":
                return RL
            return L
        if l[-1] == "C":
            return A
        if r[0] == "c":
            return a
    return s


def echo(s):
    sys.stdout.write(s.ljust(4))
    sys.stdout.flush()


def simulate(n, sleep_secs=0.05, do_print=True):
    assert n > 0

    seq = [I] * n
    seq[0] = G

    if do_print:
        for s in seq:
            echo(s)
        sys.stdout.write("\n")

    while 1:
        seq1 = []
        for j, s in enumerate(seq):
            l = seq[j - 1] if j - 1 >= 0 else "$"
            r = seq[j + 1] if j + 1 < len(seq) else "$"
            s1 = next(l, s, r)
            seq1.append(s1)

            if do_print:
                echo(s1)
                if sleep_secs > 0:
                    time.sleep(sleep_secs)

            if s1 == s and s != I:
                raise Exception(f"Non idle state repeated: {l} {s} {r}")
        seq = seq1

        if do_print:
            sys.stdout.write("\n")

        if set(seq) == {F}:
            print("FIRE")
            break


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 13
    simulate(n, sleep_secs=0.02, do_print=True)
