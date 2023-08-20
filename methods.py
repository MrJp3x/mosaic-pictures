import cv2
import numpy as np
from math import sqrt
from sys import maxsize
from os import listdir
from time import time


# import glob


class mosaic:
    """
    default directory path format is './Pics'.
    It is better to use the same format so that you do not encounter an error.

    "Pics" file has a main photo and a directory where mosaic images are located.

    It is emphasized again, it is better to follow this method so as not to encounter an error.
    """

    def __init__(self, directory_path: str = './Pics', mosaic_width_size: int = 4, mosaic_height_size: int = 4) -> None:
        self.start_time = time()  # start image processing
        self.mosaic_height_size = mosaic_height_size
        self.mosaic_width_size = mosaic_width_size
        self.directory_path = directory_path
        self._mosaic_pics_dir = f'{self.directory_path}/mosaic_pics'
        # { The variables below are defined and initialized in the constructor function و
        # so that they can be used in other methods in the continuation of the algorithm.
        self.end_time = None
        self.W = None  # 2
        self.H = None  # 2
        self.mosaics_average_get_label = None
        self.main_pic_cropped_average_channels = None
        self.main_pic_cropped = None
        # }
        # It reads the original image and converts it into an array
        self.main_pic = cv2.imread(f'Pics/{self._get_picture_name()}')

        # we need that when proccessing is ended , then we resize final  picture to first size
        self._main_pic_first_H_shape = self.main_pic.shape[0]
        self._main_pic_first_W_shape = self.main_pic.shape[1]
        self._mosaic_pics_dir = f'{self.directory_path}/mosaic_pics'

        # mosaic pictures are in a directory, it for to there and read that's
        self.list_Of_mosaic_pics = self.list_of_mosaic_pics_maker()
        self.list_Of_mosaic_pics_resized = self.resize_all_mosaic_pics()
        # ========..:: updating ::.. ==========
        self.run()

    def run(self):
        self.mosaic_picture_resize_calculate()
        self.calculate_number_of_mosaic()
        self.main_pic_cropped = self.crop()
        self.main_pic_cropped_average_channels = self.average_mosaics_channels(self.main_pic_cropped)
        self.mosaics_average_get_label = self.calculate_all_mosaic_average(self.list_Of_mosaic_pics_resized)
        self.replace_pic_with_mosaics()
        self.main_pic = self._merge()
        self.main_pic = self._resize_pic(self.main_pic, self._main_pic_first_W_shape, self._main_pic_first_H_shape)

        self.end_time = time()  # End of image processing

    def get_final_pic(self):
        return self.main_pic

    def show_image(self, im_title='..:: Final Picture ::..'):
        cv2.imshow(im_title, self.main_pic)
        cv2.waitKey()

    def _get_picture_name(self) -> str:
        """
        check in user directory, main picture is exist or not.
        if not exist, app get raise.
        :return:
        """
        main_path_files = listdir(self.directory_path)
        for file in main_path_files:
            if file[-3:] in ['jpg', 'png']:  # if file format is png or jpg, program is working
                return file
        else:
            raise FileNotFoundError('\'.png\' or \'.jpg\' file is not defined.')

    def list_of_mosaic_pics_maker(self) -> list:
        """
        First, it goes to the directory of mosaic images and then reads them and puts them in a list.
        In the end, returns them.
        :return:
        """
        _get_pics_into_mosaic_dir_pic = listdir(
            f'{self.directory_path}/mosaic_pics')  # always in 'Pics' directory,  we have 'mosaic_pics' directory
        return [cv2.imread(f'Pics/mosaic_pics/{pic}') for pic in _get_pics_into_mosaic_dir_pic]

    def mosaic_picture_resize_calculate(self) -> None:
        width, height = self.main_pic.shape[1], self.main_pic.shape[0]
        if (width % self.mosaic_width_size) != 0:
            width = int(width / self.mosaic_width_size)
            width *= self.mosaic_width_size

        if (height % self.mosaic_height_size) != 0:
            height = int(height / self.mosaic_height_size)
            height *= self.mosaic_height_size

        self.main_pic = cv2.resize(self.main_pic, dsize=(width, height))
        # resize main pic to balance width and height (updating main pic)

    def calculate_number_of_mosaic(self):
        original_width = self.main_pic.shape[1]
        original_height = self.main_pic.shape[0]

        self.W = original_width // self.mosaic_width_size
        self.H = original_height // self.mosaic_height_size

    def crop(self) -> list:
        cropped_list = []
        for i in range(self.H):
            for j in range(self.W):
                save = self.main_pic[i * self.mosaic_height_size:(i + 1) * self.mosaic_height_size,
                       j * self.mosaic_width_size: (j + 1) * self.mosaic_width_size]
                cropped_list.append(save)
        return cropped_list

    @staticmethod
    def _resize_pic(pic: np.ndarray, width, height) -> list:
        dim = (width, height)
        resized_pic = cv2.resize(pic, dsize=dim)
        return resized_pic

    def resize_all_mosaic_pics(self) -> list:
        """
        resize all mosaic pictures and save them into the list.
        finally return that.
        :return:
        """
        resized_pics_list = []
        width, height = self.mosaic_width_size, self.mosaic_height_size  # for simplicity

        for pic in self.list_Of_mosaic_pics:
            resized = self._resize_pic(pic, width, height)
            resized_pics_list.append(resized)

        return resized_pics_list

    @staticmethod
    def average_mosaics_channels(mosaic_pics_list) -> list:
        """
        get mosaic picture and solve average
        :param mosaic_pics_list:
        :return:
        """
        average_list = []
        for pic in mosaic_pics_list:
            b, g, r = cv2.split(pic)
            meanB = b.mean()
            meanG = g.mean()
            meanR = r.mean()
            average_list.append([meanB, meanG, meanR])

        return average_list

    def calculate_all_mosaic_average(self, pic_list: list) -> dict:
        average_dict = {}
        for i in range(len(pic_list)):
            average_dict[f'{i}'] = self.average_mosaics_channels(pic_list)[i]

        return average_dict

    def replace_pic_with_mosaics(self) -> list:
        """
        Calculating the difference of color channels
        between a piece (mosaic) of the original image and resized mosaic images (using Norm 2).
        Then, the photo with the smallest distance is stored in a list,
        to be replaced with a dictionary containing labeled mosaic images (dictionary key) in the next steps.
        :return:
        """
        minimum = maxsize
        changed_picture_list = []
        save_label = 0
        mosaic_dict = self.mosaics_average_get_label
        main_pic_list = self.main_pic_cropped_average_channels
        for i in main_pic_list:
            for label, mos_avg in mosaic_dict.items():
                avg_difference = sqrt(
                    ((i[0] - mos_avg[0]) ** 2) + ((i[1] - mos_avg[1]) ** 2) + ((i[2] - mos_avg[2]) ** 2))
                if avg_difference < minimum:
                    minimum = avg_difference
                    save_label = label
            changed_picture_list.append(self.list_Of_mosaic_pics_resized[int(save_label)])
            minimum = maxsize

        return changed_picture_list

    def _merge(self):
        line_list = []
        CPL = self.replace_pic_with_mosaics()
        line = CPL[0]
        for i in range(1, len(CPL)):
            if (i % self.W) == 0:
                line_list.append(line)
                line = CPL[i]
            else:
                line = np.hstack((line, CPL[i]))
        line_list.append(line)
        final_pic = []
        Fline = line_list[0]
        for j in range(1, self.H):
            Fline = np.vstack((Fline, line_list[j]))
        final_pic.append(Fline)
        return final_pic[0]

    def cpu_time(self) -> float:
        """
        Calculation of CPU engagement time when applying the mosaic algorithm on the target image.
        :return:
        """
        return self.end_time - self.start_time
