import json
import os

# path to raw data folder
data_path = "C:/Users/pc/OneDrive/Documents/football_analytics/data/raw"

files = os.listdir(data_path)

print("Files found:", files)

# open first file
file_path = os.path.join(data_path, files[0])

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Total events in file:", len(data))

# print first event
print("\nSample event:\n", data[0])