import os
from pathlib import Path

import numpy as np
from PIL import Image
import pydicom


def conv_dcm(path_img, path_jpg):
    """
    Сохранение изображения из файлов dcm в jpg
    :param path_img: полный путь файлов dcm
    :param path_jpg: полный путь куда сохранять jpg
    :return:
    """
    # directory = os.fsdecode(os.fsencode(os.path.dirname(os.path.realpath(__file__)))) + '\\' + path_img
    # directory_jpg = os.fsdecode(os.fsencode(os.path.dirname(os.path.realpath(__file__)))) + '\\' + path_jpg
    Path(path_img).mkdir(parents=True, exist_ok=True)
    Path(path_jpg).mkdir(parents=True, exist_ok=True)
    j = 0
    for file in os.listdir(path_img):
        filename = os.fsdecode(file)
        if filename.endswith(".dcm"):
            open_filename = path_img + '\\' + filename
            name_file = ''.join(filename.split('.')[0:-1])
            ds = pydicom.dcmread(open_filename)
            new_image = ds.pixel_array.astype(float)
            scaled_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0
            scaled_image = np.uint8(scaled_image)
            final_image = Image.fromarray(scaled_image)
            # final_image.show()
            final_image.save(path_jpg + '\\' + name_file + '.jpg')
            j += 1
        else:
            continue
    print(f'Конвертация {j} изображений завершена!')


if __name__ == '__main__':
    conv_dcm(f'{os.path.dirname(os.path.realpath(__file__))}/dicom_img',
             f'{os.path.dirname(os.path.realpath(__file__))}/dicom_jpg')
