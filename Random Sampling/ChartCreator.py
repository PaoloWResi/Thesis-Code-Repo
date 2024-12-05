import json
import numpy as np
import pandas as pd
import statistics
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from scipy.ndimage import gaussian_filter


runCount = 7

with open(f"Jsons/data{runCount}.json") as json_file:
    data = json.load(json_file)

print(runCount)
total_violations = data["totalViolations"]
total_cost = data["totalCost"]

df = pd.DataFrame({'TotalViolations': total_violations, 'TotalCost': total_cost})

x = df["TotalViolations"]
y = df["TotalCost"]

"""vioMean = np.mean(x)
costMean = np.mean(y)

vioMode = statistics.mode(x)

vioMedian = statistics.median(x)

vioSt = statistics.stdev(x)

print(round(vioMode,2))
print(round(vioMedian,2))
print(round(vioSt,2))"""




hist, xedges, yedges = np.histogram2d(x, y, bins=50)

smoothed_hist = gaussian_filter(hist, sigma=2)

plt.imshow(smoothed_hist.T, origin='lower', cmap='Reds', interpolation='bilinear',
           extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], aspect='auto')

plt.colorbar(label="Density")
plt.xlabel("Hard Constraint Violations")
plt.ylabel("Soft Constraint")
plt.title("Heat Map of Hard against Soft Constraint Violations for Instance 7")

plt.show()

"""hist, xedges, yedges = np.histogram2d(x, y)

xpos, ypos = np.meshgrid(xedges[:-1] + 0.5, yedges[:-1] + 0.5, indexing="ij")
xpos = xpos.ravel()
ypos = ypos.ravel()
zpos = 0

dz = hist.ravel()

norm = plt.Normalize(dz.min(), dz.max())
colors = cm.viridis(norm(dz))

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(projection="3d")

dx = np.diff(xedges)[0] * np.ones_like(zpos)  
dy = np.diff(yedges)[0] * np.ones_like(zpos) 
ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colors, alpha=0.7, shade=True, zsort = 'average')

mappable = cm.ScalarMappable(cmap="viridis", norm=norm)
mappable.set_array(dz)
fig.colorbar(mappable, ax=ax, shrink=0.5, aspect=10, label="Frequency")

ax.set_xlabel("Hard Violations")
ax.set_ylabel("Soft Violations")
ax.set_zlabel("Frequency")
ax.set_title("Histogram of Total Violations vs. Total Cost for dataset 11")

plt.show() """
