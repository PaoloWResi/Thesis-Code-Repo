import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

with open("Jsons/data11.json") as file:
    data = json.load(file)

with open("Jsons/data7.json") as file:
    data2 = json.load(file)

hard_violations = data['hard_violations']
soft_violations = data2['hard_violations']

x_values = list(range(1, len(hard_violations) + 1))


plt.plot(x_values, hard_violations, label='Hard Constraint Violations for Instance 11', color='blue')
plt.plot(x_values, soft_violations, label='Hard Constraint Violations for Instance 7', color='red')


plt.title('Hard Constraint Violations over 10000 Generations for Instance 7 and Instance 11')
plt.xlabel('Generation')
plt.ylabel('Number of Violations')
plt.legend()

plt.grid(True)
plt.show()
