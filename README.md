# Lineage Auditor

> **ML-powered data quality & lineage auditor for enterprise data teams**  
> Automatically detects schema drift, semantic drift, and data quality issues across your data pipeline. Traces root causes through dataset lineage and recommends remediation steps.

---

## ðŸŽ¯ Live Demo

| Environment | URL |
|-------------|-----|
| **Frontend** | https://lineage-auditor.vercel.app |
| **API Documentation** | https://lineage-auditor-api.onrender.com/docs |

---

## âœ¨ Core Features

### ðŸ“Š **Dataset Profiling**
Extract comprehensive statistics including null percentages, cardinality metrics, and distribution analysis for baseline dataset understanding.

### ðŸ” **Schema Detection**
Catch critical schema changes including column additions, removals, and type transformations in real-time.

### ðŸ“ˆ **Drift Detection**
Statistical test suite (Kolmogorov-Smirnov, Population Stability Index, Chi-squared) for distribution shifts across numerical and categorical features.

### ðŸ·ï¸ **Semantic Classification**
ML-powered column type detection using embedding-based classification to identify semantic changes missed by schema analysis alone.

### ðŸ”— **Lineage Tracking**
Map complete dataset dependencies and transformation lineage (Dataset A â†’ Job X â†’ Dataset B) for end-to-end traceability.

### ðŸŽ¯ **Root-Cause Engine**
Automatically identify upstream culprits responsible for downstream anomalies, reducing fault triage time by 60%.

### ðŸ“‹ **Issue Dashboard**
Centralized, interactive dashboard for visualizing all detected problems with severity levels and remediation recommendations.

### âš¡ **High-Performance Detection**
End-to-end detection pipeline optimized for sub-500ms latency on large-scale datasets.

---

## ðŸ—ï¸ System Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    React Frontend (Vercel)                      â”‚
â”‚              Interactive Dashboard & Visualization              â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                         â”‚ HTTP/REST API
                         â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                 FastAPI Backend (Render)                        â”‚
â”‚         Profiling â€¢ Detection â€¢ Lineage Analysis                â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
             â”‚                                â”‚
             â–¼                                â–¼
   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”          â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
   â”‚  PostgreSQL      â”‚          â”‚   Neo4j/PostgreSQL      â”‚
   â”‚  (Metadata)      â”‚          â”‚   (Lineage Graph)       â”‚
   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜          â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
             â”‚
             â–¼
   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
   â”‚     MinIO        â”‚
   â”‚   (Data Lake)    â”‚
   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## ðŸš€ Quick Start Guide

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

## ðŸŒ Production Deployment

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

## ðŸ“Š Performance Benchmarks

| Metric | Performance | Target |
|--------|-------------|--------|
| **Schema Detection Precision** | 95% | â‰¥ 90% |
| **Schema Detection Recall** | 90% | â‰¥ 85% |
| **Semantic Classification F1 Score** | 0.92 | â‰¥ 0.90 |
| **Root-Cause Rank-1 Accuracy** | 82% | â‰¥ 80% |
| **Profiling Speed** | 200ms per 10K rows | < 250ms |
| **Schema Detection** | 50ms per comparison | < 100ms |
| **Lineage Query Latency** | < 300ms (5,000 datasets) | < 500ms |
| **Full Pipeline Latency** | < 500ms per dataset | < 1000ms |

ðŸ‘‰ **[View Detailed Benchmark Results â†’](BENCHMARK.md)**

---

## ðŸ“ Project Structure

