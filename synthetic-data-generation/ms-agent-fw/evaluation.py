
from pathlib import Path
import json

with open(Path("scenarios.json"), "r") as f:
    dataset = json.load(f)

# print(dataset[0])
generation = {"GenZ": 0, "Millennial": 0, "GenX": 0, "Boomer": 0}
for scenario in dataset:
    if scenario["user"]["age"] < 29:
        generation["GenZ"] += 1
    elif scenario["user"]["age"] < 45:
        generation["Millennial"] += 1
    elif scenario["user"]["age"] < 61:
        generation["GenX"] += 1
    else:
        generation["Boomer"] += 1
print(generation)

"""
result: {'GenZ': 29, 'Millennial': 53, 'GenX': 34, 'Boomer': 31}
"""
