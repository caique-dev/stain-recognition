from matplotlib import pyplot as plt

class Data:
    data_path = "/home/caique/unicamp/f359/data_csv/"

    def plot_speedxtime(x_axis, y_axis, legend=''):
        plt.plot(x_axis, y_axis, 'o-', label=legend)
        plt.legend()
        plt.show()