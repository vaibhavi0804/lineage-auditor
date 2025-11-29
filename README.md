# Lineage Auditor

ML-powered data quality and lineage auditor for enterprise data teams.

## Quick Start

### Local Development

1. **Install dependencies**

```sh
poetry install
cd src/frontend && npm install
```

2. **Start all services**

```sh
docker-compose up -d
```

3. **Run API**

```sh
poetry run uvicorn src.backend.app.main:app --reload
```

4. **Run Frontend**

```sh
cd src/frontend
npm run dev
```

5. **Access**

* Frontend: [http://localhost:5173](http://localhost:5173)
* API: [http://localhost:8000](http://localhost:8000)
* API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
* MinIO Console: [http://localhost:9001](http://localhost:9001)

---

## Architecture

* **Backend:** FastAPI, PostgreSQL, MinIO
* **Frontend:** React + Vite
* **ML:** Scikit-learn, Sentence-Transformers
* **Orchestration:** Apache Airflow (demo)

---

## Project Structure

```
lineage-auditor/
├── src/
│   ├── backend/           # FastAPI application
│   └── frontend/          # React application
├── infra/                 # Docker & deployment
├── data/                  # Datasets & profiles
├── docs/                  # Documentation
└── .github/               # CI/CD workflows
```

---

## Next Steps

* [ ] Set up local development environment
* [ ] Implement dataset ingestion
* [ ] Build profile extraction
* [ ] Add drift detectors
* [ ] Build lineage graph
* [ ] Create UI
* [ ] Deploy to production

---

## License

MIT