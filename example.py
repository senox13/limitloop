#!/usr/bin/env python3
from limitloop import limitloop, endloop, getfps, frame_time_remaining
from math import sqrt

i = 0
def test_func():
    global i
    i += 1
    #print('Iteration {}, FPS is {}'.format(i, getfps()))
    print('Frame time remaining in ns: {}'.format(frame_time_remaining()*1e9))

    for j in range(0, 1000000):
        sqrt(j)

    if i == 10: #End loop when i reaches 10
        endloop()
        print("Loop broken")

if __name__ == "__main__":
    limitloop(test_func, 90)
