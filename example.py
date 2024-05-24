#!/usr/bin/env python3
from limitloop import limitloop, endloop, getfps
from math import sqrt

i = 0
def test_func():
    global i
    i += 1
    print("Iteration {}, FPS is {}".format(i, getfps()))
    
    for j in range(0, 1000000):
        sqrt(j)
    
    if i == 10: #End loop when i reaches 10
        endloop()
        print("Loop broken")

if __name__ == "__main__":
    limitloop(test_func, 90)
