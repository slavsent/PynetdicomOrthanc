import os
from pathlib import Path

import numpy as np
from PIL import Image
import pydicom


def create_dcm_new(path_img, path_img_new):
    """
    Создание новой серии из старой с переворотом изображения на 90 градусов
    :param path_img: где храняться dcm
    :param path_img_new: куда сохранить новую серию
    :return:
    """
    Path(path_img).mkdir(parents=True, exist_ok=True)
    Path(path_img_new).mkdir(parents=True, exist_ok=True)
    #directory = os.fsdecode(os.fsencode(os.path.dirname(os.path.realpath(__file__)))) + '\\' + path_img
    #directory_new = os.fsdecode(os.fsencode(os.path.dirname(os.path.realpath(__file__)))) + '\\' + path_img_new
    new_study = pydicom.uid.generate_uid()
    new_series = pydicom.uid.generate_uid()
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
            ds.StudyInstanceUID = new_study
            ds.SeriesInstanceUID = new_series
            ds.save_as(path_img_new + '\\' + name_file + '_new.dcm')
        else:
            continue


if __name__ == '__main__':
    #create_dcm_new('narabotki/dicom_img', 'narabotki/dicom_img_new')
    create_dcm_new(f'{os.path.dirname(os.path.realpath(__file__))}/dicom_img',
             f'{os.path.dirname(os.path.realpath(__file__))}/dicom_new_img')
