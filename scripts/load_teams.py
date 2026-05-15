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

teams_seen = set()

for file_name in files:

    file_path = os.path.join(data_path, file_name)

    with open(file_path, "r", encoding="utf-8") as f:
        events = json.load(f)

    for event in events:

        team = event.get("team")

        if team:

            team_id = team.get("id")
            team_name = team.get("name")

            if team_id not in teams_seen:

                cur.execute("""
                    INSERT INTO teams (
                        team_id,
                        team_name
                    )
                    VALUES (%s, %s)
                    ON CONFLICT (team_id)
                    DO NOTHING;
                """, (
                    team_id,
                    team_name
                ))

                teams_seen.add(team_id)

conn.commit()

cur.close()
conn.close()

print(f"✅ Loaded {len(teams_seen)} teams")