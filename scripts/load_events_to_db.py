import json
import os
import psycopg2

conn = psycopg2.connect(
    dbname="football_analytics",
    user="postgres",
    password="Postgres",
    host="localhost",
    port="5433"
)

cur = conn.cursor()

data_path = "C:/Users/pc/OneDrive/Documents/football_analytics/data/raw"
files = os.listdir(data_path)

file_path = os.path.join(data_path, files[0])

with open(file_path, "r", encoding="utf-8") as f:
    events = json.load(f)

match_id = os.path.basename(file_path).replace(".json", "")

inserted_count = 0

for event in events:
    event_type = event["type"]["name"]

    if event_type in ["Pass", "Shot", "Carry", "Dribble"]:

        player_id = event.get("player", {}).get("id")
        team_id = event.get("team", {}).get("id")

        x, y = None, None
        if "location" in event:
            x, y = event["location"]

        outcome = None

        if event_type == "Pass":
            outcome = event.get("pass", {}).get("outcome", {}).get("name", "Complete")
        
        elif event_type == "Shot":
            outcome = event.get("shot", {}).get("outcome", {}).get("name")

        cur.execute("""
            INSERT INTO events (
                match_id, player_id, team_id, event_type,
                minute, second, x, y, outcome
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            match_id,
            player_id,
            team_id,
            event_type,
            event.get("minute"),
            event.get("second"),
            x,
            y,
            outcome
        ))

        inserted_count += 1

conn.commit()

cur.close()
conn.close()

print(f"✅ Inserted {inserted_count} events into database")