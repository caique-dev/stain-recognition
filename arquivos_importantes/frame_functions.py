from arquivos_importantes.general_functions import *

import numpy as np
from PIL import Image as im
from PIL import ImageDraw
import scipy as sp

class Frame():
    marked_content_folder = '/home/caique/unicamp/f359/maked_stain_expansion_videos'
    def __init__(self, image_path):
        self.name = getting_archive_name(image_path)
        self.original_image = im.open(image_path)
        self.image_with_analisys_line = self.original_image
        self.original_image_vector = np.array(self.original_image)
        self.gray_image_vector = np.array(self.original_image.convert('L'))

        self.n_lines, self.n_columns = self.gray_image_vector.shape

        self.start_stain, self.end_stain = 0, 0

    def show(self, version=''):
        match version:
            case 'gray':
                im.fromarray(self.gray_image_vector).show()
            
            case 'original':
                self.original_image.show()
            
            case _:
                self.image_with_analisys_line.show()

    def marking_the_stain(self, analized_line):   
        # marking the line of analisys in the image
        draw = ImageDraw.Draw(self.image_with_analisys_line)
        # horizontal line
        draw.line((0, analized_line, self.n_columns, analized_line), fill='white', width=3)

        # start stain
        draw.line((self.start_stain, 0, self.start_stain, self.n_lines), fill=(102, 255, 51), width=3)

        # end stain
        draw.line((self.end_stain, 0, self.end_stain, self.n_lines), fill=(102, 255, 51), width=3)
        
    def getting_intensity_vector(self):
        """
            returns the luminance of the analized line
        """
        y_axis = []
        x_axis = []

        # filling in the y_axis
        n_lines, n_columns = self.gray_image_vector.shape
        middle_line = n_lines // 2
        for column in range(n_columns):
            y_axis.append(self.gray_image_vector[middle_line][column])

        y_axis = np.asarray(y_axis)
        
        # getting the number of pixel of the first column of video matrix
        x_axis = np.asarray([i for i in range(len(self.original_image_vector[0]))])

        # softening y_axis
        b, a = sp.signal.butter(1, [.01, 0.1], btype='bandpass')
        filtered_y_axis= sp.signal.filtfilt(b, a, y_axis, padlen=150)

        return x_axis, y_axis, filtered_y_axis    

    def radio_growth_rate(delD_vec, frame_interval, conversion_constant=1):
        speed_rate_vec = []
        for D in delD_vec:
            speed_rate = (D * conversion_constant)/frame_interval
            speed_rate_vec.append(speed_rate)

        return speed_rate_vec
    
    def saving_marked_image(self, source_video):
        # creating the folder
        folder_path = create_folder(f'{Frame.marked_content_folder }/{source_video}')

        frame_name = (f'marked_frame{frame_number(self.name):04d}.jpg')

        # saving
        self.image_with_analisys_line.save(f'{folder_path}/{frame_name}')

        # success message
        print(f'{folder_path}/{frame_name} saved with success')

    # setters
    def set_startstain(self, start):
        self.start_stain = start

    def set_endstain(self, end):
        self.end_stain = end