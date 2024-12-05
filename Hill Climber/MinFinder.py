import pandas as pd
import numpy as np
import json

runCount = 1

while runCount <= 21:

    with open(f"Jsons/data{runCount}.json") as json_file:
        data = json.load(json_file)

    print("Instance:", + runCount)
    total_violations = data["hard_violations"]
    total_cost = data["soft_violations"]

    df = pd.DataFrame({'TotalViolations': total_violations, 'TotalCost': total_cost})

    x = df["TotalViolations"]
    y = df["TotalCost"]

    vioMean = min(x)
    costMean = min(y)

    print("Hard Violations:", + round(vioMean,2))
    print("Soft Violations:", + round(costMean,2))
    runCount += 1