#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Face(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.confidence = 0

    def __str__(self):
        return "x: %s y: %s width: %s height: %s confidence: %s" % \
              (self.x, self.y, self.width, self.height, self.confidence)

    def __repr__(self):
        return "Face (" + self.__str__() + ")"

class FaceAlgorithm(object):
    def __init__(self, name):
        self.name = name

    def findFace(self, imagePath):
        pass