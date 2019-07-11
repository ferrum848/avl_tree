from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
from base_viewer import BaseViewer

COLOR_UNKNOWN = (128, 128, 128)
COLOR_FG = (0, 255, 0)
COLOR_BG = (0, 0, 0)
GRID_COLORS = [255, 220]


class ResultViewer(BaseViewer):

    def __init__(self, parent, window):
        super().__init__(parent, window)
        self.window = window
        self.zoom = 1.0
        self.pos_00 = [0, 0]
        self.zoom_hw = (None, None)
        self.image = None

        self.image_orig = None
        self.image_alpha = None

        self.move_shift = [0, 0]

        self.draw_mode = False
        self.fill_mode = False

        self.res_image = None

        self.start_x = 0
        self.start_y = 0

    def contruct_visualization_image(self):

        if self.image_orig is None:
            return

        if self.image_alpha is None:
            self.image = self.image_orig.copy()

        self.res_image = None
        self.update()

    def fill(self, r, c):
        r, c = self.widget_to_img_pos(r, c)
        from skimage.measure import label
        connected_components, num = label(self.image_trimap, background=1000, return_num=True)
        color = self.get_brush_color()
        component = (connected_components == connected_components[r, c]).astype(np.uint8)
        self.image_trimap = (self.image_trimap * (1 - component) + color * component).astype(np.uint8)
        self.fill_mode = False
        self.contruct_visualization_image()

    def trimap_fill_object(self):
        self.fill_mode = True

    def set_mask_image(self, mask):
        self.image_alpha = mask
        self.generate_mixed_image()

    def draw_alpha_grid(self, hw_size, block_size=25):
        image = np.zeros((hw_size[0], hw_size[1], 3), dtype=np.uint8)
        counter_y = counter_x = 0
        for i in range(0, hw_size[0], block_size):
            counter_y += 1
            for j in range(0, hw_size[1], block_size):
                counter_x += 1
                bottom = min(i + block_size, hw_size[0] - 1)
                right = min(j + block_size, hw_size[1] - 1)
                color = GRID_COLORS[(counter_y + counter_x) % 2]
                image[i:bottom, j:right, :] = color
        return image

    def generate_mixed_image(self):
        if self.image_orig is None:
            return

        self.image = self.draw_alpha_grid(self.image_orig.shape[:2])
        alpha_3c = np.repeat(np.expand_dims(self.image_alpha / 255.0, 2), 3, axis=2)
        self.image = (self.image * (1 - alpha_3c) + alpha_3c * self.image_orig).astype(np.uint8)

        self.res_image = None
        self.update()
