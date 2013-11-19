#!/usr/bin/env python

import argparse

from sys import exit

TOP = 7
TOP_RIGHT = 6
TOP_LEFT = 2
MIDDLE = 1
BOTTOM_RIGHT = 5
BOTTOM_LEFT = 3
BOTTOM = 4
DECIMAL = 0

ON = '1'
OFF = '0'
CHUNK = 8
TOTAL_CHUNKS = 25

TAP_A = [199, 197]
TAP_B = [196, 194]

display = """
 _
|_   _   _   _   _
|_  |   |   |_| |  .

"""

def find_new_bit(byte_string):
    a = int(byte_string[TAP_A[0]])
    b = int(byte_string[TAP_A[1]])
    c = int(byte_string[TAP_B[0]])
    d = int(byte_string[TAP_B[1]])

    def b_xor(a, b):
        return a ^ b
    def b_not(a):
        if a == 0:
            return 1
        if a == 1:
            return 0

    print "%s, %s, %s, %s" % (a,b,c,d)

    NXOR_A = b_not(b_xor(a, b))
    NXOR_B = b_not(b_xor(c, d))
    new_bit = b_not(b_xor(NXOR_A, NXOR_B))

    print new_bit


    return new_bit

def on(byte, position):
    return byte[position] == ON

def off(byte, position):
    return not on(byte, position)

def draw(byte_string):
    byte_array = map(None, *([iter(byte_string)]) * CHUNK)[0:TOTAL_CHUNKS]

    # Print Top
    string = ''
    for b in byte_array:
        if on(b, TOP):
            string += " _  "
        else:
            string += "    "
    #    string += "  "
    print string


    # Print Top Left, Middle, and Top Right
    string = ''
    for b in byte_array:
        if on(b, TOP_LEFT) and on(b, MIDDLE) and on(b, TOP_RIGHT):
            string +=  "|_| "
        elif on(b, TOP_LEFT) and on(b, MIDDLE) and off(b, TOP_RIGHT):
            string +=  "|_  "
        elif on(b, TOP_LEFT) and off(b, MIDDLE) and off(b, TOP_RIGHT):
            string +=  "|   "
        elif off(b, TOP_LEFT) and on(b, MIDDLE) and on(b, TOP_RIGHT):
            string +=  " _| "
        elif off(b, TOP_LEFT) and off(b, MIDDLE) and on(b, TOP_RIGHT):
            string +=  "  | "
        elif on(b, TOP_LEFT) and off(b, MIDDLE) and on(b, TOP_RIGHT):
            string +=  "| | "
        elif off(b, TOP_LEFT) and on(b, MIDDLE) and off(b, TOP_RIGHT):
            string +=  " _  "
        else:
            string +=  "    "
        #string +=  "  "
    print string

    # Print Bottom Left, Bottom, Bottom Right, Decimal Point
    string = ''
    for b in byte_array:
        if on(b, BOTTOM_LEFT) and on(b, BOTTOM) and on(b, BOTTOM_RIGHT) and off(b, DECIMAL):
            string += "|_| "
        elif on(b, BOTTOM_LEFT) and on(b, BOTTOM) and off(b, BOTTOM_RIGHT) and off(b, DECIMAL):
            string += "|_  "
        elif on(b, BOTTOM_LEFT) and off(b, BOTTOM) and off(b, BOTTOM_RIGHT) and off(b, DECIMAL):
            string += "|   "
        elif on(b, BOTTOM_LEFT) and off(b, BOTTOM) and on(b, BOTTOM_RIGHT) and off(b, DECIMAL):
            string += "| | "
        elif off(b, BOTTOM_LEFT) and on(b, BOTTOM) and on(b, BOTTOM_RIGHT) and off(b, DECIMAL):
            string += " _| "
        elif off(b, BOTTOM_LEFT) and off(b, BOTTOM) and on(b, BOTTOM_RIGHT) and off(b, DECIMAL):
            string += "  | "
        elif off(b, BOTTOM_LEFT) and on(b, BOTTOM) and off(b, BOTTOM_RIGHT) and off(b, DECIMAL):
            string += " _  "
        elif on(b, BOTTOM_LEFT) and on(b, BOTTOM) and on(b, BOTTOM_RIGHT) and on(b, DECIMAL):
            string += "|_|."
        elif on(b, BOTTOM_LEFT) and on(b, BOTTOM) and off(b, BOTTOM_RIGHT) and on(b, DECIMAL):
            string += "|_ ."
        elif on(b, BOTTOM_LEFT) and off(b, BOTTOM) and off(b, BOTTOM_RIGHT) and on(b, DECIMAL):
            string += "|  ."
        elif on(b, BOTTOM_LEFT) and off(b, BOTTOM) and on(b, BOTTOM_RIGHT) and on(b, DECIMAL):
            string += "| |."
        elif off(b, BOTTOM_LEFT) and on(b, BOTTOM) and on(b, BOTTOM_RIGHT) and on(b, DECIMAL):
            string += " _|."
        elif off(b, BOTTOM_LEFT) and off(b, BOTTOM) and on(b, BOTTOM_RIGHT) and on(b, DECIMAL):
            string += "  |."
        elif off(b, BOTTOM_LEFT) and on(b, BOTTOM) and off(b, BOTTOM_RIGHT) and on(b, DECIMAL):
            string += " _ ."
        else:
            string += "    "
        #string += "  "
    print string


def main():
    args = parse_args()

    byte_string = args.binary_file.readline().strip()

    print "Byte String:\n%s" % byte_string
    draw(byte_string)

    while raw_input("Continue? (y/n)") != 'n':
        new_bit = find_new_bit(byte_string)
        byte_string = str(new_bit) + byte_string[:-1]
        print "Byte String:\n%s" % byte_string
        draw(byte_string)

    exit (0)

def parse_args():
    parser = argparse.ArgumentParser(description="Fuck The Police")
    parser.add_argument("binary_file", type=argparse.FileType('r'))

    return parser.parse_args()


if __name__ == "__main__":
    main()
