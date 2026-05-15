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
"""

# LOAD DATA

df = pd.read_sql(query, conn)

conn.close()

# PROGRESSIVE PASS LOGIC

df["progressive"] = (
    (df["end_x"] - df["x"]) >= 10
)

# SPLIT DATA

completed_passes = df[df["outcome"] == "Complete"]

incomplete_passes = df[df["outcome"] != "Complete"]

progressive_passes = completed_passes[
    completed_passes["progressive"] == True
]

# CREATE PITCH

pitch = Pitch(
    pitch_type='statsbomb',
    pitch_color='#1E1E1E',
    line_color='white'
)

fig, ax = pitch.draw(figsize=(14, 10))

fig.set_facecolor('#1E1E1E')

# COMPLETED PASSES

pitch.arrows(
    completed_passes["x"],
    completed_passes["y"],
    completed_passes["end_x"],
    completed_passes["end_y"],
    color="#4DA6FF",
    ax=ax,
    width=2,
    headwidth=4,
    headlength=4,
    alpha=0.5
)

# INCOMPLETE PASSES

pitch.arrows(
    incomplete_passes["x"],
    incomplete_passes["y"],
    incomplete_passes["end_x"],
    incomplete_passes["end_y"],
    color="#FF6B6B",
    ax=ax,
    width=2,
    headwidth=4,
    headlength=4,
    alpha=0.6
)

# PROGRESSIVE PASSES

pitch.arrows(
    progressive_passes["x"],
    progressive_passes["y"],
    progressive_passes["end_x"],
    progressive_passes["end_y"],
    color="#FFD700",
    ax=ax,
    width=3,
    headwidth=5,
    headlength=5,
    alpha=1
)

# PASS START LOCATIONS

pitch.scatter(
    completed_passes["x"],
    completed_passes["y"],
    s=40,
    color="white",
    edgecolors="black",
    ax=ax,
    zorder=3
)

# TITLES

fig.suptitle(
    "Francesca Kirby Advanced Pass Map",
    color="white",
    fontsize=24
)

fig.text(
    0.5,
    0.92,
    (
        f"Completed: {len(completed_passes)} | "
        f"Incomplete: {len(incomplete_passes)} | "
        f"Progressive: {len(progressive_passes)}"
    ),
    ha="center",
    color="white",
    fontsize=14
)

# SAVE VISUAL

plt.savefig(
    "visuals/francesca_kirby_advanced_pass_map.png",
    dpi=300,
    bbox_inches='tight',
    facecolor=fig.get_facecolor()
)

# SHOW PLOT
plt.show()