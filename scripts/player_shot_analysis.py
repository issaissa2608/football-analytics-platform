import psycopg2
import pandas as pd
import math

# -----------------------------------
# PLAYER
# -----------------------------------

player_name = "Francesca Kirby"

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------

# database connection
conn = psycopg2.connect(
    dbname="football_analytics",
    user="postgres",
    password="Postgres",
    host="localhost",
    port="5433"
)

# -----------------------------------
# QUERY
# -----------------------------------

query = f"""
SELECT
    p.player_name,
    e.x,
    e.y,
    e.outcome

FROM events e

JOIN players p
    ON e.player_id = p.player_id

WHERE e.event_type = 'Shot'
AND p.player_name = '{player_name}'
"""

df = pd.read_sql(query, conn)

conn.close()

# -----------------------------------
# CALCULATE DISTANCE TO GOAL
# -----------------------------------

goal_x = 120
goal_y = 40

def calculate_distance(x, y):
    return round(
        math.sqrt((goal_x - x)**2 + (goal_y - y)**2),
        2
    )

df["distance_to_goal"] = df.apply(
    lambda row: calculate_distance(row["x"], row["y"]),
    axis=1
)

# -----------------------------------
# SHOT DANGER CLASSIFICATION
# -----------------------------------

def classify_shot(distance):

    if distance < 10:
        return "High Danger"

    elif distance < 18:
        return "Medium Danger"

    else:
        return "Low Danger"

df["shot_danger"] = df["distance_to_goal"].apply(classify_shot)

# -----------------------------------
# OUTPUT
# -----------------------------------

print(df)

print("\nShot danger breakdown:")

print(df["shot_danger"].value_counts())

print("\nAverage shot distance:")
print(round(df["distance_to_goal"].mean(), 2))