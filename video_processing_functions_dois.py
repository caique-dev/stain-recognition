import cv2 as cv
import os
import numpy as np
from PIL import Image as im
from matplotlib import pyplot as plt
import scipy as sp

class Video():
    videos_path = "/home/caique/unicamp/f359/diffusion_videos/";
    frames_mother_path = "/home/caique/unicamp/f359/videos_frames/";

    def __init__(self, video_name):
        self.frames_child_path = Video.frames_mother_path + video_name
        self.name = video_name
        self.video_target = cv.VideoCapture(Video.videos_path + video_name)

        # taking video infos
        self.fps = self.video_target.get(cv.CAP_PROP_FPS)
        self.frame_numbers = int(self.video_target.get(cv.CAP_PROP_FRAME_COUNT))
        self.duration = self.frame_numbers/self.fps
        self.frame_delt = self.duration/self.frame_numbers


    def separating_frames(self):
        """
            separating the video in frames and storage it
        """

        # creating a storege path
        if not os.path.exists(Video.frames_mother_path + self.name):
            os.mkdir(Video.frames_mother_path + self.name)

        counter = 0
        while (True):
            # reading from frame
            ret, frame = self.video_target.read()

            if ret:
                # if video still left, continue creating images
                name = self.frames_child_path + '/frame' + str(counter) + '.jpg'
                # show how many frames are created
                print("creating frame n°", counter)

                # writring the extracted images
                cv.imwrite(name, frame)

                counter += 1
            else:
                break

        # showing local of frames
        print("The frames are saved in", self.frames_child_path)

class Frame():
    def converting_to_gray(image_location):
        """
        input: the location of original image
        output: np array of the image in a gray scale
        """

        # open the image
        image = im.open(image_location)

        # converting to a gray scale and to a np array
        vet_img_grayscale = np.array(image.convert('L'))

        return vet_img_grayscale
   
    def getting_intensity_vector(image):
        """
        input: image in a gray scale
        output: vector of intensity of the middle line
        """
        y_axis = []
        x_axis = []

        # filling in the y_axis
        n_lines, n_columns = image.shape
        middle_line = n_lines // 2
        for column in range(n_columns):
            y_axis.append(image[middle_line][column])

        y_axis = np.asarray(y_axis)
        
        # getting the number of pixel of the first column of video matrix
        x_axis = np.asarray([i for i in range(len(image[0]))])

        # softening y_axis
        b, a = sp.signal.butter(1, [.01, 0.1], btype='bandpass')
        smooth_y_axis= sp.signal.filtfilt(b, a, y_axis, padlen=150)

        return x_axis, y_axis, smooth_y_axis
    
    def getting_peaks(vec_x, vec_y):
        """
        input: np vec with the x values and np vec with y values
        output: (x,y) of two peaks
        """

        # finding minimum point
        tuplas_x_y = list(zip(vec_x,vec_y))

        min_y_value = vec_y[0]
        min_point = 0
        for point in tuplas_x_y:
            if point[1] < min_y_value:
                min_y_value = point[1]
                min_point = point[0]

        # taking the first peak
        max_y_value = vec_y[0]
        max_point = 0
        graph_l_to_r = tuplas_x_y[0:min_point]
        for point in graph_l_to_r:
            if point[1] > max_y_value:
                max_y_value = point[1]
                max_point = point[0]

        first_peak = max_point

        # taking the second peak
        max_y_value = min_y_value
        max_point
        graph_inverted = tuplas_x_y[min_point:]
        for point in graph_inverted:
            if point[1] > max_y_value:
                max_y_value = point[1]
                max_point = point[0]


        second_peak = max_point

        return first_peak, second_peak

    def radio_growth_rate(delD_vec, frame_interval, conversion_constant=1):
        speed_rate_vec = []
        for D in delD_vec:
            speed_rate = (D * conversion_constant)/frame_interval
            speed_rate_vec.append(speed_rate)

        return speed_rate_vec

class Data:
    data_path = "/home/caique/unicamp/f359/data_csv/"

    def plot_speedxtime(x_axis, y_axis, legend=''):
        plt.plot(x_axis, y_axis, 'o-', label=legend)
        plt.legend()
        plt.show()

def frame_number(archive_name):
    string = archive_name.replace('frame','')
    string = int(string.split('.')[0])
    frame_index = int(string)
    return frame_index