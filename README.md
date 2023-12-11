# ncaa-bb-fantasy-manager

This project contains a webapp and database for managing ncaa basketball march madness fantasy.

### Developing App Locally
    export $(grep -v '^#' .env | xargs)
    cd services/app/src
    flask --debug run --port 5001

### Running Web App Locally
    docker compose -f docker-compose.dev.yml up --build
    docker compose -f docker-compose.dev.yml down

### Running App in Production
    docker compose -f docker-compose.prod.yml up --build

Getting Started:
    services/app/src >

    from api import model
    model.init_database()

    python3 api/transformations/populate_model.py

Inspecting Database Tables:

    select * from ncaa_fantasy.tbl_ball_team;
    select * from ncaa_fantasy.tbl_fantasy_team;
    select * from ncaa_fantasy.tbl_game;
    select * from ncaa_fantasy.tbl_player;
    select * from ncaa_fantasy.tbl_user;

Troubleshooting:

Dependencies:
Use requirements-dev.txt for local development.
Additional dependencies for lxml must be resolved
https://lxml.de/installation.html#requirements


export $(grep -v '^#' .env | xargs)

Data Model

schools

