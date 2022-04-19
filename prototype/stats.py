import pandas as pd
import seaborn as sns
from IPython.display import display, HTML
from scipy import stats
from matplotlib import pyplot as plt
import statsmodels.api as sm
import pylab
import math
import numpy as np

mice = pd.read_csv("flat.csv", header=0)
print(mice.head)

from matplotlib.pyplot import figure
import numpy as np

figure(figsize=(8, 7), dpi=160)

tx = [i for i in range(14, 23, 1)]

sd_scale = 2.3

cd40 = mice.loc[mice["Group"]=='CD40']
cd40_mean = cd40.groupby(["Day", "Group"])['volume'].mean().values
cd40_std = cd40.groupby(["Day", "Group"])['volume'].std().values
cd40_up = cd40_mean + cd40_std / sd_scale
cd40_down = cd40_mean - cd40_std / sd_scale

igg = mice.loc[mice["Group"]=='IgG']
igg_mean = igg.groupby(["Day", "Group"])['volume'].mean().values
igg_std = igg.groupby(["Day", "Group"])['volume'].std().values
igg_up = igg_mean + igg_std / sd_scale
igg_down = igg_mean - igg_std / sd_scale

plt.scatter(x=tx, y=cd40_mean, marker="o", label='antiCD40', color="red")
plt.scatter(x=tx, y=cd40_up, marker="_", color="red")
plt.scatter(x=tx, y=cd40_down, marker="_", color="red")
plt.plot(tx, cd40_mean, color="red")
[plt.plot([tx[i], tx[i]],[cd40_up[i], cd40_down[i]],color="red") for i in range(0,len(tx))]

plt.scatter(x=tx, y=igg_mean, marker='o', label='igG', color="blue")
plt.scatter(x=tx, y=igg_up, marker='_', color="blue")
plt.scatter(x=tx, y=igg_down, marker='_', color="blue")
plt.plot(tx, igg_mean, color="blue")
[plt.plot([tx[i], tx[i]],[igg_up[i], igg_down[i]],color="blue") for i in range(0,len(tx))]


plt.title("Tumor Volume Over Time")
plt.xlabel("Day")
plt.ylabel("Tumor Volume mm^3")
plt.legend()
plt.savefig("figure.png")