import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

team_name = "Chelsea FCW"

conn = psycopg2.connect(
    dbname="football_analytics",
    user="postgres",
    password="Postgres",
    host="localhost",
    port="5433"
)

query = f"""
SELECT
    p.player_id AS passer_id,
    p.player_name AS passer,
    r.player_id AS recipient_id,
    r.player_name AS recipient,
    e.x,
    e.y,
    e.end_x,
    e.end_y
FROM events e
JOIN players p
    ON e.player_id = p.player_id
JOIN players r
    ON e.recipient_id = r.player_id
JOIN teams t
    ON e.team_id = t.team_id
WHERE e.event_type = 'Pass'
AND e.outcome = 'Complete'
AND e.recipient_id IS NOT NULL
AND t.team_name = '{team_name}'
"""

df = pd.read_sql(query, conn)
conn.close()

print(df.head())
print("Total completed passes:", len(df))

# Average player position based on pass start locations
player_positions = (
    df.groupby(["passer_id", "passer"])
    .agg(avg_x=("x", "mean"), avg_y=("y", "mean"), pass_count=("passer", "count"))
    .reset_index()
)

# Pass combinations between players
pass_pairs = (
    df.groupby(["passer", "recipient"])
    .size()
    .reset_index(name="pass_count")
)

# Only show stronger connections
pass_pairs = pass_pairs[pass_pairs["pass_count"] >= 3]

# Create lookup for positions
position_lookup = player_positions.set_index("passer")[["avg_x", "avg_y"]].to_dict("index")

pitch = Pitch(
    pitch_type="statsbomb",
    pitch_color="#0B0D0F",
    line_color="white"
)

fig, ax = pitch.draw(figsize=(14, 10))
fig.set_facecolor("#0B0D0F")

# Draw pass connections
for _, row in pass_pairs.iterrows():
    passer = row["passer"]
    recipient = row["recipient"]

    if passer in position_lookup and recipient in position_lookup:
        x_start = position_lookup[passer]["avg_x"]
        y_start = position_lookup[passer]["avg_y"]
        x_end = position_lookup[recipient]["avg_x"]
        y_end = position_lookup[recipient]["avg_y"]

        pitch.lines(
            x_start,
            y_start,
            x_end,
            y_end,
            lw=row["pass_count"] * 0.4,
            color="#4FA3FF",
            alpha=0.55,
            ax=ax
        )

# Draw player nodes
pitch.scatter(
    player_positions["avg_x"],
    player_positions["avg_y"],
    s=player_positions["pass_count"] * 20,
    color="#FFD700",
    edgecolors="black",
    linewidth=1.5,
    ax=ax,
    zorder=3
)

# Add player labels
for _, row in player_positions.iterrows():
    ax.text(
        row["avg_x"],
        row["avg_y"] + 2,
        row["passer"].split()[-1],
        color="white",
        fontsize=9,
        ha="center",
        va="center"
    )

fig.suptitle(
    f"{team_name} Pass Network",
    color="white",
    fontsize=24
)

fig.text(
    0.5,
    0.92,
    f"Completed passes: {len(df)} | Connections shown: {len(pass_pairs)}",
    ha="center",
    color="white",
    fontsize=14
)

plt.savefig(
    "visuals/chelsea_fcw_pass_network.png",
    dpi=300,
    bbox_inches="tight",
    facecolor=fig.get_facecolor()
)

# Show plot
plt.show()