from lycarusLab.plot import plot_style
from collections.abc import Iterable
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

NumericData = int | float | Iterable[int | float]

def plot(f, xMin, xMax, number):
    xList = np.linspace(xMin, xMax, number)
    print(xList)
    yList = f(xList)
    print(yList)
    plt.plot(xList, yList, '-', color='black', label='z stress')

if __name__ == "__main__":
    data = pd.read_csv('s.csv')
    x = [float(i) for i in data['Step'].values]
    y = [float(i) for i in data['zStress'].values]
    with plot_style('my plot', 'step', 'stress'):
        plt.scatter(x, y, color='black', label='origin')

    # def f(x: NumericData):
    #     y = lambda x: x / (-4498.78659 + 0.06865 * x)

    #     return y(x)

    # with plot_style('my plot', 'step', 'stress'):
    #     print(1)
    #     plot(f, 65540, 865540, 800)