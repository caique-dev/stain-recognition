from arquivos_importantes.general_functions import *
import cv2 as cv
import os

class Video():
    videos_path = "/home/caique/unicamp/f359/diffusion_videos/";
    frames_mother_path = "/home/caique/unicamp/f359/videos_frames/";

    def __init__(self, video_name):
        self.name = video_name

        self.frames_child_path = Video.frames_mother_path + video_name
        self.video_target = cv.VideoCapture(Video.videos_path + video_name)

        # taking video infos
        self.fps = self.video_target.get(cv.CAP_PROP_FPS)
        self.frame_numbers = int(self.video_target.get(cv.CAP_PROP_FRAME_COUNT))
        self.duration = self.frame_numbers/self.fps
        self.frame_delt = self.duration/self.frame_numbers

        # about frames
        self.start_frame = 0
        self.end_frame = self.frame_numbers

    def separating_frames(self):
        """
            separating the video in frames and storage it
        """
        
        # creating the storage folder
        create_folder(Video.frames_mother_path + self.name)

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

    def set_endframe(self, end):
        self.end_frame = end

    def set_startframe(self, start):
        self.start_frame = start