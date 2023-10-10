import os
from pathlib import Path

from convert_dicom import conv_dcm
from find_dicom import read_dcm
from creat_dicom_new import create_dcm_new
from create_dicom import create_dcm
from send_dicom import send_dcm


def main_new():
    """
    Работа модулей  по порядку:
    Поиск и сохранение данных
    Поворот изображений сохраненной серии и создание новой серии
    Отправка новой серии на сервер
    :return:
    """
    print('Начало - поиск иследований по модальности MG и сохранение данных первой серии....')
    Path(f"{os.path.dirname(os.path.realpath(__file__))}/dicom_img").mkdir(parents=True, exist_ok=True)
    dir_name = f'{os.path.dirname(os.path.realpath(__file__))}/dicom_img'
    read_dcm(dir_name)

    print('Конвертация файлов dcm в jpg....')
    dir_for_dcm = 'dicom_img'
    Path(f"{os.path.dirname(os.path.realpath(__file__))}/{dir_for_dcm}").mkdir(parents=True, exist_ok=True)
    dir_for_jpg = 'dicom_jpg'
    Path(f"{os.path.dirname(os.path.realpath(__file__))}/{dir_for_jpg}").mkdir(parents=True, exist_ok=True)
    conv_dcm(f"{os.path.dirname(os.path.realpath(__file__))}/{dir_for_dcm}",
             f"{os.path.dirname(os.path.realpath(__file__))}/{dir_for_jpg}")

    print('Начался переворот на 90 градусов изображений в dcm и сохранение в новую серию....')
    dir_for_dcm = 'dicom_img'
    Path(f"{os.path.dirname(os.path.realpath(__file__))}/{dir_for_dcm}").mkdir(parents=True, exist_ok=True)
    dir_to_dcm = 'dicom_img_new'
    Path(f"{os.path.dirname(os.path.realpath(__file__))}/{dir_to_dcm}").mkdir(parents=True, exist_ok=True)
    create_dcm_new(f"{os.path.dirname(os.path.realpath(__file__))}/{dir_for_dcm}",
                   f"{os.path.dirname(os.path.realpath(__file__))}/{dir_to_dcm}")

    print('Передача на сервер файлов dcm.....')
    dir_for_dcm = 'dicom_img_new'
    Path(f"{os.path.dirname(os.path.realpath(__file__))}/{dir_for_dcm}").mkdir(parents=True, exist_ok=True)
    send_dcm(f"{os.path.dirname(os.path.realpath(__file__))}/{dir_for_dcm}")

    print('Выполнение модуля завершено!')


if __name__ == '__main__':
    main_new()
