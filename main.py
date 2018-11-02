import sys
import argparse
import os
from glob import glob

from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QApplication, QPushButton, QSlider, QLCDNumber, QAction, qApp, QFileDialog, QCheckBox
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt

import cv2

class Example(QMainWindow):
    def __init__(self, path = None):
        super().__init__()
        self.main_image = path
        self.overlay_image = None
        self.points = []

        self.num_overlay_count = 0
        self.num_create_count = 0
        self.overlay_size_count = 0

        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 700, 500)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        dlg = QFileDialog(self)       
        openAction = QAction('Open Image', self)
        openAction.triggered.connect(self.openMainImage)
        fileMenu.addAction(openAction)

        openSubAction = QAction('Overlay Image', self)
        openSubAction.triggered.connect(self.openSubImage)
        fileMenu.addAction(openSubAction)

        outputAction = QAction('Output', self)
        outputAction.triggered.connect(self.outputImage)
        fileMenu.addAction(outputAction)

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        # btn = QPushButton('create', self)
        # btn.setToolTip('This is a <b>QPushButton</b> widget')
        # btn.resize(btn.sizeHint())
        # btn.move(0, 360)
        # btn.clicked.connect(self.createImage)

        num_overlay_lbl = QLabel(self)
        num_overlay_lbl.setGeometry(0, 360, 90, 30)
        num_overlay_lbl.setText('num overlay:')

        num_overlay_sld = QSlider(Qt.Horizontal, self)
        num_overlay_sld.setMaximum(9)
        num_overlay_sld.setFocusPolicy(Qt.NoFocus)
        num_overlay_sld.setGeometry(100, 360, 100, 30)
        num_overlay_sld.valueChanged[int].connect(self.changeNumOverlay)

        self.num_overlay = QLCDNumber(self)
        self.num_overlay.display(1)
        self.num_overlay.setGeometry(220, 360, 100, 30)


        overlay_size_lbl = QLabel(self)
        overlay_size_lbl.setGeometry(0, 390, 90, 30)
        overlay_size_lbl.setText('overlay size:')

        overlay_size_sld = QSlider(Qt.Horizontal, self)
        overlay_size_sld.setFocusPolicy(Qt.NoFocus)
        overlay_size_sld.setGeometry(100, 390, 100, 30)
        overlay_size_sld.valueChanged[int].connect(self.changeOverlaySize)

        self.overlay_size = QLCDNumber(self)
        self.overlay_size.display(1)
        self.overlay_size.setGeometry(220, 390, 100, 30)


        num_create_lbl = QLabel(self)
        num_create_lbl.setGeometry(0, 420, 90, 30)
        num_create_lbl.setText('num create:')

        num_create_sld = QSlider(Qt.Horizontal, self)
        num_create_sld.setFocusPolicy(Qt.NoFocus)
        num_create_sld.setGeometry(100, 420, 100, 30)
        num_create_sld.valueChanged[int].connect(self.changeNumCreate)

        self.num_create = QLCDNumber(self)
        self.num_create.display(1)
        self.num_create.setGeometry(220, 420, 100, 30)

        is_Flip_h = QCheckBox('Flip Horizontal', self)
        is_Flip_h.move(80, 450)
        # is_Flip_h.stateChanged.connect(self.changeTitle)

    def changeNumOverlay(self, value):
        self.num_overlay.display(value + 1)
        self.num_overlay_count = value


    def changeOverlaySize(self, value):
        self.overlay_size.display(value + 1)
        self.overlay_size_count = value


    def changeNumCreate(self, value):
        self.num_create.display(value + 1)
        self.num_create_count = value


    def paintEvent(self, event):
        painter = QPainter(self)

        mainImage = QPixmap(self.main_image)
        subImage = QPixmap(self.overlay_image)
        painter.drawPixmap(0, 0, 640, 360, mainImage)
        painter.drawPixmap(0, 0, 60, 60, subImage)

        pen = QPen(Qt.red, 3)
        painter.setPen(pen)
        if len(self.points) > 3:
            painter.drawLine(self.points[0], self.points[1])
            painter.drawLine(self.points[1], self.points[2])
            painter.drawLine(self.points[2], self.points[3])
            painter.drawLine(self.points[3], self.points[0])


    def mousePressEvent(self, event):
        self.points.append(event.pos())
        self.update()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.points = []
            self.update()


    def createImage(self, path):
        mainImage = cv2.imread(self.main_image)
        subImage = cv2.imread(self.overlay_image)

        height, width = subImage.shape[:2]
        mainImage[:height, :width] = subImage

        cv2.imwrite(path, mainImage)


    def openMainImage(self):
        filename = QFileDialog.getOpenFileName()
        imagePath = filename[0]
        self.main_image = imagePath
        self.update()


    def openSubImage(self):
        filename = QFileDialog.getOpenFileName()
        imagePath = filename[0]
        self.overlay_image = imagePath
        self.update()


    def outputImage(self):
        dirname = QFileDialog.getExistingDirectory()
        save_name = os.path.join(dirname, 'test.jpg')
        self.createImage(save_name)


def main(args):
    app = QApplication(sys.argv)
    ex = Example(args.path)
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--path', type=str, default = None)

    main(parser.parse_args())
