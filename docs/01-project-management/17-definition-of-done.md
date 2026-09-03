# 🏁 Definition of Done (DoD) for Sprint Delivery
## Namma Clinic Digital Health & Operations Platform
**Document Code:** PM-DOD-17 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. Quality Criteria for Sprint Completion
A User Story or Engineering Task is strictly **DONE** if and only if:
1. **Code & Contract Quality:** Code written in strict TypeScript; zero lint errors; clean architectural boundary compliance.
2. **Automated Unit & Integration Tests:** Unit test coverage >= 85%; all integration contract tests passing cleanly.
3. **E2E Validation:** Critical patient flow automated in Playwright with zero flaky test retries.
4. **Offline Resilience Validated:** Tested with simulated network disconnections and IndexedDB sync verification.
5. **Bilingual Verification:** English and Kannada UI text validated by bilingual clinical coordinator.
6. **Security & Audit Sign-Off:** All sensitive patient data access generates an immutable audit record; no plaintext PII in logs.
7. **CI/CD Quality Gate Passed:** Automated build, container security scan (Trivy), and SonarQube quality gate green.
