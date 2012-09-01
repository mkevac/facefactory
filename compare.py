#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pprint
import sys
import math

def main():

    if len(sys.argv) < 3:
        print "usage: %s <origresult> <ourresult>"
        sys.exit(1)

    origresultfilename = sys.argv[1]
    ourresultfilename = sys.argv[2]

    originaldata = {}

    with open(origresultfilename) as fp:
        for line in fp.readlines():
            url, x1, y1, x2, y2 = line.split(',')
            x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)
            imagename = url.split('/')[-1].split('?')[0]

            originaldata[imagename] = {'x': x1, 'y': y1, 'width': x2-x1, 'height': y2-y1}


    with open(ourresultfilename, "r") as fp:
        ourresult = json.load(fp)

    decision = {}

    for image, ourimage in ourresult.iteritems():

        for algresult in ourimage:

            try:
                decision[algresult['algorithm']]
            except KeyError:
                decision[algresult['algorithm']] = 0

            if len(algresult['faces']) == 0:
                decision[algresult['algorithm']] -= 0.5
                continue

            if len(algresult['faces']) > 1:
                decision[algresult['algorithm']] -= 0.1

            found = False

            for face in algresult['faces']:
                oursquarecenter = (face['x'] + face['width']/2, face['y'] + face['height']/2)

                try:
                    origimage = originaldata[image]
                except KeyError:
                    continue

                originalsquarecenter = (origimage['x'] + origimage['width']/2, origimage['y'] + origimage['height']/2)

                distance = math.sqrt(pow((oursquarecenter[0]-originalsquarecenter[0]), 2) + pow((oursquarecenter[1]-originalsquarecenter[1]), 2))
                if distance <= 70.0:
                    print "image '%s': distance is smaller than 70pix (%d) -> ok" % (image, distance)
                    found = True
                else:
                    print "image '%s': distance is bigger than 70pix (%d) -> bad" % (image, distance)

            if found:
                decision[algresult['algorithm']] += 1
            else:
                decision[algresult['algorithm']] -= 0.5

    print decision

if __name__ == "__main__":
    main()
