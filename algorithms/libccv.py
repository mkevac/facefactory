#!/usr/bin/env python
# -*- coding: utf-8 -*-

import facealgorithm
import pbs

class LibCCV(facealgorithm.FaceAlgorithm):
    def __init__(self, bin_path, face_path):
        super(LibCCV, self).__init__()

        self._bin_path = bin_path
        self._face_path = face_path
        self._bbfdetect = pbs.Command(self._bin_path + "/" + "bbfdetect")

    def findFace(self, imagePath):
        faces = []

        res = self._bbfdetect(imagePath, self._face_path)
        res = [line for line in res.split('\n') if line != ""]

        if len(res) <= 0:
            return None
        for line in res[:-1]:
            face = facealgorithm.Face()
            face.x, face.y, face.width, face.height, face.confidence = line.split(" ")
            face.x = int(face.x)
            face.y = int(face.y)
            face.width = int(face.width)
            face.height = int(face.height)
            faces.append(face)

        return faces

