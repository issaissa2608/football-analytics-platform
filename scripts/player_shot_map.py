import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# PLAYER TO ANALYSE

player_name = "Francesca Kirby"

# DATABASE CONNECTION

# database connection
conn = psycopg2.connect(
    dbname="football_analytics",
    user="postgres",
    password="Postgres",
    host="localhost",
    port="5433"
)

# QUERY

query = f"""
SELECT
    p.player_name,
    t.team_name,
    e.x,
    e.y,
    e.outcome

FROM events e

JOIN players p
    ON e.player_id = p.player_id

JOIN teams t
    ON e.team_id = t.team_id

WHERE e.event_type = 'Shot'
AND p.player_name = '{player_name}'
"""

df = pd.read_sql(query, conn)

conn.close()

# CALCULATE DISTANCE TO GOAL

goal_x = 120
goal_y = 40

def calculate_distance(x, y):
    return ((goal_x - x)**2 + (goal_y - y)**2) ** 0.5

df["distance_to_goal"] = df.apply(
    lambda row: calculate_distance(row["x"], row["y"]),
    axis=1
)

# CREATE SHOT SIZE
# Closer shots = bigger circles

df["shot_size"] = 400 - (df["distance_to_goal"] * 15)

df["shot_size"] = df["shot_size"].clip(lower=80)

#function for shot classification
def classify_shot(distance):
    if distance < 10:
        return "High Danger"
    elif distance < 18:
        return "Medium Danger"
    else:
        return "Low Danger"

df["shot_danger"] = df["distance_to_goal"].apply(classify_shot)

# SPLIT GOALS VS NON-GOALS

goals = df[df["outcome"] == "Goal"]
non_goals = df[df["outcome"] != "Goal"]

# CREATE PITCH

pitch = Pitch(
    pitch_type="statsbomb",
    pitch_color="#0B0D0F",
    line_color="white"
)

fig, ax = pitch.draw(figsize=(12, 8))

fig.set_facecolor("#0B0D0F")

# NON-GOAL SHOTS

danger_colors = {
    "High Danger": "#FF4C4C",
    "Medium Danger": "#FFB000",
    "Low Danger": "#4FA3FF"
}

for danger, color in danger_colors.items():
    danger_df = df[(df["shot_danger"] == danger) & (df["outcome"] != "Goal")]

    pitch.scatter(
        danger_df["x"],
        danger_df["y"],
        ax=ax,
        s=danger_df["shot_size"],
        color=color,
        edgecolors="black",
        alpha=0.8,
        label=danger
    )

# GOALS

pitch.scatter(
    goals["x"],
    goals["y"],
    ax=ax,
    s=goals["shot_size"] + 150,
    marker="*",
    color="#FFCC00",
    edgecolors="black",
    label="Goals"
)

# TITLES

ax.set_title(
    f"{player_name}\nShot Map",
    color="white",
    fontsize=24,
    pad=20
)

# METRICS

fig.text(
    0.5,
    0.88,
    f"Shots: {len(df)} | Goals: {len(goals)} | Avg Distance: {round(df['distance_to_goal'].mean(), 2)}",
    ha="center",
    color="white",
    fontsize=14
)

# LEGEND

legend = ax.legend(
    facecolor="#0B0D0F",
    edgecolor="white",
    fontsize=12,
    loc="upper left"
)

for text in legend.get_texts():
    text.set_color("white")

plt.tight_layout()

# SAVE IMAGE


file_name = player_name.replace(" ", "_").lower()

plt.savefig(
    f"data/{file_name}_shot_map.png",
    dpi=300,
    bbox_inches="tight",
    facecolor=fig.get_facecolor()
)

plt.show()

print(f"Shot map created for {player_name}")
print(f"Total shots: {len(df)}")
print(f"Goals: {len(goals)}")