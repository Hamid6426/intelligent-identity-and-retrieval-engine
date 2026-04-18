# Project Structure

The project follows a modular layout designed for performance, quick iteration, and scalable facial recognition using FastAPI and pgvector.

```text
intelligent-identity-and-retrieval-engine/
├── docs/                      # Documentation and designs
│   ├── architecture.md        # System architecture and design choices
│   ├── project-structure.md   # Directory layout reference
│   └── problem-statement/     # Original hackathon specifications
├── src/                       # Application Source Code
│   ├── main.py                # FastAPI app initialization and endpoints
│   ├── database.py            # Database connection configuration (SQLAlchemy)
│   └── models.py              # Database definitions (Image, Person, Vector Mapping)
├── storage/                   # Directory used as a local ingestion bucket for crawling images
├── docker-compose.yml         # Container orchestration (API, PostgreSQL DB)
├── Dockerfile                 # Slim python build containing DB and compiled native dependencies
├── start.sh                   # Startup script logic
├── stop.sh                    # Teardown script logic
├── requirements.txt           # Python dependencies list
└── README.md                  # Main entry point and instructions
```

## Key Modules
*   **`src/models.py`:** Contains the primary schema. Built using a normalized pattern where `Images` are related to `Persons` (Unique Identifiers) across an intermediate junction table called `FaceEmbedding` which stores the actual 512-length Vector array.
*   **`storage/`:** Intended to act as the raw crawler deposit point where images are evaluated by the ingestion system.
