import os
from pathlib import Path

import numpy as np
from PIL import Image
import pydicom


def create_dcm(path_img):
    """
    переворот изображения в dcm и сохранение в туже серию
    :param path_img: путь файлов dcm
    :return:
    """
    Path(path_img).mkdir(parents=True, exist_ok=True)
    #directory = os.fsdecode(os.fsencode(os.path.dirname(os.path.realpath(__file__)))) + '\\' + path_img
    for file in os.listdir(path_img):
        filename = os.fsdecode(file)
        if filename.endswith(".dcm"):
            open_filename = os.path.join(path_img, filename)
            ds = pydicom.dcmread(open_filename, force=True)
            ds.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
            #print(ds.PatientID, ds.StudyDate, ds.Modality)
            name_file = ''.join(filename.split('.')[0:-1])
            data_img = Image.fromarray(ds.pixel_array)
            data_img_rotated = data_img.rotate(angle=90, resample=Image.BICUBIC, fillcolor=data_img.getpixel((0, 0)))

            data_rotated = np.array(data_img_rotated, dtype=np.int16)
            ds.PixelData = data_rotated.tobytes()
            ds.Rows, ds.Columns = data_rotated.shape

            ds.save_as(path_img + '\\' + name_file + '_new.dcm')
        else:
            continue


if __name__ == '__main__':
    create_dcm(f'{os.path.dirname(os.path.realpath(__file__))}/dicom_img')
