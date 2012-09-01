# -*- coding: utf-8 -*-

"""The user interface for our app"""

import os, sys

from algorithms.libccv import LibCCV
from algorithms.opencv import OpenCV
from algorithms.fse import FSE

from PySide import QtCore, QtGui

algorithms = [FSE("fse"),
              LibCCV("libccv", bin_path="/Users/marko/Dropbox/projects/ccv/bin", face_path="/Users/marko/Dropbox/projects/ccv/samples/face"),
              OpenCV("opencv-default", cascade_path="/usr/local/Cellar/opencv/2.4.2/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"),
              OpenCV("opencv-alt", cascade_path="/usr/local/Cellar/opencv/2.4.2/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"),
              OpenCV("opencv-alt2", cascade_path="/usr/local/Cellar/opencv/2.4.2/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")]

images = []
current_image = None

class MyImage(QtGui.QLabel):

    def __init__(self):
        super(MyImage, self).__init__()
        self.faces = None
        self.scaling = 1
    def paintEvent(self, event):
        super(MyImage, self).paintEvent(event)

        if self.faces:
            painter = QtGui.QPainter(self)
            painter.setPen(QtGui.QColor(255,255,0)) #yellow
            for face in self.faces:
                rect = QtCore.QRect(face.x*self.scaling, face.y*self.scaling, face.width*self.scaling, face.height*self.scaling)
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

    def openImage(self, path=None):
        if not path:
            path = QtGui.QFileDialog.getOpenFileName()

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

    def minimumSizeHint(self):
        if self.imagesLayout.pixmap:
            return QtCore.QSize(800, self.pixmap.height())
        return QtCore.QSize(100, 100)

    def sizeHint(self):
        return QtCore.QSize(1024, 800)

    def loadImage(self):

        print "loading image"

        global current_image

        if current_image == None:
            current_image = 0
        else:
            current_image += 1

        print "current image", current_image
        print "len", len(images)
        if current_image >= len(images):
            return

        for widget in self.imagesLayout.widgets:
            self.imagesLayout.removeWidget(widget)
            widget.deleteLater()

        pixmap = QtGui.QPixmap()
        if not pixmap.load(images[current_image]):
            QtGui.QMessageBox.warning(self, "Open Image", "The image file could not be loaded.", QtGui.QMessageBox.Cancel)
            return

        window_width = self.geometry().width()
        new_width = window_width/len(algorithms)
        scaling = float(new_width) / float(pixmap.width())
        pixmap = pixmap.scaledToWidth(new_width)
        self.pixmap = pixmap

        self.imagesLayout.widgets = []

        for algorithm in algorithms:
            label = MyImage()
            label.setPixmap(pixmap)
            label.scaling = scaling
            faces = algorithm.findFace(images[current_image])
            if faces:
                label.faces = faces
            self.imagesLayout.addWidget(label)
            self.imagesLayout.widgets.append(label)

def main():
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()