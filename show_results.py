#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The user interface for our app"""

import os, sys
import simplejson as json

from algorithms.libccv import LibCCV
from algorithms.opencv import OpenCV
from algorithms.fse import FSE

from PySide import QtCore, QtGui

images = []
current_image = None

class MyImage(QtGui.QLabel):

    def __init__(self):
        super(MyImage, self).__init__()
        self.faces = None
        self.scaling = 1
    def paintEvent(self, event):
        super(MyImage, self).paintEvent(event)

        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QColor(255,255,0)) #yellow

        painter.drawText(QtCore.QRect(0, 0, 200, 50), self.algo)

        if self.faces:
            for face in self.faces:
                rect = QtCore.QRect(face['x']*self.scaling, face['y']*self.scaling, face['width']*self.scaling, face['height']*self.scaling)
                painter.drawRect(rect)

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1024, 600)
        self.setupMenus()
        self._dialog = Dialog()
        self.setCentralWidget(self._dialog)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed))
        self.fullScreen = False

    def setupMenus(self):
        fileMenu = self.menuBar().addMenu("&File")

        openAction = fileMenu.addAction("&Open dir...")
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(self.openDir)

        openAction = fileMenu.addAction("&Open image...")
        openAction.setShortcut("Ctrl+P")
        openAction.triggered.connect(self.openImage)

        viewMenu = self.menuBar().addMenu("View")

        fullScreenAction = viewMenu.addAction("&Full screen")
        fullScreenAction.setShortcut("Ctrl+F")
        fullScreenAction.triggered.connect(self.fullScreenToggle)

    def fullScreenToggle(self):
        if not self.fullScreen:
            self.fullScreen = True
            self.showFullScreen()
        else:
            self.fullScreen = False
            self.showNormal()

    def openImage(self):
        image = QtGui.QFileDialog.getOpenFileName(caption="choose image file")
        originalresult = QtGui.QFileDialog.getOpenFileName(caption="choose original result file")
        originalresult = QtGui.QFileDialog.getOpenFileName(caption="choose original result file")

        if path:

            global images, current_image

            images = [path[0]]

            self._dialog.loadImage()

    def openDir(self, path=None):
        if not path:
            path = QtGui.QFileDialog.getExistingDirectory()

        if path:

            global images, current_image

            images = []

            dirList = os.listdir(path)
            for fname in dirList:
                images.append(path+"/"+fname)

            self._dialog.loadImage()

