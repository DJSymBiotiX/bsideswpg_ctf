#!/usr/bin/env python

import argparse

from sys import exit

def main():
    args = parse_args()
    ciphertext = args.ciphertext.readline()
    plaintext = args.plaintext.readline()
    flagcipher = ''.join([line for line in args.flagcipher])

    # With help from https://gist.github.com/craSH/2969666

    keystream = (map(lambda x: x[0] ^ x[1], zip(map(ord, ciphertext), map(ord, plaintext))))

    # decrypt
    pt = ''
    for pos in xrange(len(ciphertext)):
        if pos >= len(keystream):
            print "Ran out of keystream material at pos = %d" % pos
            break
        else:
            pt += chr(ord(ciphertext[pos]) ^ keystream[pos])

    pt = ''
    for pos in xrange(len(flagcipher)):
        pt += chr(ord(flagcipher[pos]) ^ keystream[pos])

    print "Solution: %s" % pt

    exit (0)

def parse_args():
    parser = argparse.ArgumentParser(description="Fuck The Police")
    parser.add_argument("plaintext", type=argparse.FileType('rb'))
    parser.add_argument("ciphertext", type=argparse.FileType('rb'))
    parser.add_argument("flagcipher", type=argparse.FileType('rb'))

    return parser.parse_args()


if __name__ == "__main__":
    main()
