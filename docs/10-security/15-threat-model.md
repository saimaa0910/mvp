# 🛡️ Threat Model & STRIDE Vulnerability Analysis
## Namma Clinic Digital Health & Operations Platform
**Document Code:** SEC-STR-15 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. STRIDE Threat Analysis Matrix across 10 Attack Vectors

| Threat Vector | STRIDE Category | Threat Scenario | Impact | Security Control & Countermeasure | Verification Method |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **TV-01** | Spoofing | Adversary impersonates clinic doctor using stolen credentials. | High | WebAuthn / OTP MFA for sensitive access; automatic 15-min session timeout. | Auth Penetration Test |
| **TV-02** | Tampering | Malicious actor modifies drug stock counts in transit. | High | TLS 1.3 end-to-end encryption; cryptographic HMAC signatures on API requests. | MitM Proxy Inspection |
| **TV-03** | Repudiation | Staff member deletes patient consultation and denies action. | Critical | Append-only partitioned `access_audit_logs` with SHA-256 hash chaining. | Audit Log Integrity Test |
| **TV-04** | Info Disclosure | Unencrypted database dump leaks citizen diagnostic history. | Critical | AES-256-GCM data-at-rest encryption; KMS envelope keys; column-level masking. | Storage Encryption Audit |
| **TV-05** | Denial of Service | Flooding clinic API with bogus requests to halt registrations. | High | Redis leaky-bucket rate limiting; Cloudflare / AWS WAF DDoS mitigation. | k6 Stress Simulation |
| **TV-06** | Elevation of Priv | Staff nurse crafts API request to approve monthly indents. | High | Strict RBAC middleware checking user permissions on every route handler. | Privilege Escalation Test |
| **TV-07** | Offline Theft | Physical theft of clinic Android tablet containing cached visits. | Critical | Full disk encryption (Android dm-crypt); encrypted Dexie.js store; remote wipe. | Device Seizure Test |
| **TV-08** | Token Hijacking | XSS attack steals JWT session token from browser localStorage. | High | Tokens stored strictly in HttpOnly, SameSite=Strict cookies; strict CSP. | XSS Injection Test |
| **TV-09** | SQL Injection | SQL injection via patient search bar compromises database. | Critical | 100% parameterized queries via Prisma / Kysely ORM; zero raw string SQL. | DAST Static Analysis |
| **TV-10** | Supply Chain | Compromised npm dependency injects backdoor into clinic app. | Critical | Automated Dependabot & Snyk scanning; lockfile verification; signed builds. | SBOM & Trivy Scanner |
