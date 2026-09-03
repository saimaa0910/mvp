# 🌐 Six-Tier Environment Strategy & Promotion Pipeline
## Namma Clinic Digital Health & Operations Platform
**Document Code:** DEV-ENV-02 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Environment Architecture & Isolation Matrix

| Environment | Purpose | Infrastructure & Sizing | Database Strategy | Deployment Trigger | Approval Required |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Local** | Developer workstation development and unit testing. | Docker Compose (Node, PG16, Redis). | Ephemeral Docker container with synthetic seed data. | Manual `docker compose up`. | None (Developer). |
| **Development** | Continuous integration testing and feature branch verification. | AWS ECS Fargate / Single RDS instance (`db.t4g.medium`). | Shared Dev DB with automated daily seed reset. | Push to `feature/*` or `develop`. | Automated CI green. |
| **Test (QA)** | System integration testing, automated regression, and load testing. | AWS ECS Fargate / RDS Multi-AZ (`db.t4g.large`). | Test DB with sanitized synthetic 10k patient datasets. | Automated merge to `develop`. | QA Lead sign-off. |
| **Staging** | Production mirror for UAT, security scans, and rehearsal. | AWS ECS Fargate / RDS Multi-AZ (`db.m6g.xlarge`). | Anonymized production-like data snapshot. | Automated merge to `release/*`. | Architect & PM. |
| **Pilot (20 Clinics)**| Live field deployment in 20 designated pilot Namma Clinics. | Dedicated VPC / Production RDS Multi-AZ (`db.r6g.xlarge`). | Production pilot database with full PITR backups. | Manual release tag `v1.0.0-pilot`. | GBA Steering Gate 11. |
| **Production (183 Clinics)**| Citywide live operational deployment across Bengaluru. | High-Availability Multi-AZ (`db.r6g.2xlarge` + Read Replicas). | Sovereign Production Database with strict encryption. | Manual release tag `v1.0.0`. | Gate 12 Final Approval. |
