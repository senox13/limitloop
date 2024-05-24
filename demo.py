#!/usr/bin/env python3

from limitloop import limitloop, endloop, getfps

i = 0
def test_func():
    global i
    i += 1
    print("Iteration {}, FPS is {}".format(i, getfps()))
    if i == 10:
        print("Ending loop")
        endloop()

if __name__ == "__main__":
    limitloop(test_func, 90)

