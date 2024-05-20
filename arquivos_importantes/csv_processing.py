from video_processing_functions import *
import pandas as pd
import matplotlib.pyplot as plt

# columns = ["radio_growth_rate", 't']
columns = ['t', ]
for csv_file in os.listdir(Data.data_path):
    data = pd.read_csv(Data.data_path+csv_file)
    # print(data.columns)
    # print(data.keys)
    plt.plot(data['t'], data['x1'], label='first peak')
    plt.plot(data["t"], data['x2'], label='second peak')
    plt.legend()
    plt.show()
    
