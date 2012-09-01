#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import simplejson as json

from algorithms.libccv import LibCCV
from algorithms.opencv import OpenCV
from algorithms.fse import FSE

algorithms = [FSE("fse"),
              LibCCV("ccv", bin_path="/Users/marko/Dropbox/projects/ccv/bin", face_path="/Users/marko/Dropbox/projects/ccv/samples/face"),
              OpenCV("opencv-default", cascade_path="/usr/local/Cellar/opencv/2.4.2/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"),
              OpenCV("opencv-alt", cascade_path="/usr/local/Cellar/opencv/2.4.2/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"),
              OpenCV("opencv-alt2", cascade_path="/usr/local/Cellar/opencv/2.4.2/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")]

def saveData(result, result_file):
    with open(result_file, 'w') as fp:
        json.dump(result, fp)

def main():
    if len(sys.argv) < 3:
        print "usage: %s <image_path> <result_file>" % sys.argv[0]
        sys.exit(1)

    images_path = sys.argv[1]
    result_file = sys.argv[2]
    print "analyzing images from path", images_path

    images = []

    dirList = os.listdir(images_path)
    for fname in dirList:
        images.append(fname)

    print "loading previous results from analyzeresult.json"
    try:
        with open(result_file, "r") as fpbackup:
            result = json.load(fpbackup)
    except IOError, err:
        print "error while loading previous results:", err
        result = {}

    total_images = len(images)
    print "found %d images in path" % total_images

    for imageno, image in enumerate(images):

        if image in result:
            print "image %s already in result" % image
            continue

        resultentry = []

        for algorithmno, algorithm in enumerate(algorithms):
            print "analyzing picture %d of %d (%f%%) with algorithm %s" % (imageno, total_images, (float(imageno)/float(total_images))*100, algorithm.name)
            faces = algorithm.findFace(images_path+'/'+image)

            resultentry2 = {'algorithm': algorithm.name, 'faces': []}

            if faces:
                for face in faces:
                    resultentry2['faces'].append({'x': face.x, 'y': face.y, 'width': face.width, 'height': face.height})

            resultentry.append(resultentry2)

        result[image] = resultentry

        if imageno % 50 == 0:
            saveData(result, result_file)

if __name__ == "__main__":
    main()