# LIBRARIES
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch


# DATABASE CONNECTION

conn = psycopg2.connect(
    host="localhost",
    database="football_analytics",
    user="postgres",
    password="Postgres",
    port="5433"
)

# SQL QUERY

query = """
SELECT
    p.player_name,
    e.x,
    e.y,
    e.end_x,
    e.end_y,
    e.outcome
FROM events e
JOIN players p
    ON e.player_id = p.player_id
WHERE
    e.event_type = 'Pass'
    AND p.player_name = 'Francesca Kirby'
    AND e.outcome = 'Complete'
"""

# LOAD DATA

df = pd.read_sql(query, conn)

conn.close()

print(df.head())

print(f"\nTotal completed passes: {len(df)}")


# CREATE PITCH

pitch = Pitch(
    pitch_type='statsbomb',
    pitch_color='#1E1E1E',
    line_color='white'
)

fig, ax = pitch.draw(figsize=(12, 8))

fig.set_facecolor('#1E1E1E')

# DRAW PASSES

pitch.arrows(
    df["x"],
    df["y"],
    df["end_x"],
    df["end_y"],
    color="#00BFFF",
    ax=ax,
    width=2,
    headwidth=4,
    headlength=4,
    alpha=0.7
)

# TITLES

fig.suptitle(
    "Francesca Kirby Pass Map",
    color="white",
    fontsize=20
)

fig.text(
    0.5,
    0.90,
    f"Completed Passes: {len(df)}",
    ha="center",
    color="white",
    fontsize=14
)

# SAVE VISUAL

plt.savefig(
    "visuals/francesca_kirby_pass_map.png",
    dpi=300,
    bbox_inches='tight',
    facecolor=fig.get_facecolor()
)

plt.show()