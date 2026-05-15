import psycopg2

conn = psycopg2.connect(
    dbname="football_analytics",
    user="postgres",
    password="Postgres",
    host="localhost",
    port="5433"
)

cur = conn.cursor()

# Insert league
cur.execute("""
    INSERT INTO leagues (league_name, country)
    VALUES (%s, %s)
    RETURNING league_id;
""", ("Premier League", "England"))

league_id = cur.fetchone()[0]

# Insert teams
cur.execute("""
    INSERT INTO teams (team_name, league_id)
    VALUES (%s, %s)
    RETURNING team_id;
""", ("Arsenal", league_id))

arsenal_id = cur.fetchone()[0]

cur.execute("""
    INSERT INTO teams (team_name, league_id)
    VALUES (%s, %s)
    RETURNING team_id;
""", ("Manchester City", league_id))

man_city_id = cur.fetchone()[0]

# Insert player
cur.execute("""
    INSERT INTO players (player_name, position, nationality)
    VALUES (%s, %s, %s)
    RETURNING player_id;
""", ("Bukayo Saka", "Forward", "England"))

player_id = cur.fetchone()[0]

# Insert match
cur.execute("""
    INSERT INTO matches (match_date, home_team_id, away_team_id, league_id, season)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING match_id;
""", ("2025-05-01", arsenal_id, man_city_id, league_id, "2024/2025"))

match_id = cur.fetchone()[0]

# Insert event
cur.execute("""
    INSERT INTO events (match_id, player_id, team_id, event_type, minute, second, x, y, outcome)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
""", (match_id, player_id, arsenal_id, "Shot", 23, 15, 88.5, 42.1, "On Target"))

conn.commit()

cur.close()
conn.close()

print("Test football data inserted successfully")