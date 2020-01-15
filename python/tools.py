import numpy as np
import cv2 as cv


def match_template(img, temp, val):
    """
    模板匹配
    :param img: 图片矩阵
    :param temp: 模板路径
    :param val: 阈值
    :return: 匹配的坐标
    """
    if len(img.shape) > 2:
        im_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    else:
        im_gray = img.copy()
    temp = cv.cvtColor(temp, cv.COLOR_BGR2GRAY)
    temps = temp.copy()

    t_h, t_w = temp.shape[:2]
    res = cv.matchTemplate(im_gray, temps, cv.TM_CCOEFF_NORMED)

    for _val in range(val, 100):
        threshold = _val / 100
        loc = np.where(res >= threshold)
        w_arr = []
        h_arr = []
        for pt in zip(*loc[::-1]):
            w_arr.append(pt[0])
            h_arr.append(pt[1])

        if len(w_arr) == 1:
            p_w = int(np.mean(w_arr, axis=0))
            p_h = int(np.mean(h_arr, axis=0))
            top_left = (p_w, p_h)
            bottom_right = top_left[0] + t_w, top_left[1] + t_h
            return top_left, bottom_right
