import os

def create_folder(folder_path):
    # creating a storege path
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    return folder_path

def getting_archive_name(archive_path):
    return archive_path.split('/')[-1]

def frame_number(archive_name):
    string = archive_name.replace('frame','')
    string = string.split('.')[0]
    if ('_' in string):
        string = string.split('_')[1]
    frame_index = int(string)
    return frame_index

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