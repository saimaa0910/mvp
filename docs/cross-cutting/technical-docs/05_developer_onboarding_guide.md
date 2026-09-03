# 💻 Developer Onboarding & Engineering Handbook
## Namma Clinic Digital Health & Operations Platform
### Engineering Setup, Architecture Guidelines, Git Conventions & Quality Standards
### Document Code: TD-DEV-05 | Version: 1.0 | Date: September 2026

---

## 1. Welcome & Project Orientation

Welcome to the **Namma Clinic Platform** engineering team. We are building the primary healthcare backbone for Bengaluru, digitizing clinical consultations, pharmacy logistics, and disease surveillance for 183+ clinics.

### Technology Stack Summary:
* **Frontend:** Next.js 16 (App Router), React 19, TypeScript, Vanilla CSS design tokens (zero external CSS framework runtime overhead).
* **Backend:** Next.js Server Components & Route Handlers / Node.js API layer.
* **Database:** PostgreSQL 16 (Relational OLTP) + Redis 7 (Caching & Sessions).
* **Interoperability:** ABDM FHIR R4, LOINC, ICD-10, SNOMED CT.
* **Localization:** Bilingual English & Kannada (Noto Sans Kannada).

---

## 2. Local Environment Setup

### 2.1 Prerequisites
Ensure the following tools are installed on your workstation:
* **Node.js:** v24.x LTS (tested on Node v24.19.0+)
* **npm:** v11.x or higher
* **Git:** v2.40+
* **PostgreSQL (Optional for local dev):** v16.x (Or use Docker)
* **VS Code Extensions Recommended:**
  * ESLint (`dbaeumer.vscode-eslint`)
  * Prettier - Code Formatter (`esbenp.prettier-vscode`)
  * Tailwind / CSS Intellisense
  * GitLens

### 2.2 Quickstart Commands
```bash
# 1. Clone repository
git clone https://github.com/kmati/namma-clinic.git
cd namma-clinic

# 2. Install dependencies
npm install

# 3. Configure Environment Variables
cp .env.example .env.local

# 4. Start Local Development Server (Turbopack enabled)
npm run dev

# 5. Open in browser
# Visit http://localhost:3000 to view the running application.
```

### 2.3 Environment Configuration (`.env.local`)
```ini
# Application Port & Host
PORT=3000
NEXT_PUBLIC_APP_ENV=development
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Database Configuration (PostgreSQL 16)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/nammaclinic_dev
REDIS_URL=redis://localhost:6379

# JWT & Authentication Secret (Generate 256-bit key)
JWT_SECRET=super_secret_local_jwt_key_for_development_only_replace_in_prod
JWT_EXPIRY_SECONDS=900

# ABDM Sandbox Credentials
ABDM_SANDBOX_BASE_URL=https://dev.abdm.gov.in/gateway
ABDM_CLIENT_ID=mock_client_id
ABDM_CLIENT_SECRET=mock_client_secret

# SMS Gateway (MSG91 / Mock)
SMS_GATEWAY_API_KEY=mock_key
SMS_SENDER_ID=BBMPNC
```

---

## 3. Project Directory Structure

```
namma-clinic/
├── public/                 # Static assets, logos, favicon
├── src/
│   ├── app/                # Next.js App Router
│   │   ├── globals.css     # Master design system & CSS tokens
│   │   ├── layout.tsx      # Root layout & bilingual font imports
│   │   ├── page.tsx        # Shell orchestrator for all modules
│   │   └── api/            # REST API route handlers
│   ├── components/
│   │   ├── Sidebar.tsx     # Main navigation with dynamic badge counts
│   │   ├── Topbar.tsx      # Top bar with live clinic indicators
│   │   └── modules/        # Domain-driven feature modules
│   │       ├── DashboardModule.tsx     # High-level KPIs & alerts
│   │       ├── RegistrationModule.tsx  # Patient search, token issue
│   │       ├── TriageModule.tsx        # Vitals capture, danger flags
│   │       ├── DoctorModule.tsx        # EMR, templates, prescriptions
│   │       ├── PharmacyModule.tsx      # Stock ledger, indents, dispense
│   │       ├── LabModule.tsx           # Test orders, result entry
│   │       ├── ReferralModule.tsx      # Specialist referrals
│   │       └── AnalyticsModule.tsx     # Zonal & city-level intelligence
│   └── lib/
│       ├── data.ts         # Central in-memory data store & mock fixtures
│       └── utils.ts        # Common validators, BMI calculators, formatters
├── docs/                   # Comprehensive project & governance documentation
│   ├── phase-0/            # Discovery, DPR, field research
│   └── cross-cutting/      # Architecture, security, runbooks, manuals
├── tsconfig.json           # TypeScript strict configuration
└── package.json            # Project dependencies & scripts
```

---

## 4. Git Branching Strategy & Commit Conventions

### 4.1 Branching Flow
* `main`: Protected production branch. Deploys directly to staging/production via CI/CD.
* `develop`: Integration branch for current sprint.
* `feature/<ticket-id>-short-name`: New features (e.g., `feature/NC-42-kannada-print`).
* `bugfix/<ticket-id>-short-name`: Defect fixes (e.g., `bugfix/NC-88-vitals-validation`).
* `hotfix/<ticket-id>-short-name`: Production emergency patches branched directly off `main`.

### 4.2 Conventional Commits
All commit messages must adhere to the Conventional Commits specification:
```
feat(emr): add pediatric dosage calculator for amoxicillin
fix(triage): enforce bp_systolic upper bound constraint of 300 mmHg
docs(runbook): add point-in-time database restore procedure
perf(pharmacy): index stock ledger on clinic_id and expiry_date
```

---

## 5. Coding Standards & Clinical Usability Rules

1. **Bilingual String Handling:** All patient-facing prints, instructions, and labels must support both English and Kannada (`Noto Sans Kannada`). Never hardcode English strings on printed receipts.
2. **Clinical Safety Guards:**
   * Never bypass triage danger flag calculations.
   * Pediatric and elderly doses must display confirmation prompts.
   * High-alert medications (e.g., insulin, antihypertensives) must require batch and strength validation.
3. **Accessibility & Contrast:** The UI uses a modern dark healthcare aesthetic with high-contrast text ratios ($\ge 4.5:1$) compliant with WCAG 2.1 AA standards.
4. **Testing Requirements:**
   ```bash
   # Run linter
   npm run lint

   # Run type checker
   npm run build
   ```
