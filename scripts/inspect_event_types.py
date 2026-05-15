import json
import os
from collections import Counter

data_path = "C:/Users/pc/OneDrive/Documents/football_analytics/data/raw"

files = os.listdir(data_path)
file_path = os.path.join(data_path, files[0])

with open(file_path, "r", encoding="utf-8") as f:
    events = json.load(f)

event_types = [event["type"]["name"] for event in events]

counts = Counter(event_types)

print("Event types found:\n")

for event_type, count in counts.most_common():
    print(f"{event_type}: {count}")