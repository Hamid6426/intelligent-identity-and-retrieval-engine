# Grabpic Intelligent Identity & Retrieval Engine

**Vyro Hackathon Backend Application**

Grabpic is a high-performance image processing backend built for large-scale facial recognition events. It uses `Deepface` and PostgreSQL (`pgvector`) to discover, map, and authenticate human faces dynamically across tens of thousands of unsorted gigabytes of photos without requiring external SaaS vector DBs.

## Documentation Index

| Documentation Topic     | Description                                                            | Link                                                                 |
| :---------------------- | :--------------------------------------------------------------------- | :------------------------------------------------------------------- |
| **System Architecture** | Overview of the technology stack, schema design, and vector workflows. | [docs/architecture.md](docs/architecture.md)                         |
| **Project Structure**   | Explanation of codebase organization and the role of each module.      | [docs/project-structure.md](docs/project-structure.md)               |
| **API Testing / Guide** | Step-by-step tutorial on calling and validating endpoints via cURL.    | [docs/testing-app.md](docs/testing-app.md)                           |
| **Problem Statement**   | The original hackathon requirements and judging constraints.           | [docs/problem-statement/README.md](docs/problem-statement/README.md) |

## Quickstart Guide

1. Place raw JPEG/PNG images inside the local `./storage/` folder.
2. Build and run the docker instances (Make sure you have Docker daemon running):
   ```bash
   docker-compose up -d --build
   ```
3. Visit the Swagger documentation dynamically generated at [http://localhost:8000/docs](http://localhost:8000/docs) to easily interact with the ingestion and identification pipelines.
