from video_processing_functions import * 
from PIL import ImageDraw
import pandas as pd
import numpy as np
import os

def frame_number(archive_name):
    string = archive_name.replace('frame','')
    string = int(string.split('.')[0])
    frame_index = int(string)
    return frame_index

# seting the vectors that will be converted to csv
frame_index_vec = []
time_vec = []
first_peak_vec = []
second_peak_vec = []
peak_distance_vec = []
del_peak_dist_vec = []

testing_mode = int(input('testing mode? '))

# for diffusion_video in os.listdir(Video.videos_path):

# picking the video
diffusion_video = 'nosso_video.mp4'
# Video.separating_frames(diffusion_video)

# taking video infos
target_video = cv.VideoCapture(Video.videos_path + diffusion_video)
fps = target_video.get(cv.CAP_PROP_FPS)
frame_numbers = int(target_video.get(cv.CAP_PROP_FRAME_COUNT))
duration = frame_numbers/fps
frame_delt = duration/frame_numbers

target_video.release()

# open the especific path with the frames
ordered_frames = sorted(os.listdir(Video.frames_mother_path + diffusion_video), key=frame_number)
frame_index = 0
for diffusion_frame in ordered_frames:
    specific_path = Video.frames_mother_path + diffusion_video + "/"

    fn = frame_number(diffusion_frame)

    if (fn < 20):
        continue

    # processing the frame
    gray_frame = Frame.converting_to_gray(specific_path + diffusion_frame)
    im.fromarray(gray_frame).show()
    cropped_gray_frame = gray_frame[:,650:1550]
    original_y_axis = []
    smooth_y_axis = []
    x_axis = []

    # analyzing line
    x_axis, original_y_axis, smooth_y_axis = Frame.getting_intensity_vector(cropped_gray_frame)

    # analising the peaks of graph
    first_peak, second_peak = Frame.getting_peaks(x_axis, smooth_y_axis)
    peak_distance = abs(first_peak - second_peak)

    # append the frame results
    frame_index_vec.append(frame_index)
    time_vec.append(frame_index * frame_delt)
    first_peak_vec.append(first_peak)
    second_peak_vec.append(second_peak)
    peak_distance_vec.append(peak_distance)

    if (frame_index):
        del_peak_dist_vec.append(abs(
            peak_distance_vec[frame_index] - peak_distance_vec[frame_index-1]
        ))

    frame_index += 1
    print(f'the peaks of {diffusion_frame} are in {first_peak} and {second_peak}')
    if (testing_mode):
        # line analyzed
        (n_lines, n_columns) = cropped_gray_frame.shape
        middle_line = n_lines // 2
        line = [(0, middle_line), (n_columns-1, middle_line)]
        img = im.fromarray(cropped_gray_frame)
        img1 = ImageDraw.Draw(img)
        img1.line(line, fill='white', width=3)
        img.show()

        # graphing the data
        plt.plot(original_y_axis)
        plt.plot(smooth_y_axis)
        plt.axvline(first_peak)
        plt.axvline(second_peak)
        plt.show()

# correting the lenth of vector
del_peak_dist_vec.insert(0,0)

print(
    'frame_index_vec len: ', len(frame_index_vec) ,  '\n',
    'time_vec len: ', len(time_vec) , '\n',
    'first_peak_vec len: ', len(first_peak_vec) , '\n',
    'second_peak_vec len: ', len(second_peak_vec) , '\n',
    'peak_distance_vec len: ', len(peak_distance_vec) 
)

# calculating the growth rate of radio
# speed_rate_vec = Frame.radio_growth_rate(del_peak_dist_vec, frame_delt)

if (not testing_mode):
    d = {
        'frame_index': frame_index_vec,
        't': time_vec,
        'x1': first_peak_vec,
        'x2': second_peak_vec,
        'delX_in_frame': peak_distance_vec, 
        # 'delx_between_frames': del_peak_dist_vec,
        # 'radio_growth_rate': speed_rate_vec
    }

    df = pd.DataFrame(data=d)

    # saving the csv
    diffusion_csv = diffusion_video.split(".")[0] +".csv"
    df.to_csv(Data.data_path + "/"+ diffusion_csv, index=0)

    # success message
    print("..........................")
    print("the archive", Data.data_path + "/"+ diffusion_csv, "has been saved with succes")