```
lineage-auditor/
â”‚
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ backend/                          # FastAPI Application
â”‚   â”‚   â”œâ”€â”€ app/
â”‚   â”‚   â”‚   â”œâ”€â”€ main.py                   # Application Entry Point
â”‚   â”‚   â”‚   â”œâ”€â”€ config.py                 # Configuration Management
â”‚   â”‚   â”‚   â”œâ”€â”€ database.py               # Database Connection & Setup
â”‚   â”‚   â”‚   â”‚
â”‚   â”‚   â”‚   â”œâ”€â”€ models/                   # SQLAlchemy ORM Models
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ dataset.py
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ profile.py
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ issue.py
â”‚   â”‚   â”‚   â”‚   â””â”€â”€ lineage.py
â”‚   â”‚   â”‚   â”‚
â”‚   â”‚   â”‚   â”œâ”€â”€ schemas/                  # Pydantic Request/Response Schemas
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ dataset.py
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ profile.py
â”‚   â”‚   â”‚   â”‚   â””â”€â”€ issue.py
â”‚   â”‚   â”‚   â”‚
â”‚   â”‚   â”‚   â”œâ”€â”€ services/                 # Core Business Logic
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ profiler.py           # Dataset Profiling Engine
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ detectors.py          # Drift Detection Algorithms
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ lineage.py            # Lineage Graph Construction
â”‚   â”‚   â”‚   â”‚   â””â”€â”€ root_cause.py         # Root-Cause Analysis Engine
â”‚   â”‚   â”‚   â”‚
â”‚   â”‚   â”‚   â””â”€â”€ routers/                  # API Route Handlers
â”‚   â”‚   â”‚       â”œâ”€â”€ datasets.py
â”‚   â”‚   â”‚       â”œâ”€â”€ profiles.py
â”‚   â”‚   â”‚       â”œâ”€â”€ issues.py
â”‚   â”‚   â”‚       â””â”€â”€ lineage.py
â”‚   â”‚   â”‚
â”‚   â”‚   â””â”€â”€ tests/                        # Unit & Integration Tests
â”‚   â”‚       â”œâ”€â”€ test_profiler.py
â”‚   â”‚       â”œâ”€â”€ test_detectors.py
â”‚   â”‚       â””â”€â”€ test_lineage.py
â”‚   â”‚
â”‚   â””â”€â”€ frontend/                         # React Application (Vite)
â”‚       â”œâ”€â”€ src/
â”‚       â”‚   â”œâ”€â”€ components/               # Reusable UI Components
â”‚       â”‚   â”œâ”€â”€ pages/                    # Page Components
â”‚       â”‚   â”œâ”€â”€ utils/
â”‚       â”‚   â”‚   â””â”€â”€ api.js                # API Client & Request Handlers
â”‚       â”‚   â”œâ”€â”€ App.jsx                   # Root Component
â”‚       â”‚   â””â”€â”€ main.jsx                  # React DOM Mount
â”‚       â”‚
â”‚       â”œâ”€â”€ Dockerfile                    # Container Configuration
â”‚       â”œâ”€â”€ vite.config.js                # Vite Build Configuration
â”‚       â””â”€â”€ package.json                  # Node Dependencies
â”‚
â”œâ”€â”€ infra/
â”‚   â”œâ”€â”€ docker/                           # Docker Image Definitions
â”‚   â”‚   â”œâ”€â”€ Dockerfile.backend
â”‚   â”‚   â””â”€â”€ Dockerfile.frontend
â”‚   â”‚
â”‚   â””â”€â”€ docker-compose.yml                # Multi-Container Orchestration
â”‚
â”œâ”€â”€ scripts/
â”‚   â”œâ”€â”€ inject_faults.py                  # Synthetic Fault Injection
â”‚   â””â”€â”€ run_benchmark.py                  # Benchmark Execution Script
â”‚
â”œâ”€â”€ .github/
â”‚   â””â”€â”€ workflows/
â”‚       â””â”€â”€ ci.yml                        # GitHub Actions CI/CD Pipeline
â”‚
â”œâ”€â”€ pyproject.toml                        # Python Dependencies & Metadata
â”œâ”€â”€ poetry.lock                           # Locked Dependency Versions
â”œâ”€â”€ BENCHMARK.md                          # Detailed Benchmark Results
â”œâ”€â”€ CONTRIBUTING.md                       # Contribution Guidelines
â”œâ”€â”€ LICENSE                               # MIT License
â””â”€â”€ README.md                             # This File
```

---

## ðŸ§ª Testing & Quality Assurance

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

## ðŸ“š API Reference

### Datasets Endpoint

```http
GET    /api/datasets              # List all datasets with metadata
POST   /api/datasets/upload       # Upload new dataset for profiling
GET    /api/datasets/{id}         # Retrieve dataset details & history
```

### Profiles Endpoint

```http
GET    /api/profiles/{dataset_id}         # Retrieve all profiles for dataset
GET    /api/profiles/{dataset_id}/latest  # Get most recent profile
```

### Issues Endpoint

```http
GET    /api/issues                         # List all detected issues
GET    /api/issues/dataset/{dataset_id}   # Filter issues by dataset
```

### Lineage Endpoint

