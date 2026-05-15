CREATE TABLE leagues (
    league_id SERIAL PRIMARY KEY,
    league_name TEXT,
    country TEXT
);

CREATE TABLE teams (
    team_id INT PRIMARY KEY,
    team_name TEXT,
    league_id INT
);

CREATE TABLE players (
    player_id INT PRIMARY KEY,
    player_name TEXT,
    position TEXT,
    nationality TEXT
);

CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    match_date DATE,
    home_team_id INT,
    away_team_id INT,
    league_id INT,
    season TEXT
);

CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    match_id INT,
    player_id INT,
    team_id INT,
    event_type TEXT,
    minute INT,
    second INT,
    x FLOAT,
    y FLOAT,
    outcome TEXT
);