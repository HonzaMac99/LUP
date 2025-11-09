#!/usr/bin/env python
"""
Task2, LUP, 2025.

You need the Python wrapper for Z3. You can install it, for example, by

pip install z3-solver

A tutorial Z3 API in Python is available at (but there is no need to go through it):

https://microsoft.github.io/z3guide/programming/Z3%20Python%20-%20Readonly/Introduction

For details, see https://z3prover.github.io/api/html/index.html

Note that you may get different counterexamples!
"""

from z3 import * # We want to experiment...

def mean(x, y):
    """
    The function returns the mean of ``x`` and ``y``.
    """
    return (x + y) / 2

# Define two reals.
x, y = Reals("x y")


# We want to prove that mean(x, y) < x or mean(x, y) < y
#
# For prove, see
# https://z3prover.github.io/api/html/namespacez3py.html#afe5063009623290e15bf3f15183bbd50

prove(Or(mean(x, y) < x, mean(x, y) < y))
# counterexample
# [y = 0, x = 0]


# Ok, so assume that x < y

prove(Implies(x < y, Or(mean(x, y) < x, mean(x, y) < y)))
# proved


# Is it still the case if x and y are floats?

x_fp, y_fp, mean_fp = FPs("x_fp y_fp mean_fp", Float32())
prove(Implies(And(x_fp < y_fp, mean(x_fp, y_fp) == mean_fp), Or(mean_fp < x_fp, mean_fp < y_fp)))
# counterexample
# [y_fp = -1.5156190395355224609375*(2**-115),
#  mean_fp = -1.5156190395355224609375*(2**-115),
#  x_fp = -1.51561915874481201171875*(2**-115)]


# Say we want to show that
#
# if 1 < x and 1 < y then mean(x, y) != sqrt(x)
#
# Do not use Sqrt(x) from Z3, or add Sqrt(x) * Sqrt(x) == x among your conditions...

sqrt_x = Real("sqrt_x")
prove(Implies(And(1 < x, 1 < y, 0 < sqrt_x, sqrt_x * sqrt_x == x), mean(x, y) != sqrt_x))
# proved

######################
# Task2 starts here. #
######################

def heron(x, init=1, iters=6):
    """
    It computes the approximation of sqrt(x) using Heron's method
    where ``init`` is the initial estimate. The number of iterations
    is in ``iters``.
    
    https://en.wikipedia.org/wiki/Methods_of_computing_square_roots#Heron's_method
    """
    res = init
    for _ in range(iters):
        res = (x / res + res) / 2
    return res


print("First task:")
# 1) Let x be a real number such that 0 < x < 100. (5 points.)

# - Find a counterexample for |heron(x, init=1, iters=6) - sqrt(x)| < 0.01.

x, sqrt_x = Reals("x sqrt_x")
prove(Implies(And(0 < x, 100 > x, 0 < sqrt_x, sqrt_x * sqrt_x == x), Abs(heron(x, init=1, iters=6) - sqrt_x) < 0.01))
# counterexample
# [x = 1/65536,
#  sqrt_x = 1/256,
#  /0 = [(1/65536,
#         116669415233980221858614236280625329462402168448850656480924014565503414566913/3714115847506448008307728517843975755945054265867022173029130126229811629129728) ->
#        56672910270789306767390877042296993346329563382980685013261873264004694048/116669415233980221858614236280625329462402168448850656480924014565503414566913,
#        (1/65536,
#         340905586748899734115216925744587866113/5447425903058239103600970451551993724928) ->
#        83121122788364244134536292290527248/340905586748899734115216925744587866113,
#        (1/65536, 18454625673706995713/147589715428890902528) ->
#        2252040335523848/18454625673706995713,
#        (1/65536, 4295360513/17180131328) ->
#        262148/4295360513,
#        (1/65536, 65537/131072) -> 2/65537,
#        else -> 0]]


# - Prove |heron(x, init=1, iters=7) - sqrt(x)| < 0.01.

x, sqrt_x = Reals("x sqrt_x")
prove(Implies(And(0 < x, 100 > x, 0 < sqrt_x, sqrt_x * sqrt_x == x), Abs(heron(x, init=1, iters=7) - sqrt_x) < 0.01))
# proved


print("Second task:")
# 2) Let x and b be real numbers such that 0 < x and 0 < b. (7 points.)

