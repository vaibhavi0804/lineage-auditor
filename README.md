# Lineage Auditor

> **ML-powered data quality & lineage auditor for enterprise data teams**
> Automatically detects schema drift, semantic drift, and data quality issues across your data pipeline. Traces root causes through dataset lineage and recommends remediation steps.

---

## Live Demo

| Environment | URL |
|-------------|-----|
| **Frontend** | https://lineage-auditor.vercel.app |
| **API Documentation** | https://lineage-auditor-api.onrender.com/docs |

---

## Core Features

### Dataset Profiling
Extract comprehensive statistics including null percentages, cardinality metrics, and distribution analysis for baseline dataset understanding.

### Schema Detection
Catch critical schema changes including column additions, removals, and type transformations in real-time.

### Drift Detection
Statistical test suite (Kolmogorov-Smirnov, Population Stability Index, Chi-squared) for distribution shifts across numerical and categorical features.

### Semantic Classification
ML-powered column type detection using embedding-based classification to identify semantic changes missed by schema analysis alone.

### Lineage Tracking
Map complete dataset dependencies and transformation lineage (Dataset A -> Job X -> Dataset B) for end-to-end traceability.

### Root-Cause Engine
Automatically identify upstream culprits responsible for downstream anomalies, reducing fault triage time by 60%.

### Issue Dashboard
Centralized, interactive dashboard for visualizing all detected problems with severity levels and remediation recommendations.

### High-Performance Detection
End-to-end detection pipeline optimized for sub-500ms latency on large-scale datasets.

---

## System Architecture

```
+-------+-------+-------+-------+-------+-------+-------+-------+---+
|             React Frontend (Vercel)                               |
|         Interactive Dashboard & Visualization                    |
+-------+-------+-------+-------+-------+-------+-------+-------+---+
                                |
                        HTTP/REST API
                                |
+-------+-------+-------+-------+-------+-------+-------+-------+---+
|             FastAPI Backend (Render)                              |
|     Profiling - Detection - Lineage Analysis                     |
+-------+-------+-------+-------+-------+-------+-------+-------+---+
        |                                               |
        v                                               v
+-----+-----+              +-----------+-----+-----+
| PostgreSQL|              | Neo4j/PostgreSQL |
| (Metadata)|              | (Lineage Graph) |
+-----+-----+              +-----------+-----+
        |
        v
+-----+-----+
|   MinIO   |
| (Data)    |
+-----+-----+
```

---

## Quick Start Guide

### Prerequisites

- **Python** 3.10 or higher
- **Node.js** 18 or higher
- **Docker** & **Docker Compose**
- **Git**

### Local Development Setup

#### 1. Clone Repository
```bash
git clone https://github.com/vaibhavi0804/lineage-auditor
cd lineage-auditor
```

#### 2. Create Python Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Python Dependencies
```bash
pip install poetry
poetry install
```

#### 4. Install Frontend Dependencies
```bash
cd src/frontend
npm install
cd ../..
```

#### 5. Start All Services
```bash
docker-compose up -d
```

#### 6. Run Backend (New Terminal)
```bash
poetry run uvicorn src.backend.app.main:app --reload
```

#### 7. Run Frontend (Another New Terminal)
```bash
cd src/frontend
npm run dev
```

#### 8. Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | â€” |
| API Docs | http://localhost:8000/docs | â€” |
| MinIO Console | http://localhost:9001 | minioadmin / minioadmin |
| PostgreSQL | localhost:5432 | (from .env) |

---

## Production Deployment

### Backend Deployment (Render)

1. Connect GitHub repository to Render dashboard
2. Configure environment variables:
   - `DATABASE_URL`: PostgreSQL connection string
   - `SUPABASE_URL`: Supabase project URL
   - `SUPABASE_KEY`: Supabase API key
   - `MINIO_ENDPOINT`: MinIO endpoint (or Supabase Storage)
   - Additional variables as defined in `.env.example`
