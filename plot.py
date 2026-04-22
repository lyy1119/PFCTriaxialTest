from lycarusLab.plot import plot_style
from collections.abc import Iterable
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress

NumericData = int | float | Iterable[int | float]

def plot(f, xMin, xMax, number):
    xList = np.linspace(xMin, xMax, number)
    print(xList)
    yList = f(xList)
    print(yList)
    plt.plot(xList, yList, '-', color='black', label='z stress')

if __name__ == "__main__":
    # confinePressure = 800000.0
    confinePressure = float(input('input confining pressue (Pa):'))
    csvfile = input('input csv file:').strip()
    csvfile = csvfile if csvfile.endswith('.csv') else csvfile+'.csv'
    data = pd.read_csv('800000.0.csv')
    deltaStress = [float(i)-confinePressure for i in data['stress'].values]
    strain = [float(i) for i in data['strain'].values]
    y = []
    for i, j in zip(deltaStress, strain):
        y.append(j/i)
    x = strain
    slope, intercept, r_value, p_value, std_err = linregress(x, y)

    with plot_style('my plot', r'$\epsilon$', r'$\frac{\epsilon}{\Delta \sigma}$'):
        plt.scatter(x, y, color='black', label='origin', s=3)
        yLinear = [slope*i + intercept for i in x] # type: ignore
        plt.plot(x, yLinear, '-', color='red')
    print(f'sigma_1 - sigma_3 = {1e100/(intercept+slope*1e100)}') # type: ignore
    with plot_style('origin', r'$\epsilon$', r'$\Delta \sigma$'):
        plt.scatter(strain, deltaStress, color='black', label='origin', s=3)
        deltaStressFit = [i/(intercept + slope*i) for i in strain] # type: ignore
        plt.plot(strain, deltaStressFit, '-', color='red')
