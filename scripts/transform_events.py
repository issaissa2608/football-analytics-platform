import json
import os

data_path = "C:/Users/pc/OneDrive/Documents/football_analytics/data/raw"


files = os.listdir(data_path)
file_path = os.path.join(data_path, files[0])

with open(file_path, "r", encoding="utf-8") as f:
    events = json.load(f)

filtered_events = []

for event in events:
    event_type = event["type"]["name"]

    if event_type in ["Pass", "Shot", "Carry", "Dribble"]:
        
        record = {
            "event_id": event.get("id"),
            "match_id": os.path.basename(file_path).replace(".json", ""),
            "player_id": event.get("player", {}).get("id"),
            "team_id": event.get("team", {}).get("id"),
            "event_type": event_type,
            "minute": event.get("minute"),
            "second": event.get("second"),
            "x": event.get("location", [None, None])[0],
            "y": event.get("location", [None, None])[1],
            "outcome": None
        }

        # outcome logic
        if event_type == "Pass":
            record["outcome"] = event.get("pass", {}).get("outcome", {}).get("name", "Complete")
        
        elif event_type == "Shot":
            record["outcome"] = event.get("shot", {}).get("outcome", {}).get("name")

        filtered_events.append(record)

print("Total filtered events:", len(filtered_events))

print("\nSample transformed event:\n", filtered_events[0])