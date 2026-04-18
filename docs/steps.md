# Steps

## Github Repository

## Tech Stack

- Python
- FastAPI
- Docker
- Deepface

## Run Docker

Build docker by directly running the `docker-compose up -d --build` in the terminal or by running the `start.sh` file, first time build take a lot of time.

```bash
./start.sh
```

To check status of docker

```bash
docker-compose ps
```

To stop docker

```bash
docker-compose down
```

## Docker Success Log

```bash
PS C:\Users\Hamid\OneDrive\Desktop\intelligent-identity-and-retrieval-engine> docker ps
CONTAINER ID   IMAGE                                           COMMAND                  CREATED          STATUS                    PORTS                                         NAMES
67fa57f97c04   intelligent-identity-and-retrieval-engine-api   "uvicorn src.main:ap…"   11 seconds ago   Up 4 seconds              0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp   grabpic_api
1b3876f7083c   pgvector/pgvector:pg16                          "docker-entrypoint.s…"   12 seconds ago   Up 10 seconds (healthy)   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp   grabpic_db
```
