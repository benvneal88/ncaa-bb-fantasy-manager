# ncaa-bb-fantasy-manager

This project contains a webapp and database for managing ncaa basketball march madness fantasy.

### Running App Locally
    docker compose -f docker-compose.dev.yml up --build

### Running App in Production
    docker compose -f docker-compose.prod.yml up --build


Troubleshooting:

Dependencies:
Use requirements-dev.txt for local development.
Additional dependencies for lxml must be resolved
https://lxml.de/installation.html#requirements


export $(grep -v '^#' .env | xargs)

Data Model

schools

