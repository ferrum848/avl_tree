import cv2

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np

import utils
import math
from skimage.measure import label

from base_viewer import BaseViewer

COLOR_UNKNOWN = (128, 128, 128)
COLOR_FG = (0, 255, 0)
COLOR_BG = (0, 0, 0)


class PhotoViewer(BaseViewer):

    def __init__(self, parent, window):
        super().__init__(parent, window)
        self.window = window
        self.parent = parent
        self.zoom = 1.0
        self.pos_00 = [0, 0]
        self.zoom_hw = (None, None)
        self.image = None

        self.image_orig = None
        self.image_trimap = None

        self.move_shift = [0, 0]

        self.draw_mode = False
        self.fill_mode = False
        #self.move_point = False

        self.res_image = None

        self.start_x = 0
        self.start_y = 0
        self.list_of_points = []
        self.target = None

    def setPhoto(self, image):
        super().setPhoto(image)
        self.image_trimap = np.zeros(self.image_orig.shape, dtype=np.uint8)

    def clear_trimap(self):
        self.image_trimap = np.zeros(self.image_orig.shape, dtype=np.uint8)
        self.contruct_visualization_image()
        self.list_of_points = []

    def get_brush_color(self):
        if self.window.brush_unk.isChecked():
            return COLOR_UNKNOWN
        if self.window.brush_fg.isChecked():
            return COLOR_FG
        if self.window.brush_bg.isChecked():
            return COLOR_BG

    def draw_on_trimap(self, r, c, y, x):
        r, c = self.widget_to_img_pos(r, c)
        y, x = self.widget_to_img_pos(y, x)
        color = self.get_brush_color()
        if r == y and c == x:
            self.image_trimap = cv2.circle(self.image_trimap, (c, r), self.window.brush_size_box.value(), color, -1)
            self.list_of_points.append((c, r, self.window.brush_size_box.value()))
            print(self.list_of_points)
        else:
            self.image_trimap = cv2.line(self.image_trimap, (x, y), (c, r), color, self.window.brush_size_box.value() * 2)
        self.contruct_visualization_image()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.buttons() == Qt.LeftButton:
            if self.fill_mode is True and not self.window.brush_move_point.isChecked():
                self.fill(event.pos().y(), event.pos().x())
            elif self.window.brush_move_point.isChecked():
                cursor_coord_x, cursor_coord_y = self.widget_to_img_pos(event.pos().x(), event.pos().y())
                for point in self.list_of_points:
                    point_distance = ((cursor_coord_x - point[0])**2 + (cursor_coord_y - point[1])**2)**0.5
                    if point_distance <= point[2]:
                        self.target = point
                        break
                print(self.target)

            else:
                self.draw_mode = True
                self.start_x = event.pos().x()
                self.start_y = event.pos().y()
                self.draw_on_trimap(event.pos().y(), event.pos().x(), self.start_y, self.start_x)
        elif event.buttons() == Qt.RightButton:
            print(self.image_orig.shape)
            print(self.image_trimap.shape)

    def mouseMoveEvent(self, event):
        if self.draw_mode is True:
            self.draw_on_trimap(event.pos().y(), event.pos().x(), self.start_y, self.start_x)
            self.start_x = event.pos().x()
            self.start_y = event.pos().y()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.draw_mode = False
        if self.window.brush_move_point.isChecked():
            new_point_coord = self.widget_to_img_pos(event.pos().x(), event.pos().y())
            if self.target:
                self.list_of_points.append((new_point_coord[0], new_point_coord[1], self.target[2]))
                self.list_of_points.remove(self.target)
                # re-draw points here
                color = self.get_brush_color()
                point_size = self.target[2]
                mask_for_del_point = np.zeros(self.image_orig.shape, dtype=np.uint8)
                mask_for_del_point = cv2.circle(mask_for_del_point, (self.target[0], self.target[1]), self.target[2],
                                                (1, 1, 1), -1)
                mask_for_del_point *= self.image_orig
                self.image_trimap = cv2.circle(self.image_trimap, (self.target[0], self.target[1]), self.target[2],
                                                (0, 0, 0), -1)
                self.image_trimap += mask_for_del_point
                self.image_trimap = cv2.circle(self.image_trimap, (new_point_coord[0], new_point_coord[1]), point_size,
                                               color, -1)
                self.target = None
        self.contruct_visualization_image()

    def contruct_visualization_image(self):
        if self.image_orig is None:
            return
        self.image = self.image_orig.copy()

        if self.window.radio_image.isChecked():
            self.image = self.image_orig.copy()
        # elif self.window.radio_extract.isChecked() and self.image_alpha is not None:
        #     alpha_pred = self.image_alpha / 255.
        #     bg_mask = (alpha_pred == 0).astype(np.float32)
        #
        #     alpha_pred = np.repeat(np.expand_dims(alpha_pred, 2), 3, axis=2)
        #     bg_mask = np.repeat(np.expand_dims(bg_mask, 2), 3, axis=2)
        #
        #     self.image = (self.window.extract_slider.value() / 100.0 * bg_mask * self.image_orig  + alpha_pred * self.image_orig).astype(np.uint8)
        # else:
        #     self.image = np.repeat(np.expand_dims(self.image_alpha, 2), 3, axis=2)

        if self.window.show_trimap_checkbox.isChecked():
            trimap_overlay = ((self.image_trimap[:, :, 0] != 0) | (self.image_trimap[:, :, 1] != 0) | (self.image_trimap[:, :, 2] != 0)).astype(np.float32) \
                             * self.window.trimap_transp.value() / 100.0
            trimap_overlay = np.repeat(np.expand_dims(trimap_overlay, 2), 3, axis=2)
            self.image = self.image * (1.0 - trimap_overlay) + trimap_overlay * self.image_trimap
            self.image = self.image.astype(np.uint8)

        self.res_image = None
        self.update()

        if self.window.auto_predict.isChecked():
            self.parent.predict()

    def fill(self, r, c):
        r, c = self.widget_to_img_pos(r, c)
        connected_components, num = label(self.image_trimap, background=1000, return_num=True)
        color = self.get_brush_color()
        component = (connected_components == connected_components[r, c]).astype(np.uint8)
        self.image_trimap = (self.image_trimap * (1 - component) + color * component).astype(np.uint8)
        self.fill_mode = False
        self.contruct_visualization_image()

    def trimap_fill_object(self):
        self.fill_mode = True

    #def trimap_move_point(self):
        #self.move_point = True

    def predict(self):
        trimap = self.image_trimap.copy()
        trimap[np.where((trimap == [0, 255, 0]).all(axis=2))] = [255, 255, 255]

        cv2.imwrite('/data_encnet/original_img.png', self.image_orig)
        cv2.imwrite('/data_encnet/original_trimap.png', trimap)

        trimap_mask = ((trimap[:, :, 0] != 0) | (trimap[:, :, 1] != 0) | (trimap[:, :, 2] != 0)).astype(np.float32)

        image_alpha = np.zeros(self.image_orig.shape[:2], dtype=np.uint8)

        # Comment it
        #image_alpha = cv2.imread('/src/v2/BALER_MASK.png', cv2.IMREAD_GRAYSCALE)

        if trimap_mask.max() == 0:
            return image_alpha

        i, j = np.where(trimap_mask)
        r0 = min(i)
        r1 = max(i) + 1
        pad_pixels_height = math.ceil((r1 - r0) * 0.2)

        c0 = min(j)
        c1 = max(j) + 1
        pad_pixels_width = math.ceil((c1 - c0) * 0.2)

        r0 = max(0, r0 - pad_pixels_height)
        r1 = min(self.image_orig.shape[0], r1 + pad_pixels_height)

        c0 = max(0, c0 - pad_pixels_width)
        c1 = min(self.image_orig.shape[1], c1 + pad_pixels_width)

        indices = np.meshgrid(np.arange(r0, r1), np.arange(c0, c1), indexing='ij')
        img_crop = self.image_orig[indices]

        trimap_crop = trimap[indices]

        # Uncomment it
        pred = utils.predict_distr(img_crop, trimap_crop, 'http://localhost:7777')
        #h, w = img_crop.shape[:2]
        #pred = cv2.resize(pred.copy(), (w, h), interpolation=cv2.INTER_CUBIC)
        image_alpha[r0: r1, c0:c1] = pred

        # Stay commented
        # image_alpha = np.repeat(np.expand_dims(image_alpha, 2), 3, 2)

        return image_alpha