# - Find a counterexample for
# |heron(x, init=b, iters=1) - sqrt(x)| > |heron(x, init=b, iters=2) - sqrt(x)|.

x, b, sqrt_x = Reals("x b sqrt_x")
prove(Implies(And(0 < x, 0 < b, 0 < sqrt_x, sqrt_x * sqrt_x == x),
              Abs(heron(x, init=b, iters=1) - sqrt_x) > (heron(x, init=b, iters=2) - sqrt_x)))
# counterexample
# [b = 1, x = 1, sqrt_x = 1, /0 = [(1, 1) -> 1, else -> 0]]

# - Prove that the previous holds if b != sqrt(x).

x, b, sqrt_x = Reals("x b sqrt_x")
prove(Implies(And(0 < x, 0 < b, 0 < sqrt_x, sqrt_x * sqrt_x == x, b != sqrt_x),
              Abs(heron(x, init=b, iters=1) - sqrt_x) > (heron(x, init=b, iters=2) - sqrt_x)))
# proved

# - If b != sqrt(x), find (experimentally) the maximal real number c for which you can prove
# |heron(x, init=b, iters=1) - sqrt(x)| > c*|heron(x, init=b, iters=3) - sqrt(x)|.

def bisection(lb, ub, max_iter=10):
    print("Input '1' if proved and '0' if we got a counterexample")
    c_val = (ub - lb) / 2
    c_vals = []
    res = c_val
    for i in range(max_iter):
        print("New_c: ", c_val)
        x, b, c, sqrt_x = Reals("x b c sqrt_x")
        prove(Implies(And(0 < x, 0 < b, 0 < sqrt_x, sqrt_x * sqrt_x == x, b != sqrt_x, c == c_val),
                      Abs(heron(x, init=b, iters=1) - sqrt_x) > c * (heron(x, init=b, iters=2) - sqrt_x)))
        c_vals.append(c_val)
        proved = int(input()) # couldn't get binary output, so setting it manually
        if proved:
            res = c_val
            lb = c_val
            c_val += (ub-c_val)/2
        else:
            ub = c_val
            c_val -= (c_val-lb)/2
    print(c_vals)
    print("c = {}".format(res))
    return res

# --> I have first let the solver choose a counterexample for arbitrary c value: c = 11,
#     then I tried bisection method for 15 iterations:

c_approx = bisection(0, 11, 15)

# [5.5, 2.75, 1.375, 2.0625, 1.71875, 1.890625, 1.9765625, 2.01953125, 1.998046875, 2.0087890625,
# 2.00341796875, 2.000732421875, 1.9993896484375, 2.00006103515625, 1.999725341796875]
# c = 1.999725341796875

# --> the number clearly converges to a value of 2, so we prove that c == 2 is the highest value:

x, b, c, sqrt_x = Reals("x b c sqrt_x")
prove(Implies(And(0 < x, 0 < b, 0 < sqrt_x, sqrt_x * sqrt_x == x, b != sqrt_x, c == 2),
              Abs(heron(x, init=b, iters=1) - sqrt_x) > c * (heron(x, init=b, iters=2) - sqrt_x)))
# proved


print("Third task:")
# 3) Let x, b1, and b2 be real numbers such that 0 < x and 0 < b1 < b2. 
#    Moreover, | sqrt(x) - b1| == | sqrt(x) - b2|. (3 points.)

# Is heron(x, iters=1, init=b1) or heron(x, iters=1, init=b2) a better
# approximation of sqrt(x)? Prove your claim!
x, b1, b2, sqrt_x = Reals("x b1 b2 sqrt_x")

a1 = And(0 < x, 0 < b1, b1 < b2, sqrt_x * sqrt_x == x, Abs(sqrt_x - b1) == Abs(sqrt_x - b2))
a2 = Abs(heron(x, iters=1, init=b1) - sqrt_x) < Abs(heron(x, iters=1, init=b2) - sqrt_x)
a3 = Abs(heron(x, iters=1, init=b1) - sqrt_x) > Abs(heron(x, iters=1, init=b2) - sqrt_x)

prove(Implies(a1, a2))
# counterexample
# [b1 = 1/2,
# x = 1,
# sqrt_x = 1,
# b2 = 3/2,
# /0 = [(1, 1/2) -> 2, (1, 3/2) -> 2/3, else -> 0]]

prove(Implies(a1, a3))
# proved
# --> better approximation of sqrt_x is heron with b2: heron(x, iters=1, init=b2)