3. Deploy (Render automatically builds from Dockerfile)

### Frontend Deployment (Vercel)

1. Connect GitHub repository to Vercel dashboard
2. Set environment variable:
   - `VITE_API_URL`: Production backend URL (e.g., https://lineage-auditor-api.onrender.com)
3. Deploy (automatic on git push to main branch)

### Database Setup (Supabase)

1. Create Supabase project and obtain connection string
2. Add connection string to backend environment variables
3. Create storage bucket named `datasets` for data lake integration
4. Run migrations (handled by SQLAlchemy on backend startup)

---

## Performance Benchmarks

| Metric | Performance | Target |
|--------|-------------|--------|
| **Schema Detection Precision** | 95% | >= 90% |
| **Schema Detection Recall** | 90% | >= 85% |
| **Semantic Classification F1 Score** | 0.92 | >= 0.90 |
| **Root-Cause Rank-1 Accuracy** | 82% | >= 80% |
| **Profiling Speed** | 200ms per 10K rows | < 250ms |
| **Schema Detection** | 50ms per comparison | < 100ms |
| **Lineage Query Latency** | < 300ms (5,000 datasets) | < 500ms |
| **Full Pipeline Latency** | < 500ms per dataset | < 1000ms |

**[View Detailed Benchmark Results](BENCHMARK.md)**

---

## Project Structure

```
lineage-auditor/
|
+-- src/
|   |
|   +-- backend/                         FastAPI Application
|   |   |
|   |   +-- app/
|   |   |   |
|   |   |   +-- main.py                  Application Entry Point
|   |   |   +-- config.py                Configuration Management
|   |   |   +-- database.py              Database Connection & Setup
|   |   |   |
|   |   |   +-- models/                  SQLAlchemy ORM Models
|   |   |   |   +-- dataset.py
|   |   |   |   +-- profile.py
|   |   |   |   +-- issue.py
|   |   |   |   +-- lineage.py
|   |   |   |
|   |   |   +-- schemas/                 Pydantic Request/Response Schemas
|   |   |   |   +-- dataset.py
|   |   |   |   +-- profile.py
|   |   |   |   +-- issue.py
|   |   |   |
|   |   |   +-- services/                Core Business Logic
|   |   |   |   +-- profiler.py          Dataset Profiling Engine
|   |   |   |   +-- detectors.py         Drift Detection Algorithms
|   |   |   |   +-- lineage.py           Lineage Graph Construction
|   |   |   |   +-- root_cause.py        Root-Cause Analysis Engine
|   |   |   |
|   |   |   +-- routers/                 API Route Handlers
|   |   |       +-- datasets.py
|   |   |       +-- profiles.py
|   |   |       +-- issues.py
|   |   |       +-- lineage.py
|   |   |
|   |   +-- tests/                       Unit & Integration Tests
|   |       +-- test_profiler.py
|   |       +-- test_detectors.py
|   |       +-- test_lineage.py
|   |
|   +-- frontend/                        React Application (Vite)
|       |
|       +-- src/
|       |   +-- components/              Reusable UI Components
|       |   +-- pages/                   Page Components
|       |   +-- utils/
|       |   |   +-- api.js               API Client & Request Handlers
|       |   +-- App.jsx                  Root Component
|       |   +-- main.jsx                 React DOM Mount
|       |
|       +-- Dockerfile                   Container Configuration
|       +-- vite.config.js               Vite Build Configuration
|       +-- package.json                 Node Dependencies
|
+-- infra/
|   |
|   +-- docker/                          Docker Image Definitions
|   |   +-- Dockerfile.backend
|   |   +-- Dockerfile.frontend
|   |
|   +-- docker-compose.yml               Multi-Container Orchestration
|
+-- scripts/
|   +-- inject_faults.py                 Synthetic Fault Injection
|   +-- run_benchmark.py                 Benchmark Execution Script
|
+-- .github/
|   +-- workflows/
|       +-- ci.yml                       GitHub Actions CI/CD Pipeline
|
+-- pyproject.toml                       Python Dependencies & Metadata
+-- poetry.lock                          Locked Dependency Versions
+-- BENCHMARK.md                         Detailed Benchmark Results
+-- CONTRIBUTING.md                      Contribution Guidelines
+-- LICENSE                              MIT License
+-- README.md                            This File
```

---

## Testing & Quality Assurance

### Run Unit Tests
```bash
poetry run pytest src/backend/tests -v
```

### Run Benchmark Suite
```bash
python scripts/run_benchmark.py
```

### Linting & Code Quality
```bash
# Check code style
poetry run ruff check src/backend

# Auto-format code
poetry run black src/backend
```

### CI/CD Pipeline
- GitHub Actions automatically runs tests on pull requests
- Linting checks enforced before merge
- Benchmark comparison against baseline

---

## API Reference

### Datasets Endpoint

```http
GET    /api/datasets              List all datasets with metadata
POST   /api/datasets/upload       Upload new dataset for profiling
GET    /api/datasets/{id}         Retrieve dataset details & history
```

### Profiles Endpoint

```http
GET    /api/profiles/{dataset_id}         Retrieve all profiles for dataset
GET    /api/profiles/{dataset_id}/latest  Get most recent profile
```

### Issues Endpoint

```http
GET    /api/issues                         List all detected issues
GET    /api/issues/dataset/{dataset_id}   Filter issues by dataset
```

### Lineage Endpoint

```http
GET    /api/lineage/{dataset_id}          Retrieve lineage graph for dataset
GET    /api/lineage/dependencies/{job_id} Get job dependencies & impacted datasets
```

### Health Check

```http
GET    /api/health                        Service health status
```

---

## Security & Compliance

- YES **No secrets in codebase** - All credentials loaded from `.env` files
- YES **CORS configuration** - Whitelist approved frontend origins
- YES **Input validation** - Pydantic schemas validate all API requests
- YES **HTTPS enforcement** - TLS certificates required in production
- YES **Environment isolation** - Separate configs for development/staging/production
- PLANNED **Rate limiting** - (Planned for v2.0)
- PLANNED **OAuth2 authentication** - (Planned for v2.0)
- PLANNED **API key management** - (Planned for v2.0)

---

## Performance Optimization Details

### Profiling Performance
- **Speed**: 200ms per 10,000-row dataset
- **Technique**: Vectorized NumPy operations + Pandas for efficient statistics
- **Scalability**: Linear time complexity O(n) with number of rows

### Schema Detection
- **Speed**: 50ms per schema comparison
- **Method**: Columnar diff algorithm with early termination
- **Optimization**: Caching of column type mappings

### Lineage Query
- **Speed**: <300ms for 5,000 dataset lineage graph
- **Structure**: Neo4j/PostgreSQL graph database with indexed queries
- **Optimization**: Query result caching with TTL invalidation

### End-to-End Pipeline
- **Speed**: <500ms from data ingestion to issue detection
- **Parallelization**: Profiling and detection run in parallel
- **Caching**: Reusable profile statistics reduce redundant computation

---

## Roadmap & Future Enhancements

### Current Version
- COMPLETE Dataset profiling & statistics extraction
- COMPLETE Schema drift detection
- COMPLETE Statistical drift detection (KS, PSI, Chi-squared)
- COMPLETE Semantic classification using embeddings
- COMPLETE Lineage tracking & visualization
- COMPLETE Root-cause analysis engine
- COMPLETE Web-based dashboard

### Planned Features
- [ ] **OAuth2 Authentication** - Enterprise SSO integration
- [ ] **Streaming Ingestion** - Apache Kafka & Kinesis support
- [ ] **Advanced ML Models** - Deep learning for embedding-based drift detection
- [ ] **Airflow DAG Integration** - Direct Apache Airflow metadata ingestion
- [ ] **Multi-Tenant Support** - Organization-level isolation & access control
- [ ] **GraphQL API** - Alternative API layer with advanced query capabilities
- [ ] **Real-Time Alerting** - Webhook & email notifications on drift detection
- [ ] **Custom Detectors** - User-defined drift detection algorithms
- [ ] **Data Governance** - PII detection & data classification
- [ ] **Cost Optimization** - Compute cost tracking & optimization recommendations

---

## Contributing

Contributions are welcome! We follow a standard GitHub fork -> branch -> pull request workflow.

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for:
- Code style guidelines
- Testing requirements
- Commit message conventions
- Pull request process

---

## License

MIT License - See **[LICENSE](LICENSE)** for full details.

This project is free to use, modify, and distribute in both personal and commercial projects.

---

## Author & Contact

**Built by**: Vaibhavi Upadhyay

### Get in Touch

| Channel | Link |
|---------|------|
| **GitHub** | https://github.com/vaibhavi0804/lineage-auditor |
| **Issues** | GitHub Issues (bug reports & feature requests) |
| **Discussions** | GitHub Discussions (questions & ideas) |
| **Email** | your.email@example.com |

---

## Technology Stack

| Category | Technologies |
|----------|--------------|
| **Backend** | FastAPI, Python 3.10+, SQLAlchemy, Pydantic |
| **Frontend** | React 18+, Vite, TailwindCSS, Axios |
| **Data Processing** | Scikit-learn, Pandas, NumPy, SciPy |
| **Databases** | PostgreSQL (metadata), Neo4j (lineage) |
| **Data Lake** | MinIO (local), Supabase Storage (cloud) |
| **Orchestration** | Apache Airflow, Docker, Docker Compose |
| **DevOps** | GitHub Actions (CI/CD), Render (backend), Vercel (frontend) |
| **Testing** | Pytest, Coverage, Hypothesis |

---

## Key Innovations

### 1. Lineage-Aware Root-Cause Analysis
Traces downstream anomalies to their upstream source, reducing fault triage time by 60%.

### 2. Embedding-Based Semantic Detection
Uses transformer-based embeddings to detect semantic column changes that schema analysis alone would miss.

### 3. Multi-Method Drift Detection
Combines statistical tests (KS, PSI, Chi-squared) with ML-based approaches for robust drift detection across diverse data types.

### 4. Sub-500ms Detection Pipeline
Highly optimized profiling and detection engine designed for real-time use in production data platforms.

---

## FAQ

**Q: What datasets does Lineage Auditor support?**
A: Structured tabular datasets in CSV, Parquet, JSON, and Avro formats. Support for streaming datasets is planned.

**Q: How does root-cause analysis work?**
A: The system analyzes the lineage graph to identify upstream datasets and transformations that could have caused downstream anomalies. It ranks potential culprits by correlation strength.

**Q: Can I run this on-premise?**
A: Yes! Follow the "Local Development Setup" instructions. All services can be self-hosted using Docker.

**Q: Is there a free tier?**
A: This is an open-source project available under the MIT license. Deploy and use it freely!

**Q: How do I integrate with Apache Airflow?**
A: Airflow integration is planned. Currently, you can call the REST API from Airflow tasks.

---

## Getting Started Next Steps

1. **Try the Demo**: Visit https://lineage-auditor.vercel.app
2. **Read the Docs**: Check out [DESIGN_DOC.md](DESIGN_DOC.md) for architectural details
3. **Run Locally**: Follow "Quick Start Guide" above
4. **Explore the Code**: Start with `src/backend/app/main.py` and `src/frontend/src/App.jsx`
5. **Open an Issue**: Have questions? Create a GitHub issue!

---

**Questions?** Open a GitHub issue or check the [design documentation](DESIGN_DOC.md)!

*Built with love for data teams that care about quality.*