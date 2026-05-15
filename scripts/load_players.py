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

data_path =  "C:/Users/pc/OneDrive/Documents/football_analytics/data/raw"

files = os.listdir(data_path)

players_seen = set()

for file_name in files:

    file_path = os.path.join(data_path, file_name)

    with open(file_path, "r", encoding="utf-8") as f:
        events = json.load(f)

    for event in events:

        player = event.get("player")

        if player:

            player_id = player.get("id")
            player_name = player.get("name")

            if player_id not in players_seen:

                cur.execute("""
                    INSERT INTO players (
                        player_id,
                        player_name
                    )
                    VALUES (%s, %s)
                    ON CONFLICT (player_id)
                    DO NOTHING;
                """, (
                    player_id,
                    player_name
                ))

                players_seen.add(player_id)

conn.commit()

cur.close()
conn.close()

print(f"Loaded {len(players_seen)} players")