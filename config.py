import json

with open("config.json", "r") as f:
    constants = json.load(f)

for key, value in constants.items():
    globals()[key] = value
