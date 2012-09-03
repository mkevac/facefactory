#!/usr/bin/env python
# -*- coding: utf-8 -*-

import facealgorithm
import pbs

class FSE(facealgorithm.FaceAlgorithm):
    def __init__(self, name):
        super(FSE, self).__init__(name)

    def findFace(self, imagePath):
        copycmd = pbs.Command("rsync")
        copycmd("-avz", imagePath, "www1.d4:/home/marko/images")

        imagename = imagePath[imagePath.rindex('/')+1:]

        findcmd = pbs.Command("ssh")

        res = findcmd("www1.d4", "/home/marko/showFaces.php /home/marko/images/%s" % imagename)
        res = [line for line in res.split('\n') if line != ""]

        faces = []

        if len(res) <= 0:
            return None
        for line in res:
            face = facealgorithm.Face()
            try:
                face.x, face.y, face.width, face.height = line.split(" ")
            except ValueError:
                print "could not unpack line '%s'" % line
                return None

            face.x = int(face.x)
            face.y = int(face.y)
            face.width = int(face.width)
            face.height = int(face.height)
            faces.append(face)

        return faces