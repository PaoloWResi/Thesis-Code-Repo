import pandas as pd
import numpy as np
import statistics
import json

runCount = 7


with open(f"Jsons/data{runCount}.json") as json_file:
    data = json.load(json_file)

print("Instance:", + runCount)
total_violations = data["totalViolations"]
total_cost = data["totalCost"]

df = pd.DataFrame({'TotalViolations': total_violations, 'TotalCost': total_cost})

x = df["TotalViolations"]
y = df["TotalCost"]

vioMean = statistics.stdev(x)

print("Hard Violations:", + round(vioMean,2))


"""while runCount <= 21:

    with open(f"Jsons/Testdata{runCount}.json") as json_file:
        data = json.load(json_file)

    print("Instance:", + runCount)
    total_violations = data["totalViolations"]
    total_cost = data["totalCost"]

    df = pd.DataFrame({'TotalViolations': total_violations, 'TotalCost': total_cost})

    x = df["TotalViolations"]
    y = df["TotalCost"]

    vioMean = np.mean(x)
    costMean = np.mean(y)

    print("Hard Violations:", + round(vioMean,2))
    print("Soft Violations:", + round(costMean,2))
    runCount += 1"""
