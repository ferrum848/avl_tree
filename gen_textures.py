import cv2, os, random
import numpy as np


def gen_texture():
    color_scatter = 30
    color = [random.randrange(color_scatter, 255 - color_scatter) for i in range(3)]
    mask_size = (500, 500, 3)
    mask = np.ones(mask_size, dtype=np.uint8)
    step_size = random.randint(mask_size[0]//100, mask_size[0]//25)
    type_of_image = random.choice([0, 1])
    if type_of_image == 0:
        for step in range(0, mask_size[0], step_size):
            for step2 in range(0, mask_size[1], step_size):
                temp_color = []
                for i in range(3):
                    temp_color.append(random.randint(color[i] - color_scatter, color[i] + color_scatter))
                temp_color = np.asarray(temp_color, dtype=np.uint8)
                mask[step : step + step_size, step2 : step2 + step_size] += temp_color
    else:
        colomn_count = random.randint(4, mask_size[1]//50)
        colomn_step = mask_size[1]//colomn_count
        mask_lost_size = (500, 1000, 3)
        mask_lost = np.ones(mask_lost_size, dtype=np.uint8)
        color2 = [random.randrange(color_scatter, 255 - color_scatter) for i in range(3)]
        mask_colomn1 = np.ones((mask_size[0], colomn_step, 3), dtype=np.uint8)
        mask_colomn2 = np.ones((mask_size[0], colomn_step, 3), dtype=np.uint8)
        for step in range(0, mask_colomn1.shape[0], step_size):
            for step2 in range(0, mask_colomn1.shape[1], step_size):
                temp_color1, temp_color2 = [], []
                for i in range(3):
                    temp_color1.append(random.randint(color[i] - color_scatter, color[i] + color_scatter))
                    temp_color2.append(random.randint(color2[i] - color_scatter, color2[i] + color_scatter))
                temp_color1 = np.asarray(temp_color1, dtype=np.uint8)
                temp_color2 = np.asarray(temp_color2, dtype=np.uint8)
                mask_colomn1[step : step + step_size, step2 : step2 + step_size] += temp_color1
                mask_colomn2[step: step + step_size, step2: step2 + step_size] += temp_color2
        for res in range(0, mask_lost_size[1] - colomn_step, colomn_step * 2):
            mask_lost[:, res: res + colomn_step] += mask_colomn1
            mask_lost[:, res + colomn_step: res + 2 * colomn_step] += mask_colomn2
        bias = random.randint(0, colomn_step)
        mask = mask_lost[:, bias:mask_size[1] + bias]

    blur_step = random.choice([i for i in range(19, 39, 2)])
    result = cv2.medianBlur(mask, blur_step)
    return result


im = gen_texture()
cv2.imwrite('m.png', im)
