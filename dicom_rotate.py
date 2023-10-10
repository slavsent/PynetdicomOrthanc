import os
from PIL import Image


def rotate_imq(path_img):
    """
    Перевород на 90 градусов фалов jpg
    :param path_img: директория где файлы jpg
    :return:
    """
    directory = os.fsdecode(os.fsencode(os.path.dirname(os.path.realpath(__file__)))) + '\\' + path_img
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".JPG"):
            open_filename = directory+'\\' + filename
            im = Image.open(open_filename)

            im_rotate = im.rotate(90)
            im_rotate.save(open_filename, quality=95)
            im.close()
            continue
        else:
            continue


if __name__ == '__main__':
    rotate_imq('narabotki/dicom_img')
