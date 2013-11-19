#!/usr/bin/env python
import math 
scrambled_flag = [
    [
        115,1481544,51,107,99,97,1124864,95,103,1331000,105,1331000,111,
        105,55,99,1331000,117,1061208,95,1124864,103,105,1124864
    ],
    [
        13225,12996,2601,11449,9801,9409,10816,9025,10609,12100,11025,
        12100,12321,11025,3025,9801,12100,13689,10404,9025,10816,10609,
        11025,10816
    ]
]
a = scrambled_flag[0]
b = scrambled_flag[1]

count = 0
combined = []
for x in a:
    combined.append([a[count], b[count]])
    count += 1

lst = []
for x in combined:
    first = x[0]
    second = x[1]
    if first > 9000:
        first = int(math.sqrt(second))
    lst.append(first)

lst.reverse()

string = ''
for x in lst:
    string += str(unichr(x))

print string

