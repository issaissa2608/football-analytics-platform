import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# database connection
conn = psycopg2.connect(
    dbname="football_analytics",
    user="postgres",
    password="Postgres",
    host="localhost",
    port="5433"
)

query = """
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
"""

df = pd.read_sql(query, conn)
conn.close()

# split goals vs non-goals
goals = df[df["outcome"] == "Goal"]
non_goals = df[df["outcome"] != "Goal"]

# create pitch
pitch = Pitch(
    pitch_type="statsbomb",
    pitch_color="#0B0D0F",
    line_color="white"
)

fig, ax = pitch.draw(figsize=(12, 8))

fig.set_facecolor("#0B0D0F")

# non-goal shots
pitch.scatter(
    non_goals["x"],
    non_goals["y"],
    ax=ax,
    s=140,
    color="#4FA3FF",
    edgecolors="black",
    alpha=0.75,
    label="Shots"
)

# goals
pitch.scatter(
    goals["x"],
    goals["y"],
    ax=ax,
    s=350,
    marker="*",
    color="#FFCC00",
    edgecolors="black",
    label="Goals"
)

# titles
ax.set_title(
    "Chelsea FCW vs Manchester City WFC\nShot Map",
    color="white",
    fontsize=22,
    pad=20
)

# subtitle
fig.text(
    0.5,
    0.88,
    f"Total Shots: {len(df)} | Goals: {len(goals)}",
    ha="center",
    color="white",
    fontsize=13
)

# legend
legend = ax.legend(
    facecolor="#0B0D0F",
    edgecolor="white",
    fontsize=12,
    loc="upper left"
)

for text in legend.get_texts():
    text.set_color("white")

plt.tight_layout()

# save image
plt.savefig(
    "data/professional_shot_map.png",
    dpi=300,
    bbox_inches="tight",
    facecolor=fig.get_facecolor()
)

plt.show()

print("✅ Professional shot map created")