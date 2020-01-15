import numpy as np
import cv2
import fitz
import os


def match_template(img_path, temp_path, val):
    """
    模板匹配
    :param img_path: 图片路径
    :param temp_path: 模板路径
    :param val: 阈值
    :return: 匹配的坐标
    pip install numpy
    pip install opencv-python
    """
    img = cv2.imread(img_path)
    temp = cv2.imread(temp_path)
    if len(img.shape) > 2:
        im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        im_gray = img.copy()
    temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
    temps = temp.copy()

    t_h, t_w = temp.shape[:2]
    res = cv2.matchTemplate(im_gray, temps, cv2.TM_CCOEFF_NORMED)

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


def pdf2img(pdf_path, img_path):
    """
    PDF>>PNG
    :param pdf_path:
    :param img_path:
    :return:
    pip install pymupdf
    """
    pdf_doc = fitz.open(pdf_path)
    for pg in range(pdf_doc.pageCount):
        page = pdf_doc[pg]
        rotate = int(0)
        zoom_x = 1
        zoom_y = 1
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)

        if not os.path.exists(img_path):
            os.makedirs(img_path)

        img_name = ".".join(os.path.basename(pdf_path).split(".")[:-1]) + "_" + str(pg + 1) + ".png"
        pix.writePNG(os.path.join(img_path, img_name))


if __name__ == '__main__':
    pdf = "/Users/c/Desktop/123.pdf"
    img = "/Users/c/Desktop/img"
    pdf2img(pdf, img)