```http
GET    /api/lineage/{dataset_id}          # Retrieve lineage graph for dataset
GET    /api/lineage/dependencies/{job_id} # Get job dependencies & impacted datasets
```

### Health Check

```http
GET    /api/health                        # Service health status
```

---

## ðŸ” Security & Compliance

- âœ… **No secrets in codebase** â€“ All credentials loaded from `.env` files
- âœ… **CORS configuration** â€“ Whitelist approved frontend origins
- âœ… **Input validation** â€“ Pydantic schemas validate all API requests
- âœ… **HTTPS enforcement** â€“ TLS certificates required in production
- âœ… **Environment isolation** â€“ Separate configs for development/staging/production
- â³ **Rate limiting** â€“ (Planned for v2.0)
- â³ **OAuth2 authentication** â€“ (Planned for v2.0)
- â³ **API key management** â€“ (Planned for v2.0)

---

## âš¡ Performance Optimization Details

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

## ðŸ›£ï¸ Roadmap & Future Enhancements

### Current Version
- âœ… Dataset profiling & statistics extraction
- âœ… Schema drift detection
- âœ… Statistical drift detection (KS, PSI, Chi-squared)
- âœ… Semantic classification using embeddings
- âœ… Lineage tracking & visualization
- âœ… Root-cause analysis engine
- âœ… Web-based dashboard

### Planned Features
- [ ] **OAuth2 Authentication** â€“ Enterprise SSO integration
- [ ] **Streaming Ingestion** â€“ Apache Kafka & Kinesis support
- [ ] **Advanced ML Models** â€“ Deep learning for embedding-based drift detection
- [ ] **Airflow DAG Integration** â€“ Direct Apache Airflow metadata ingestion
- [ ] **Multi-Tenant Support** â€“ Organization-level isolation & access control
- [ ] **GraphQL API** â€“ Alternative API layer with advanced query capabilities
- [ ] **Real-Time Alerting** â€“ Webhook & email notifications on drift detection
- [ ] **Custom Detectors** â€“ User-defined drift detection algorithms
- [ ] **Data Governance** â€“ PII detection & data classification
- [ ] **Cost Optimization** â€“ Compute cost tracking & optimization recommendations

---

## ðŸ¤ Contributing

Contributions are welcome! We follow a standard GitHub fork â†’ branch â†’ pull request workflow.

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for:
- Code style guidelines
- Testing requirements
- Commit message conventions
- Pull request process

---

## ðŸ“ License

MIT License â€“ See **[LICENSE](LICENSE)** for full details.

This project is free to use, modify, and distribute in both personal and commercial projects.

---

## ðŸ‘¤ Author & Contact

**Built by**: Vaibhavi Upadhyay

### Get in Touch

| Channel | Link |
|---------|------|
| **GitHub** | https://github.com/vaibhavi0804/lineage-auditor |
| **Issues** | GitHub Issues (bug reports & feature requests) |
| **Discussions** | GitHub Discussions (questions & ideas) |
| **Email** | your.email@example.com |

---

## ðŸ“‹ Technology Stack

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

## ðŸŽ“ Key Innovations

### 1. **Lineage-Aware Root-Cause Analysis**
Traces downstream anomalies to their upstream source, reducing fault triage time by 60%.

### 2. **Embedding-Based Semantic Detection**
Uses transformer-based embeddings to detect semantic column changes that schema analysis alone would miss.

### 3. **Multi-Method Drift Detection**
Combines statistical tests (KS, PSI, Chi-squared) with ML-based approaches for robust drift detection across diverse data types.

### 4. **Sub-500ms Detection Pipeline**
Highly optimized profiling and detection engine designed for real-time use in production data platforms.

---

## â“ FAQ

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

## ðŸš€ Getting Started Next Steps

1. **Try the Demo**: Visit [https://lineage-auditor.vercel.app](https://lineage-auditor.vercel.app)
2. **Read the Docs**: Check out [DESIGN_DOC.md](DESIGN_DOC.md) for architectural details
3. **Run Locally**: Follow "Quick Start Guide" above
4. **Explore the Code**: Start with `src/backend/app/main.py` and `src/frontend/src/App.jsx`
5. **Open an Issue**: Have questions? Create a GitHub issue!

---

**Questions?** Open a GitHub issue or check the [design documentation](DESIGN_DOC.md)!

*Built with â¤ï¸ for data teams that care about quality.*