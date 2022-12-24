# ncaa-bb-fantasy-manager

`docker compose up`

Build Docker for app
`docker build -f app.Dockerfile -t ncaa_fantasy/app .`
`docker run -d -p 5000:5000 ncaa_fantasy/app`

export $(grep -v '^#' .env | xargs)

Data Model

schools

