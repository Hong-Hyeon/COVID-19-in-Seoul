import matplotlib.pyplot as plt
import math
import seaborn as sns

from termcolor import colored

class plot_():
    def __init__(self, x_data = False, y_data = False):
        self.x_data = x_data
        self.y_data = y_data

    def subplot_(self, make_plot):
        if make_plot == 1:
            plt.plot(self.x_data, self.y_data, '.')
            plt.show(block = True)
        elif make_plot <= 0:
            print(colored('VALUE ERROR : This is an incorrect entry.', 'red'))
            return False
        else:
            print(colored('VALUE ERROR : It is not possible to create multiple in the current version.', 'red'))
            return False

    def histogram_(self, title, x_label, y_label, bins):
        fig = plt.figure()
        ax1 = fig.add_subplot()
        ax1.hist(self.x_data, bins)
        ax1.set_title(title)
        ax1.set_xlabel(x_label)
        ax1.set_ylabel(y_label)
        plt.show(block=True)

    def scatter_(self):
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.scatter(self.x_data, self.y_data)
        plt.show(block=True)

    def boxplot_(self, x_label, y_label):
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.boxplot([self.x_data, self.y_data], labels = [x_label, y_label])
        plt.show(block = True)

    def distplot_(self):
        plt.subplots()
        sns.distplot(self.x_data, rug=True)
        plt.show(block=True)