class Dialog(QtGui.QScrollArea):

    def __init__(self):
        super(Dialog, self).__init__()

        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)

        buttonlayout = QtGui.QHBoxLayout()
        openImageButton = QtGui.QPushButton("Open image...")
        openImageButton.clicked.connect(self.chooseImage)
        openDirButton = QtGui.QPushButton("Open dir...")
        openDirButton.clicked.connect(self.chooseDirectory)
        self.imagediredit = textEdit = QtGui.QLineEdit()
        buttonlayout.addWidget(textEdit)
        buttonlayout.addWidget(openImageButton)
        buttonlayout.addWidget(openDirButton)
        self.mainLayout.addLayout(buttonlayout)

        buttonlayout2 = QtGui.QHBoxLayout()
        self.origresultsedit = textEdit2 = QtGui.QLineEdit()
        openFileButton2 = QtGui.QPushButton("Open original results...")
        openFileButton2.clicked.connect(self.chooseOrigResults)
        buttonlayout2.addWidget(textEdit2)
        buttonlayout2.addWidget(openFileButton2)
        self.mainLayout.addLayout(buttonlayout2)

        buttonlayout3 = QtGui.QHBoxLayout()
        self.ourresultsedit = textEdit3 = QtGui.QLineEdit()
        openFileButton3 = QtGui.QPushButton("Open our results...")
        openFileButton3.clicked.connect(self.chooseOurResults)
        buttonlayout3.addWidget(textEdit3)
        buttonlayout3.addWidget(openFileButton3)
        self.mainLayout.addLayout(buttonlayout3)

        buttonapply = QtGui.QPushButton("Apply")
        buttonapply.clicked.connect(self.apply)
        self.mainLayout.addWidget(buttonapply)

        self.imagesLayout = QtGui.QHBoxLayout()
        self.imagesLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.imagesLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.imagesLayout.widgets = []
        self.imagesLayout.pixmap = None
        self.mainLayout.addLayout(self.imagesLayout)

        self.nextButton = QtGui.QPushButton("&Next image")
        self.nextButton.clicked.connect(self.loadImage)

        self.buttonLayout = QtGui.QHBoxLayout()
        self.buttonLayout.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        self.buttonLayout.addWidget(self.nextButton)
        self.mainLayout.addLayout(self.buttonLayout)

    def chooseImage(self):
        image = QtGui.QFileDialog.getOpenFileName(caption="choose image")
        self.image = image[0]
        self.imagediredit.setText(self.image)
        self.directory = None

    def chooseDirectory(self):
        self.directory = QtGui.QFileDialog.getExistingDirectory(caption="choose directory")
        print self.directory
        self.imagediredit.setText(self.directory)
        self.image = None

    def apply(self):
        global images, current_image
        images = []

        if self.directory:
            dirList = os.listdir(self.directory)
            for fname in dirList:
                images.append(self.directory+"/"+fname)

        if self.image:
            images.append(self.image)

        current_image = None
        self.loadImage()

    def chooseOrigResults(self):
        origresults = QtGui.QFileDialog.getOpenFileName(caption="choose orig results")
        self.origresultsfn = origresults[0]
        self.origresultsedit.setText(self.origresultsfn)

    def chooseOurResults(self):
        ourresults = QtGui.QFileDialog.getOpenFileName(caption="choose our results")
        self.ourresultsfn = ourresults[0]
        self.ourresultsedit.setText(self.ourresultsfn)

    def minimumSizeHint(self):
        if self.imagesLayout.pixmap:
            return QtCore.QSize(800, self.pixmap.height())
        return QtCore.QSize(100, 100)

    def sizeHint(self):
        return QtCore.QSize(1024, 800)

    def loadOurResults(self, filename):
        self.ourresults = json.load(open(filename, "r"))

    def loadOrigResults(self, filename):

        originaldata = {}

        with open(filename) as fp:
            for line in fp.readlines():
                url, x1, y1, x2, y2 = line.split(',')
                x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)
                imagename = url.split('/')[-1].split('?')[0]

                originaldata[imagename] = {'x': x1, 'y': y1, 'width': x2-x1, 'height': y2-y1}

        self.origresults = originaldata

    def loadImage(self):

        global current_image

        if current_image == None:
            current_image = 0
        else:
            current_image += 1

        if current_image >= len(images):
            return

        if not self.ourresultsfn or not self.origresultsfn:
            return

        self.loadOrigResults(self.origresultsfn)
        self.loadOurResults(self.ourresultsfn)

        # clean old images
        for widget in self.imagesLayout.widgets:
            self.imagesLayout.removeWidget(widget)
            widget.deleteLater()

        #load new image
        pixmap = QtGui.QPixmap()
        if not pixmap.load(images[current_image]):
            QtGui.QMessageBox.warning(self, "Open Image", "The image file could not be loaded.", QtGui.QMessageBox.Cancel)
            return

        algorithms_count = len(self.ourresults.values()[0])+1

        window_width = self.geometry().width()
        new_width = window_width/algorithms_count
        scaling = float(new_width) / float(pixmap.width())
        pixmap = pixmap.scaledToWidth(new_width)
        self.pixmap = pixmap

        self.imagesLayout.widgets = []

        ourimagedata = self.ourresults[images[current_image].split('/')[-1]]
        origimagedata = self.origresults[images[current_image].split('/')[-1]]
        print origimagedata

        label = MyImage()
        label.setPixmap(pixmap)
        label.scaling = scaling
        label.faces = [origimagedata]
        label.algo = "orig"
        print label.faces
        self.imagesLayout.addWidget(label)
        self.imagesLayout.widgets.append(label)

        for algorithm in ourimagedata:
            label = MyImage()
            label.setPixmap(pixmap)
            label.scaling = scaling
            label.faces = algorithm['faces']
            label.algo = algorithm['algorithm']
            self.imagesLayout.addWidget(label)
            self.imagesLayout.widgets.append(label)

def main():
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
