import os
import math
import pysat

pysat.params['data_dirs'] = "pysat_files"

# in_str = input()
in_str = "WWWBW0BWWWWWWWWWWW12WBWWW"
print(in_str)
n = math.sqrt(len(in_str))
assert n**2 == len(in_str), "invalid input length!"

