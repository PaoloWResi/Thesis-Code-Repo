import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

with open("Jsons/data7.json") as file:
    data = json.load(file)

with open("Jsons/data11.json") as file:
    data2 = json.load(file)


hard_violations = data['soft_violations']
hard_violations2 = data2['soft_violations']

max_len = max(len(hard_violations), len(hard_violations2))
hard_violations = hard_violations + [np.nan] * (max_len - len(hard_violations))
hard_violations2 = hard_violations2 + [np.nan] * (max_len - len(hard_violations2))

x_values = list(range(1, len(hard_violations) + 1))

#plt.figure(figsize=(10, 6))

plt.plot(x_values, hard_violations, label='Soft Constraint Violations for Instance 7', color='red')
plt.plot(x_values, hard_violations2, label='Soft Constraint Violations for Instance 11', color='blue')

#plt.plot(x_values, hard_violations2, label='Soft Violations for dataset 11', color='blue')

plt.title('Soft Constraint Violations over 10000 generations for Instance 7 and Instance 11')
plt.xlabel('Generations')
plt.ylabel('Number of Violations')
plt.legend()

plt.grid(True)
plt.show()
