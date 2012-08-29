#!/usr/bin/env python
# -*- coding: utf-8 -*-

import facealgorithm
import cv

class OpenCV(facealgorithm.FaceAlgorithm):

    def __init__(self, cascade_path):
        self._cascade_path = cascade_path
        self._image_scale = 2
        self._haar_scale = 1.2
        self._min_neighbors = 3
        self._haar_flags = 0
        self._min_size = (20, 20)
        super(OpenCV, self).__init__()

    def findFace(self, imagePath):
        img = cv.LoadImage(imagePath, 1)
        cascade = cv.Load(self._cascade_path)

        # allocate temporary images
        gray = cv.CreateImage((img.width,img.height), 8, 1)
        small_img = cv.CreateImage((cv.Round(img.width / self._image_scale),
                                    cv.Round(img.height / self._image_scale)), 8, 1)

        # convert color input image to grayscale
        cv.CvtColor(img, gray, cv.CV_BGR2GRAY)

        # scale input image for faster processing
        cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)

        cv.EqualizeHist(small_img, small_img)

        faces = cv.HaarDetectObjects(small_img, cascade, cv.CreateMemStorage(0), self._haar_scale, self._min_neighbors,
            self._haar_flags, self._min_size)

        if not faces:
            return None

        result = []

        for ((x, y, w, h), n) in faces:
            # the input to cv.HaarDetectObjects was resized, so scale the
            # bounding box of each face and convert it to two CvPoints
            face = facealgorithm.Face()
            face.x = int(x * self._image_scale)
            face.y = int(y * self._image_scale)
            face.width = int(w * self._image_scale)
            face.height = int(h * self._image_scale)
            result.append(face)

        return result