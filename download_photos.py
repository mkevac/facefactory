#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pbs

def main():
    if len(sys.argv) < 3:
        print "usage: %s <filename> <output directory>" % sys.argv[0]
        sys.exit(1)

    filename = sys.argv[1]
    output_directory = sys.argv[2]

    with open(filename) as fp:
        for line in fp.readlines():
            url = line.split(',')[0]
            filename = line.split('/')[-1].split('?')[0]
            pbs.curl(url, o="%s/%s" % (output_directory, filename))

if __name__ == "__main__":
    main()