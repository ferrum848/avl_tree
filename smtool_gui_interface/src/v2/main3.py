from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import utils

from double_viewer import DoubleViewer



class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.viewer = DoubleViewer(self)
        self.viewer.setUpdatesEnabled(True)
        # 'Load image' button
        self.btnLoad = QToolButton()
        self.btnLoad.setText('Load image')
        self.btnLoad.clicked.connect(self.loadImage)

        #alpha group
        self.radio_image = QRadioButton("Image")
        self.radio_image.clicked.connect(self.viewer.contruct_visualization_image)
        self.radio_image.setChecked(True)
        self.radio_extract = QRadioButton("Extract")
        self.radio_extract.clicked.connect(self.viewer.contruct_visualization_image)
        self.radio_alpha = QRadioButton("Alpha")
        self.radio_alpha.clicked.connect(self.viewer.contruct_visualization_image)
        self.extract_slider = QSlider(Qt.Horizontal)
        self.extract_slider.setMinimum(0)
        self.extract_slider.setMaximum(100)
        self.extract_slider.setTickInterval(1)
        self.extract_slider.setValue(0)
        self.extract_slider.sliderReleased.connect(self.viewer.contruct_visualization_image)

        self.radio_image.setEnabled(False)
        self.radio_extract.setEnabled(False)
        self.radio_alpha.setEnabled(False)
        self.extract_slider.setEnabled(False)

        line_01 = QFrame()
        line_01.setFrameShape(QFrame.VLine)

        alpha_layout = QHBoxLayout()
        alpha_layout.addWidget(self.radio_image)
        alpha_layout.addWidget(self.radio_extract)
        alpha_layout.addWidget(self.extract_slider)
        alpha_layout.addWidget(line_01)
        alpha_layout.addWidget(self.radio_alpha)
        alpha_group = QGroupBox("Alpha")
        alpha_group.setLayout(alpha_layout)

        # trimap group
        self.show_trimap_checkbox = QCheckBox("Show trimap")
        self.show_trimap_checkbox.setChecked(True)
        self.show_trimap_checkbox.clicked.connect(self.viewer.contruct_visualization_image)

        line_02 = QFrame()
        line_02.setFrameShape(QFrame.VLine)

        self.brush_size_box = QSpinBox()
        self.brush_size_box.setMinimum(1)
        self.brush_size_box.setMaximum(100)
        self.brush_size_box.setValue(25)

        brush_size_changer = QHBoxLayout()
        brush_size_changer.addWidget(QLabel("Brush size: "))
        brush_size_changer.addWidget(self.brush_size_box)

        line_03 = QFrame()
        line_03.setFrameShape(QFrame.VLine)

        self.brush_unk = QRadioButton("Unknown")
        self.brush_unk.setChecked(True)
        self.brush_fg = QRadioButton("Object")
        self.brush_bg = QRadioButton("Background")

        brush_modes = QHBoxLayout()
        brush_modes.addWidget(QLabel("Brush mode: "))
        brush_modes.addWidget(self.brush_unk)
        brush_modes.addWidget(self.brush_fg)
        brush_modes.addWidget(self.brush_bg)

        line_04 = QFrame()
        line_04.setFrameShape(QFrame.VLine)

        brush_clear = QPushButton("Clear")
        brush_clear.clicked.connect(self.viewer.clear_trimap)
        brush_fill_object = QPushButton("Fill object")
        brush_fill_object.clicked.connect(self.viewer.trimap_fill_object)
        self.brush_move_point = QCheckBox("Move point")
        self.brush_move_point.setChecked(False)
        #brush_move_point = QPushButton("Move point")
        #brush_move_point.clicked.connect(self.viewer.trimap_move_point)

        self.trimap_transp = QSlider(Qt.Horizontal)
        self.trimap_transp.setMinimum(0)
        self.trimap_transp.setMaximum(100)
        self.trimap_transp.setTickInterval(1)
        self.trimap_transp.setValue(50)
        self.trimap_transp.sliderReleased.connect(self.viewer.left_viewer.contruct_visualization_image)

        trimap_layout = QHBoxLayout()
        trimap_layout.addWidget(self.show_trimap_checkbox)
        trimap_layout.addWidget(QLabel("transparency"))
        trimap_layout.addWidget(self.trimap_transp)
        trimap_layout.addWidget(line_02)
        trimap_layout.addLayout(brush_size_changer)
        trimap_layout.addWidget(line_03)
        trimap_layout.addLayout(brush_modes)
        trimap_layout.addWidget(line_04)
        trimap_layout.addWidget(brush_clear)
        trimap_layout.addWidget(brush_fill_object)
        #trimap_layout.addWidget(brush_move_point)
        trimap_layout.addWidget(self.brush_move_point)

        trimap_group = QGroupBox("Trimap")
        trimap_group.setLayout(trimap_layout)

        # prediction group
        self.auto_predict = QCheckBox("Auto")
        self.auto_predict.setChecked(False)


        predict = QPushButton("Predict")
        predict.clicked.connect(self.viewer.predict)

        predict_layout = QHBoxLayout()
        predict_layout.addWidget(predict)
        predict_layout.addWidget(self.auto_predict)
        predict_group = QGroupBox("SmartTool")
        predict_group.setLayout(predict_layout)


        #instruments panel
        instrument_layout = QHBoxLayout()
        #instrument_layout.setAlignment(Qt.AlignLeft)
        instrument_layout.addWidget(alpha_group)
        instrument_layout.addWidget(trimap_group)
        instrument_layout.addWidget(predict_group)
        instrument_layout.addWidget(self.btnLoad)
        instrument_layout.addStretch(10000)

        #self.viewer.photoClicked.connect(self.photoClicked)
        # Arrange layout
        VBlayout = QVBoxLayout()
        VBlayout.addLayout(instrument_layout)
        VBlayout.addWidget(self.viewer)

        self.setLayout(VBlayout)

    def loadImage(self):
        new_image_path = QFileDialog.getOpenFileName(self, "Pick an image")[0]
        if utils.check_image_path(str(new_image_path)):
            self.viewer.setPhoto(utils.load_image(new_image_path))
            self.viewer.update()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.showMaximized()
    sys.exit(app.exec_())
