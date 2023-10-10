import os
from pathlib import Path

from convert_dicom import conv_dcm
from find_dicom import read_dcm
from creat_dicom_new import create_dcm_new
from create_dicom import create_dcm
from send_dicom import send_dcm


def main():
    """
    Мению для работы с модулями
    :return:
    """
    while True:
        print('Выберите действие:')
        print('Поиск и загрузка иследований по модальности MG - 1')
        print('Конвертировать файлы dcm в jpg - 1')
        print('Переворот на 90 градусов изображения в dcm и сохранения в новую серию - 3')
        print('Переворот на 90 градусов изображения в dcm и сохранения в ту же серию - 4')
        print('Передача на сервер файлов dcm - 4')
        print('Для выхода введите 0')
        try:
            item_menu = int(input('Введите пункт пеню: '))
        except ValueError:
            continue
        else:
            if item_menu == 0:
                break
            elif item_menu == 1:
                dir_for_dcm = input('Введите директорию для сохранения найденных иследований: ')
                Path(f"{os.path.dirname(os.path.realpath(__file__))}/{dir_for_dcm}").mkdir(parents=True, exist_ok=True)
                dir_name = f'{os.path.dirname(os.path.realpath(__file__))}/{dir_for_dcm}'
                read_dcm(f"{os.path.dirname(os.path.realpath(__file__))}/{dir_for_dcm}")
            elif item_menu == 2:
                dir_for_dcm = input('Введите директорию хранения иследований: ')
                Path(f"{os.path.dirname(os.path.realpath(__file__))}/{dir_for_dcm}").mkdir(parents=True, exist_ok=True)
                dir_for_jpg = input('Введите директорию для хранения jpg фалов: ')
                Path(f"{os.path.dirname(os.path.realpath(__file__))}/{dir_for_jpg}").mkdir(parents=True, exist_ok=True)
                conv_dcm(f"{os.path.dirname(os.path.realpath(__file__))}/{dir_for_dcm}",
                         f"{os.path.dirname(os.path.realpath(__file__))}/{dir_for_jpg}")
            elif item_menu == 3:
                dir_for_dcm = input('Введите директорию хранения иследований: ')
                Path(f"{os.path.dirname(os.path.realpath(__file__))}/{dir_for_dcm}").mkdir(parents=True, exist_ok=True)
                dir_to_dcm = input('Введите директорию для сохранения новых фалов: ')
                Path(f"{os.path.dirname(os.path.realpath(__file__))}/{dir_to_dcm}").mkdir(parents=True, exist_ok=True)
                create_dcm_new(f"{os.path.dirname(os.path.realpath(__file__))}/{dir_for_dcm}",
                               f"{os.path.dirname(os.path.realpath(__file__))}/{dir_to_dcm}")
            elif item_menu == 4:
                dir_for_dcm = input('Введите директорию хранения иследований: ')
                Path(f"{os.path.dirname(os.path.realpath(__file__))}/{dir_for_dcm}").mkdir(parents=True, exist_ok=True)
                create_dcm(f"{os.path.dirname(os.path.realpath(__file__))}/{dir_for_dcm}")
            elif item_menu == 5:
                dir_for_dcm = input('Введите директорию хранения иследований: ')
                Path(f"{os.path.dirname(os.path.realpath(__file__))}/{dir_for_dcm}").mkdir(parents=True, exist_ok=True)
                send_dcm(f"{os.path.dirname(os.path.realpath(__file__))}/{dir_for_dcm}")
            else:
                print('Вы выбрали не существующий пункт меню')


if __name__ == '__main__':
    my_path = os.path.dirname(os.path.realpath(__file__))
    Path(f"{os.path.dirname(os.path.realpath(__file__))}/dicom_img").mkdir(parents=True, exist_ok=True)
    print('PyCharm')
