# 🔬 Backlog Master: Micro-Task Breakdown (MT-0001 through MT-0300)
## Namma Clinic Digital Health & Operations Platform
**Document Code:** BCK-MIC-05 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Sample Granular Micro-Task Decompositions for Critical Tasks

#### TASK-001 / TASK-002: Patient Registration API & Frontend Implementation
1. **MT-0001:** Define TypeScript DTO interface for `PatientCreateRequest` and `PatientResponse`.
2. **MT-0002:** Create runtime Zod validation schema for Indian phone numbers (10 digits starting with 6-9) and age.
3. **MT-0003:** Implement `PatientRepository.create()` method using Prisma with UUIDv7 generation.
4. **MT-0004:** Implement duplicate patient detection logic using pg_trgm similarity matching on (phone, name, age).
5. **MT-0005:** Implement explicit DPDP consent capture recording in `patient_consents` table within same transaction.
6. **MT-0006:** Implement Fastify route handler `POST /api/v1/patients` with `@RequirePermission('patient:create')`.
7. **MT-0007:** Add structured JSON logging emitting `PATIENT_REGISTERED` event to `access_audit_logs`.
8. **MT-0008:** Implement optimistic IndexedDB storage in Dexie.js for offline patient intake.
9. **MT-0009:** Write unit test in Vitest verifying validation error on invalid phone number.
10. **MT-0010:** Write integration test verifying database rollback if consent record insertion fails.
11. **MT-0011:** Write Playwright E2E test verifying complete registration form submission and token print preview.

#### TASK-003 / TASK-004: Electronic Prescription & Pharmacy Dispense
1. **MT-0012:** Define Zod schema for `PrescriptionItem` (drugId, dosage, frequency, durationDays, instructions).
2. **MT-0013:** Implement drug interaction and allergy safety filter checking patient active conditions.
3. **MT-0014:** Implement atomic database transaction deducting medicine batch stock in `pharmacy_stock_ledger`.
4. **MT-0015:** Implement FEFO (First-Expiry-First-Out) batch recommendation algorithm for pharmacist UI.
5. **MT-0016:** Implement thermal print template rendering 2-inch bilingual prescription slip.
6. **MT-0017:** Write concurrency test simulating simultaneous dispensing of the same batch from 2 counters.
