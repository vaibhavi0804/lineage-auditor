# Lineage Auditor – Design Document

## Problem Statement

Data teams spend excessive time manually triaging data quality issues and tracing root causes across complex, multi-stage pipelines. This leads to slow incident resolution, inconsistent assessments, and operational inefficiency.

---

## Solution

An automated system that:

1. Profiles datasets (statistics, metadata, embeddings)
2. Detects schema, semantic, and distribution-level changes
3. Builds and queries dataset lineage graphs
4. Recommends root causes and remediation steps

---

## Architecture

### High-Level Flow

**Upload Dataset → Profile → Compare with Baseline → Detect Issues → Trace Lineage → Recommend Fix**

---

### Components

* **Ingestion:** CSV/Parquet upload or Airflow DAG integration
* **Profiler:** Column statistics, embeddings, sample values
* **Detectors:**

  * Schema change (strict + tolerant matching)
  * Statistical drift (KS, PSI, Chi-squared)
  * Semantic drift (embedding similarity)
  * Anomaly detection (cardinality, nullness, outliers)
* **Lineage:** Graph of dataset dependencies (jobs → datasets → transformations)
* **Diagnosis:** Root-cause ranking engine based on drift signals + lineage context
* **UI:** Dashboard + lineage explorer + issue inspector

---

## Tech Stack

* **Backend:** FastAPI + PostgreSQL
* **Frontend:** React + Vite
* **Storage:** MinIO (local) / Supabase (cloud)
* **ML:** Scikit-learn + Sentence-Transformers
* **Orchestration:** Airflow (demo)
* **Deployment:** Docker + Vercel/Render

---

## Success Metrics

* Schema detection precision ≥ **0.95**
* Semantic classification F1 ≥ **0.92**
* Root-cause attribution accuracy ≥ **0.85**
* Lineage query latency < **300 ms** (for 5000 datasets)
* Data triage time reduction ≥ **60%**

---

## Milestones

* **Week 1:** MVP — ingestion → profiling → schema detection → basic UI
* **Week 2:** ML & semantics — classifier + drift detectors
* **Week 3:** Lineage graph + root-cause engine
* **Week 4:** UI polish, infra hardening, deployment