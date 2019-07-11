from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from photo_viewer import PhotoViewer
from result_viewer import ResultViewer


class DoubleViewer(QLabel):

    def __init__(self, window):
        super().__init__(window)
        self.left_viewer = PhotoViewer(self, window)
        self.right_viewer = ResultViewer(self, window)

        # Debug styling
        self.setStyleSheet("border: 2px solid gray")
        self.left_viewer.setStyleSheet("border: 2px solid blue")
        self.right_viewer.setStyleSheet("border: 2px solid green")

        self.left_viewer.setUpdatesEnabled(True)
        self.right_viewer.setUpdatesEnabled(True)

        layout = QHBoxLayout(self)
        layout.addWidget(self.left_viewer)
        layout.addWidget(self.right_viewer)
        self.setLayout(layout)

        # For zoom and position synchronization
        self.left_viewer.zoom_changed.connect(self.on_zoom_changed)
        self.right_viewer.zoom_changed.connect(self.on_zoom_changed)

        self.left_viewer.move_drag.connect(self.on_zoom_changed)
        self.right_viewer.move_drag.connect(self.on_zoom_changed)

    def contruct_visualization_image(self):
        self.left_viewer.contruct_visualization_image()
        self.right_viewer.contruct_visualization_image()

    def clear_trimap(self):
        self.left_viewer.clear_trimap()
        self.right_viewer.clear_trimap()

    def trimap_fill_object(self):
        self.left_viewer.trimap_fill_object()
        self.right_viewer.trimap_fill_object()

    #def trimap_move_point(self):
        #self.left_viewer.trimap_move_point()

    def predict(self):
        mask_image = self.left_viewer.predict()
        self.right_viewer.set_mask_image(mask_image)
        self.update()

    def setPhoto(self, image):
        self.left_viewer.setPhoto(image)
        self.right_viewer.setPhoto(image)
        self.update()

    def on_zoom_changed(self, zoom, pos00):
        self.left_viewer.zoom_hw = zoom
        self.right_viewer.zoom_hw = zoom
        self.left_viewer.pos_00 = pos00
        self.right_viewer.pos_00 = pos00
        self.update()