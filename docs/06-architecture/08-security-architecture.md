# 🛡️ Architecture Document 08: Enterprise Security Architecture & Threat Specification
## Namma Clinic Digital Health & Operations Platform
### Greater Bengaluru Authority (GBA) / BBMP Health Department
**Standard:** Zero-Trust / STRIDE / NIST SP 800-53 / DPDP Act 2023 | **Status:** APPROVED BASELINE | **Code:** `ARCH-SEC-08`

---

## 01. Document Overview & Zero-Trust Security Philosophy
This document specifies the authoritative enterprise security architecture, cryptographic foundations, threat models, access control mechanisms, and regulatory compliance standards for the Namma Clinic Digital Health & Operations Platform. The system implements a comprehensive **Zero-Trust Architecture (ZTA)** conforming to NIST SP 800-207 and MeitY Guidelines for Cloud and Edge Deployments.

### 01.1 Core Security Principles & Invariants
1. **Continuous Identity Verification:** Every API invocation, database transaction, and inter-service call must be explicitly authenticated, authorized, and cryptographically verified. No implicit trust is granted based on internal network location, IP subnet, or physical clinic presence.
2. **Principle of Least Privilege (PoLP):** All user accounts, service accounts, and edge daemons are restricted to the minimum capability claims necessary to perform their immediate clinical or operational duties.
3. **Cryptographic Segregation of Duties (SOD-001):** Hard programmatic, database, and token-level barriers enforce absolute separation between prescribing physicians and dispensing pharmacists, eliminating single points of failure, medication fraud, and adverse clinical errors.
4. **Defense-in-Depth:** Layered security controls spanning physical appliance locks, hardware TPM 2.0 enclaves, OS hardening, network micro-segmentation, application WAF, database column encryption, and immutable WORM audit logs.
5. **Statutory DPDP Act 2023 Compliance:** All Protected Health Information (PHI) and Personally Identifiable Information (PII) are governed by affirmative digital consent, purpose specification, and strict retention limits.
6. **Rapid Incident Reporting (CERT-In 6-Hour SLA):** Automated alerting and forensic runbooks ensure confirmed cybersecurity incidents are triaged, contained, and reported to the Indian Computer Emergency Response Team (CERT-In) within statutory 6-hour windows.

## 02. STRIDE Threat Modeling Analysis Across All 18 Containers
Detailed threat model evaluating Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege across the 18 platform containers:

### 02.01 STRIDE Threat Analysis: `ARCH-CONT-001` (Clinic Workstation PWA Shell)
- **Container Identifier:** `ARCH-CONT-001`
- **Container Title:** Clinic Workstation PWA Shell
- **Architectural Classification:** Frontend Client
- **Runtime Technology:** Next.js / TypeScript / React / TailwindCSS
- **Deployment Context:** Local Workstation / Tablet
- **Associated Data Stores:** `IndexedDB / SQLite Edge`
- **Governing Product Modules:** MODULE-001..026

#### Threat Profile & Specific Mitigations:
1. **Threat Category: Spoofing**
   - **Vulnerability Scenario:** Adversary impersonates an authorized staff member or node. targeting `ARCH-CONT-001`.
   - **Architectural Control:** RS256 JWT tokens with hardware-bound certificates, Argon2id MFA, mutual TLS (mTLS) for edge nodes.
   - **Verification Test:** Verify client certificate chain and check JWT signature against JWKS endpoint.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Tampering**
   - **Vulnerability Scenario:** Malicious modification of clinical records, prescriptions, or batch logs. targeting `ARCH-CONT-001`.
   - **Architectural Control:** TLS 1.3 in-flight encryption, AES-256 GCM storage, SHA-256 HMAC digital signatures on sealed encounters.
   - **Verification Test:** Assert checksum matches SHA-256 hash of payload before accepting updates.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Repudiation**
   - **Vulnerability Scenario:** Provider or pharmacist denies performing a critical clinical action. targeting `ARCH-CONT-001`.
   - **Architectural Control:** Cryptographic WORM append-only audit ledger linking every transaction to a verified staff key.
   - **Verification Test:** Query WORM audit chain to verify cryptographic signature and immutable timestamp.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Information Disclosure**
   - **Vulnerability Scenario:** Unauthorized exfiltration of sensitive patient diagnoses, HIV/TB status, or IDs. targeting `ARCH-CONT-001`.
   - **Architectural Control:** Field-level column encryption, strict ABAC clinic scoping, automated PII log scrubber.
   - **Verification Test:** Inspect logs for redacted patterns and verify ciphertext in database dumps.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Denial of Service**
   - **Vulnerability Scenario:** Volumetric DDoS attack or retry storms exhausting edge server memory or cloud APIs. targeting `ARCH-CONT-001`.
   - **Architectural Control:** Redis token-bucket rate limiting, edge offline fallback mode, Cloudflare/Envoy WAF traffic filtering.
   - **Verification Test:** Simulate 5,000 req/min and verify HTTP 429 response without database degradation.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Elevation of Privilege**
   - **Vulnerability Scenario:** Frontline staff member exploits API flaw to gain prescribing or admin rights. targeting `ARCH-CONT-001`.
   - **Architectural Control:** Hardened NestJS RolesGuard, immutable capability claim enforcement, zero-trust token inspection.
   - **Verification Test:** Attempt API call with forged role claim and confirm immediate HTTP 403 Forbidden.
   - **Residual Risk Level:** Low (Controlled)

#### Container Runtime Hardening Directives:
- **Container Security Profile:** Non-root execution (`USER 10001:10001`), read-only rootfs (`readOnlyRootFilesystem: true`).
- **Linux Capability Dropping:** `securityContext.capabilities.drop: ['ALL']`.
- **Network Policy:** Egress restricted to approved service CIDRs; ingress strictly via service mesh.
- **Vulnerability SLA:** Zero Critical/High CVEs allowed in base container image; nightly Trivy rescan.

---

### 02.02 STRIDE Threat Analysis: `ARCH-CONT-002` (Clinic Edge Mini-Server Runtime)
- **Container Identifier:** `ARCH-CONT-002`
- **Container Title:** Clinic Edge Mini-Server Runtime
- **Architectural Classification:** Edge Computing Node
- **Runtime Technology:** Node.js / Express / Bun / SQLite WAL
- **Deployment Context:** Clinic Edge Appliance (Intel N100)
- **Associated Data Stores:** `SQLite WAL Mode (Local SSD)`
- **Governing Product Modules:** MODULE-027, MODULE-028

#### Threat Profile & Specific Mitigations:
1. **Threat Category: Spoofing**
   - **Vulnerability Scenario:** Adversary impersonates an authorized staff member or node. targeting `ARCH-CONT-002`.
   - **Architectural Control:** RS256 JWT tokens with hardware-bound certificates, Argon2id MFA, mutual TLS (mTLS) for edge nodes.
   - **Verification Test:** Verify client certificate chain and check JWT signature against JWKS endpoint.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Tampering**
   - **Vulnerability Scenario:** Malicious modification of clinical records, prescriptions, or batch logs. targeting `ARCH-CONT-002`.
   - **Architectural Control:** TLS 1.3 in-flight encryption, AES-256 GCM storage, SHA-256 HMAC digital signatures on sealed encounters.
   - **Verification Test:** Assert checksum matches SHA-256 hash of payload before accepting updates.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Repudiation**
   - **Vulnerability Scenario:** Provider or pharmacist denies performing a critical clinical action. targeting `ARCH-CONT-002`.
   - **Architectural Control:** Cryptographic WORM append-only audit ledger linking every transaction to a verified staff key.
   - **Verification Test:** Query WORM audit chain to verify cryptographic signature and immutable timestamp.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Information Disclosure**
   - **Vulnerability Scenario:** Unauthorized exfiltration of sensitive patient diagnoses, HIV/TB status, or IDs. targeting `ARCH-CONT-002`.
   - **Architectural Control:** Field-level column encryption, strict ABAC clinic scoping, automated PII log scrubber.
   - **Verification Test:** Inspect logs for redacted patterns and verify ciphertext in database dumps.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Denial of Service**
   - **Vulnerability Scenario:** Volumetric DDoS attack or retry storms exhausting edge server memory or cloud APIs. targeting `ARCH-CONT-002`.
   - **Architectural Control:** Redis token-bucket rate limiting, edge offline fallback mode, Cloudflare/Envoy WAF traffic filtering.
   - **Verification Test:** Simulate 5,000 req/min and verify HTTP 429 response without database degradation.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Elevation of Privilege**
   - **Vulnerability Scenario:** Frontline staff member exploits API flaw to gain prescribing or admin rights. targeting `ARCH-CONT-002`.
   - **Architectural Control:** Hardened NestJS RolesGuard, immutable capability claim enforcement, zero-trust token inspection.
   - **Verification Test:** Attempt API call with forged role claim and confirm immediate HTTP 403 Forbidden.
   - **Residual Risk Level:** Low (Controlled)

#### Container Runtime Hardening Directives:
- **Container Security Profile:** Non-root execution (`USER 10001:10001`), read-only rootfs (`readOnlyRootFilesystem: true`).
- **Linux Capability Dropping:** `securityContext.capabilities.drop: ['ALL']`.
- **Network Policy:** Egress restricted to approved service CIDRs; ingress strictly via service mesh.
- **Vulnerability SLA:** Zero Critical/High CVEs allowed in base container image; nightly Trivy rescan.

---

### 02.03 STRIDE Threat Analysis: `ARCH-CONT-003` (Central Cloud API Gateway)
- **Container Identifier:** `ARCH-CONT-003`
- **Container Title:** Central Cloud API Gateway
- **Architectural Classification:** Ingress & Routing
- **Runtime Technology:** Envoy / NGINX / Kong
- **Deployment Context:** Cloud Ingress Tier
- **Associated Data Stores:** `Redis Token Cache`
- **Governing Product Modules:** MODULE-001, MODULE-005

#### Threat Profile & Specific Mitigations:
1. **Threat Category: Spoofing**
   - **Vulnerability Scenario:** Adversary impersonates an authorized staff member or node. targeting `ARCH-CONT-003`.
   - **Architectural Control:** RS256 JWT tokens with hardware-bound certificates, Argon2id MFA, mutual TLS (mTLS) for edge nodes.
   - **Verification Test:** Verify client certificate chain and check JWT signature against JWKS endpoint.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Tampering**
   - **Vulnerability Scenario:** Malicious modification of clinical records, prescriptions, or batch logs. targeting `ARCH-CONT-003`.
   - **Architectural Control:** TLS 1.3 in-flight encryption, AES-256 GCM storage, SHA-256 HMAC digital signatures on sealed encounters.
   - **Verification Test:** Assert checksum matches SHA-256 hash of payload before accepting updates.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Repudiation**
   - **Vulnerability Scenario:** Provider or pharmacist denies performing a critical clinical action. targeting `ARCH-CONT-003`.
   - **Architectural Control:** Cryptographic WORM append-only audit ledger linking every transaction to a verified staff key.
   - **Verification Test:** Query WORM audit chain to verify cryptographic signature and immutable timestamp.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Information Disclosure**
   - **Vulnerability Scenario:** Unauthorized exfiltration of sensitive patient diagnoses, HIV/TB status, or IDs. targeting `ARCH-CONT-003`.
   - **Architectural Control:** Field-level column encryption, strict ABAC clinic scoping, automated PII log scrubber.
   - **Verification Test:** Inspect logs for redacted patterns and verify ciphertext in database dumps.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Denial of Service**
   - **Vulnerability Scenario:** Volumetric DDoS attack or retry storms exhausting edge server memory or cloud APIs. targeting `ARCH-CONT-003`.
   - **Architectural Control:** Redis token-bucket rate limiting, edge offline fallback mode, Cloudflare/Envoy WAF traffic filtering.
   - **Verification Test:** Simulate 5,000 req/min and verify HTTP 429 response without database degradation.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Elevation of Privilege**
   - **Vulnerability Scenario:** Frontline staff member exploits API flaw to gain prescribing or admin rights. targeting `ARCH-CONT-003`.
   - **Architectural Control:** Hardened NestJS RolesGuard, immutable capability claim enforcement, zero-trust token inspection.
   - **Verification Test:** Attempt API call with forged role claim and confirm immediate HTTP 403 Forbidden.
   - **Residual Risk Level:** Low (Controlled)

#### Container Runtime Hardening Directives:
- **Container Security Profile:** Non-root execution (`USER 10001:10001`), read-only rootfs (`readOnlyRootFilesystem: true`).
- **Linux Capability Dropping:** `securityContext.capabilities.drop: ['ALL']`.
- **Network Policy:** Egress restricted to approved service CIDRs; ingress strictly via service mesh.
- **Vulnerability SLA:** Zero Critical/High CVEs allowed in base container image; nightly Trivy rescan.

---

### 02.04 STRIDE Threat Analysis: `ARCH-CONT-004` (Identity & Access Management (IAM) Service)
- **Container Identifier:** `ARCH-CONT-004`
- **Container Title:** Identity & Access Management (IAM) Service
- **Architectural Classification:** Security & Auth
- **Runtime Technology:** Node.js / Passport / Argon2id / JOSE
- **Deployment Context:** Cloud App Tier / Edge Mirror
- **Associated Data Stores:** `PostgreSQL `auth_users``
- **Governing Product Modules:** MODULE-001, MODULE-005

#### Threat Profile & Specific Mitigations:
1. **Threat Category: Spoofing**
   - **Vulnerability Scenario:** Adversary impersonates an authorized staff member or node. targeting `ARCH-CONT-004`.
   - **Architectural Control:** RS256 JWT tokens with hardware-bound certificates, Argon2id MFA, mutual TLS (mTLS) for edge nodes.
   - **Verification Test:** Verify client certificate chain and check JWT signature against JWKS endpoint.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Tampering**
   - **Vulnerability Scenario:** Malicious modification of clinical records, prescriptions, or batch logs. targeting `ARCH-CONT-004`.
   - **Architectural Control:** TLS 1.3 in-flight encryption, AES-256 GCM storage, SHA-256 HMAC digital signatures on sealed encounters.
   - **Verification Test:** Assert checksum matches SHA-256 hash of payload before accepting updates.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Repudiation**
   - **Vulnerability Scenario:** Provider or pharmacist denies performing a critical clinical action. targeting `ARCH-CONT-004`.
   - **Architectural Control:** Cryptographic WORM append-only audit ledger linking every transaction to a verified staff key.
   - **Verification Test:** Query WORM audit chain to verify cryptographic signature and immutable timestamp.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Information Disclosure**
   - **Vulnerability Scenario:** Unauthorized exfiltration of sensitive patient diagnoses, HIV/TB status, or IDs. targeting `ARCH-CONT-004`.
   - **Architectural Control:** Field-level column encryption, strict ABAC clinic scoping, automated PII log scrubber.
   - **Verification Test:** Inspect logs for redacted patterns and verify ciphertext in database dumps.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Denial of Service**
   - **Vulnerability Scenario:** Volumetric DDoS attack or retry storms exhausting edge server memory or cloud APIs. targeting `ARCH-CONT-004`.
   - **Architectural Control:** Redis token-bucket rate limiting, edge offline fallback mode, Cloudflare/Envoy WAF traffic filtering.
   - **Verification Test:** Simulate 5,000 req/min and verify HTTP 429 response without database degradation.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Elevation of Privilege**
   - **Vulnerability Scenario:** Frontline staff member exploits API flaw to gain prescribing or admin rights. targeting `ARCH-CONT-004`.
   - **Architectural Control:** Hardened NestJS RolesGuard, immutable capability claim enforcement, zero-trust token inspection.
   - **Verification Test:** Attempt API call with forged role claim and confirm immediate HTTP 403 Forbidden.
   - **Residual Risk Level:** Low (Controlled)

#### Container Runtime Hardening Directives:
- **Container Security Profile:** Non-root execution (`USER 10001:10001`), read-only rootfs (`readOnlyRootFilesystem: true`).
- **Linux Capability Dropping:** `securityContext.capabilities.drop: ['ALL']`.
- **Network Policy:** Egress restricted to approved service CIDRs; ingress strictly via service mesh.
- **Vulnerability SLA:** Zero Critical/High CVEs allowed in base container image; nightly Trivy rescan.

---

### 02.05 STRIDE Threat Analysis: `ARCH-CONT-005` (Master Patient Index (MPI) Service)
- **Container Identifier:** `ARCH-CONT-005`
- **Container Title:** Master Patient Index (MPI) Service
- **Architectural Classification:** Patient Domain
- **Runtime Technology:** NestJS / Fastify / TypeScript
- **Deployment Context:** Cloud App Tier / Edge Sync
- **Associated Data Stores:** `PostgreSQL `patients``
- **Governing Product Modules:** MODULE-007, MODULE-008

#### Threat Profile & Specific Mitigations:
1. **Threat Category: Spoofing**
   - **Vulnerability Scenario:** Adversary impersonates an authorized staff member or node. targeting `ARCH-CONT-005`.
   - **Architectural Control:** RS256 JWT tokens with hardware-bound certificates, Argon2id MFA, mutual TLS (mTLS) for edge nodes.
   - **Verification Test:** Verify client certificate chain and check JWT signature against JWKS endpoint.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Tampering**
   - **Vulnerability Scenario:** Malicious modification of clinical records, prescriptions, or batch logs. targeting `ARCH-CONT-005`.
   - **Architectural Control:** TLS 1.3 in-flight encryption, AES-256 GCM storage, SHA-256 HMAC digital signatures on sealed encounters.
   - **Verification Test:** Assert checksum matches SHA-256 hash of payload before accepting updates.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Repudiation**
   - **Vulnerability Scenario:** Provider or pharmacist denies performing a critical clinical action. targeting `ARCH-CONT-005`.
   - **Architectural Control:** Cryptographic WORM append-only audit ledger linking every transaction to a verified staff key.
   - **Verification Test:** Query WORM audit chain to verify cryptographic signature and immutable timestamp.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Information Disclosure**
   - **Vulnerability Scenario:** Unauthorized exfiltration of sensitive patient diagnoses, HIV/TB status, or IDs. targeting `ARCH-CONT-005`.
   - **Architectural Control:** Field-level column encryption, strict ABAC clinic scoping, automated PII log scrubber.
   - **Verification Test:** Inspect logs for redacted patterns and verify ciphertext in database dumps.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Denial of Service**
   - **Vulnerability Scenario:** Volumetric DDoS attack or retry storms exhausting edge server memory or cloud APIs. targeting `ARCH-CONT-005`.
   - **Architectural Control:** Redis token-bucket rate limiting, edge offline fallback mode, Cloudflare/Envoy WAF traffic filtering.
   - **Verification Test:** Simulate 5,000 req/min and verify HTTP 429 response without database degradation.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Elevation of Privilege**
   - **Vulnerability Scenario:** Frontline staff member exploits API flaw to gain prescribing or admin rights. targeting `ARCH-CONT-005`.
   - **Architectural Control:** Hardened NestJS RolesGuard, immutable capability claim enforcement, zero-trust token inspection.
   - **Verification Test:** Attempt API call with forged role claim and confirm immediate HTTP 403 Forbidden.
   - **Residual Risk Level:** Low (Controlled)

#### Container Runtime Hardening Directives:
- **Container Security Profile:** Non-root execution (`USER 10001:10001`), read-only rootfs (`readOnlyRootFilesystem: true`).
- **Linux Capability Dropping:** `securityContext.capabilities.drop: ['ALL']`.
- **Network Policy:** Egress restricted to approved service CIDRs; ingress strictly via service mesh.
- **Vulnerability SLA:** Zero Critical/High CVEs allowed in base container image; nightly Trivy rescan.

---

### 02.06 STRIDE Threat Analysis: `ARCH-CONT-006` (Queue Orchestration & Triage Engine)
- **Container Identifier:** `ARCH-CONT-006`
- **Container Title:** Queue Orchestration & Triage Engine
- **Architectural Classification:** Workflow Domain
- **Runtime Technology:** Go / MQTT / WebSockets
- **Deployment Context:** Edge Mini-Server / Cloud Sync
- **Associated Data Stores:** `Edge SQLite `clinic_queues``
- **Governing Product Modules:** MODULE-009, MODULE-010, MODULE-011

#### Threat Profile & Specific Mitigations:
1. **Threat Category: Spoofing**
   - **Vulnerability Scenario:** Adversary impersonates an authorized staff member or node. targeting `ARCH-CONT-006`.
   - **Architectural Control:** RS256 JWT tokens with hardware-bound certificates, Argon2id MFA, mutual TLS (mTLS) for edge nodes.
   - **Verification Test:** Verify client certificate chain and check JWT signature against JWKS endpoint.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Tampering**
   - **Vulnerability Scenario:** Malicious modification of clinical records, prescriptions, or batch logs. targeting `ARCH-CONT-006`.
   - **Architectural Control:** TLS 1.3 in-flight encryption, AES-256 GCM storage, SHA-256 HMAC digital signatures on sealed encounters.
   - **Verification Test:** Assert checksum matches SHA-256 hash of payload before accepting updates.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Repudiation**
   - **Vulnerability Scenario:** Provider or pharmacist denies performing a critical clinical action. targeting `ARCH-CONT-006`.
   - **Architectural Control:** Cryptographic WORM append-only audit ledger linking every transaction to a verified staff key.
   - **Verification Test:** Query WORM audit chain to verify cryptographic signature and immutable timestamp.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Information Disclosure**
   - **Vulnerability Scenario:** Unauthorized exfiltration of sensitive patient diagnoses, HIV/TB status, or IDs. targeting `ARCH-CONT-006`.
   - **Architectural Control:** Field-level column encryption, strict ABAC clinic scoping, automated PII log scrubber.
   - **Verification Test:** Inspect logs for redacted patterns and verify ciphertext in database dumps.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Denial of Service**
   - **Vulnerability Scenario:** Volumetric DDoS attack or retry storms exhausting edge server memory or cloud APIs. targeting `ARCH-CONT-006`.
   - **Architectural Control:** Redis token-bucket rate limiting, edge offline fallback mode, Cloudflare/Envoy WAF traffic filtering.
   - **Verification Test:** Simulate 5,000 req/min and verify HTTP 429 response without database degradation.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Elevation of Privilege**
   - **Vulnerability Scenario:** Frontline staff member exploits API flaw to gain prescribing or admin rights. targeting `ARCH-CONT-006`.
   - **Architectural Control:** Hardened NestJS RolesGuard, immutable capability claim enforcement, zero-trust token inspection.
   - **Verification Test:** Attempt API call with forged role claim and confirm immediate HTTP 403 Forbidden.
   - **Residual Risk Level:** Low (Controlled)

#### Container Runtime Hardening Directives:
- **Container Security Profile:** Non-root execution (`USER 10001:10001`), read-only rootfs (`readOnlyRootFilesystem: true`).
- **Linux Capability Dropping:** `securityContext.capabilities.drop: ['ALL']`.
- **Network Policy:** Egress restricted to approved service CIDRs; ingress strictly via service mesh.
- **Vulnerability SLA:** Zero Critical/High CVEs allowed in base container image; nightly Trivy rescan.

---

### 02.07 STRIDE Threat Analysis: `ARCH-CONT-007` (Clinical Consultation & EMR Service)
- **Container Identifier:** `ARCH-CONT-007`
- **Container Title:** Clinical Consultation & EMR Service
- **Architectural Classification:** Clinical Domain
- **Runtime Technology:** NestJS / Prisma / TypeScript
- **Deployment Context:** Cloud App Tier / Edge Sync
- **Associated Data Stores:** `PostgreSQL `clinical_encounters``
- **Governing Product Modules:** MODULE-013, MODULE-014

#### Threat Profile & Specific Mitigations:
1. **Threat Category: Spoofing**
   - **Vulnerability Scenario:** Adversary impersonates an authorized staff member or node. targeting `ARCH-CONT-007`.
   - **Architectural Control:** RS256 JWT tokens with hardware-bound certificates, Argon2id MFA, mutual TLS (mTLS) for edge nodes.
   - **Verification Test:** Verify client certificate chain and check JWT signature against JWKS endpoint.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Tampering**
   - **Vulnerability Scenario:** Malicious modification of clinical records, prescriptions, or batch logs. targeting `ARCH-CONT-007`.
   - **Architectural Control:** TLS 1.3 in-flight encryption, AES-256 GCM storage, SHA-256 HMAC digital signatures on sealed encounters.
   - **Verification Test:** Assert checksum matches SHA-256 hash of payload before accepting updates.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Repudiation**
   - **Vulnerability Scenario:** Provider or pharmacist denies performing a critical clinical action. targeting `ARCH-CONT-007`.
   - **Architectural Control:** Cryptographic WORM append-only audit ledger linking every transaction to a verified staff key.
   - **Verification Test:** Query WORM audit chain to verify cryptographic signature and immutable timestamp.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Information Disclosure**
   - **Vulnerability Scenario:** Unauthorized exfiltration of sensitive patient diagnoses, HIV/TB status, or IDs. targeting `ARCH-CONT-007`.
   - **Architectural Control:** Field-level column encryption, strict ABAC clinic scoping, automated PII log scrubber.
   - **Verification Test:** Inspect logs for redacted patterns and verify ciphertext in database dumps.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Denial of Service**
   - **Vulnerability Scenario:** Volumetric DDoS attack or retry storms exhausting edge server memory or cloud APIs. targeting `ARCH-CONT-007`.
   - **Architectural Control:** Redis token-bucket rate limiting, edge offline fallback mode, Cloudflare/Envoy WAF traffic filtering.
   - **Verification Test:** Simulate 5,000 req/min and verify HTTP 429 response without database degradation.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Elevation of Privilege**
   - **Vulnerability Scenario:** Frontline staff member exploits API flaw to gain prescribing or admin rights. targeting `ARCH-CONT-007`.
   - **Architectural Control:** Hardened NestJS RolesGuard, immutable capability claim enforcement, zero-trust token inspection.
   - **Verification Test:** Attempt API call with forged role claim and confirm immediate HTTP 403 Forbidden.
   - **Residual Risk Level:** Low (Controlled)

#### Container Runtime Hardening Directives:
- **Container Security Profile:** Non-root execution (`USER 10001:10001`), read-only rootfs (`readOnlyRootFilesystem: true`).
- **Linux Capability Dropping:** `securityContext.capabilities.drop: ['ALL']`.
- **Network Policy:** Egress restricted to approved service CIDRs; ingress strictly via service mesh.
- **Vulnerability SLA:** Zero Critical/High CVEs allowed in base container image; nightly Trivy rescan.

---

### 02.08 STRIDE Threat Analysis: `ARCH-CONT-008` (Electronic Prescription & CDSS Service)
- **Container Identifier:** `ARCH-CONT-008`
- **Container Title:** Electronic Prescription & CDSS Service
- **Architectural Classification:** Clinical Domain
- **Runtime Technology:** NestJS / Rule Engine / TypeScript
- **Deployment Context:** Cloud App Tier / Edge Sync
- **Associated Data Stores:** `PostgreSQL `prescriptions``
- **Governing Product Modules:** MODULE-014, MODULE-015

#### Threat Profile & Specific Mitigations:
1. **Threat Category: Spoofing**
   - **Vulnerability Scenario:** Adversary impersonates an authorized staff member or node. targeting `ARCH-CONT-008`.
   - **Architectural Control:** RS256 JWT tokens with hardware-bound certificates, Argon2id MFA, mutual TLS (mTLS) for edge nodes.
   - **Verification Test:** Verify client certificate chain and check JWT signature against JWKS endpoint.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Tampering**
   - **Vulnerability Scenario:** Malicious modification of clinical records, prescriptions, or batch logs. targeting `ARCH-CONT-008`.
   - **Architectural Control:** TLS 1.3 in-flight encryption, AES-256 GCM storage, SHA-256 HMAC digital signatures on sealed encounters.
   - **Verification Test:** Assert checksum matches SHA-256 hash of payload before accepting updates.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Repudiation**
   - **Vulnerability Scenario:** Provider or pharmacist denies performing a critical clinical action. targeting `ARCH-CONT-008`.
   - **Architectural Control:** Cryptographic WORM append-only audit ledger linking every transaction to a verified staff key.
   - **Verification Test:** Query WORM audit chain to verify cryptographic signature and immutable timestamp.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Information Disclosure**
   - **Vulnerability Scenario:** Unauthorized exfiltration of sensitive patient diagnoses, HIV/TB status, or IDs. targeting `ARCH-CONT-008`.
   - **Architectural Control:** Field-level column encryption, strict ABAC clinic scoping, automated PII log scrubber.
   - **Verification Test:** Inspect logs for redacted patterns and verify ciphertext in database dumps.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Denial of Service**
   - **Vulnerability Scenario:** Volumetric DDoS attack or retry storms exhausting edge server memory or cloud APIs. targeting `ARCH-CONT-008`.
   - **Architectural Control:** Redis token-bucket rate limiting, edge offline fallback mode, Cloudflare/Envoy WAF traffic filtering.
   - **Verification Test:** Simulate 5,000 req/min and verify HTTP 429 response without database degradation.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Elevation of Privilege**
   - **Vulnerability Scenario:** Frontline staff member exploits API flaw to gain prescribing or admin rights. targeting `ARCH-CONT-008`.
   - **Architectural Control:** Hardened NestJS RolesGuard, immutable capability claim enforcement, zero-trust token inspection.
   - **Verification Test:** Attempt API call with forged role claim and confirm immediate HTTP 403 Forbidden.
   - **Residual Risk Level:** Low (Controlled)

#### Container Runtime Hardening Directives:
- **Container Security Profile:** Non-root execution (`USER 10001:10001`), read-only rootfs (`readOnlyRootFilesystem: true`).
- **Linux Capability Dropping:** `securityContext.capabilities.drop: ['ALL']`.
- **Network Policy:** Egress restricted to approved service CIDRs; ingress strictly via service mesh.
- **Vulnerability SLA:** Zero Critical/High CVEs allowed in base container image; nightly Trivy rescan.

---

### 02.09 STRIDE Threat Analysis: `ARCH-CONT-009` (Pharmacy Inventory & Dispensation Service)
- **Container Identifier:** `ARCH-CONT-009`
- **Container Title:** Pharmacy Inventory & Dispensation Service
- **Architectural Classification:** Logistics Domain
- **Runtime Technology:** NestJS / TypeScript
- **Deployment Context:** Cloud App Tier / Edge Sync
- **Associated Data Stores:** `PostgreSQL `pharmacy_batches``
- **Governing Product Modules:** MODULE-019..022

#### Threat Profile & Specific Mitigations:
1. **Threat Category: Spoofing**
   - **Vulnerability Scenario:** Adversary impersonates an authorized staff member or node. targeting `ARCH-CONT-009`.
   - **Architectural Control:** RS256 JWT tokens with hardware-bound certificates, Argon2id MFA, mutual TLS (mTLS) for edge nodes.
   - **Verification Test:** Verify client certificate chain and check JWT signature against JWKS endpoint.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Tampering**
   - **Vulnerability Scenario:** Malicious modification of clinical records, prescriptions, or batch logs. targeting `ARCH-CONT-009`.
   - **Architectural Control:** TLS 1.3 in-flight encryption, AES-256 GCM storage, SHA-256 HMAC digital signatures on sealed encounters.
   - **Verification Test:** Assert checksum matches SHA-256 hash of payload before accepting updates.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Repudiation**
   - **Vulnerability Scenario:** Provider or pharmacist denies performing a critical clinical action. targeting `ARCH-CONT-009`.
   - **Architectural Control:** Cryptographic WORM append-only audit ledger linking every transaction to a verified staff key.
   - **Verification Test:** Query WORM audit chain to verify cryptographic signature and immutable timestamp.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Information Disclosure**
   - **Vulnerability Scenario:** Unauthorized exfiltration of sensitive patient diagnoses, HIV/TB status, or IDs. targeting `ARCH-CONT-009`.
   - **Architectural Control:** Field-level column encryption, strict ABAC clinic scoping, automated PII log scrubber.
   - **Verification Test:** Inspect logs for redacted patterns and verify ciphertext in database dumps.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Denial of Service**
   - **Vulnerability Scenario:** Volumetric DDoS attack or retry storms exhausting edge server memory or cloud APIs. targeting `ARCH-CONT-009`.
   - **Architectural Control:** Redis token-bucket rate limiting, edge offline fallback mode, Cloudflare/Envoy WAF traffic filtering.
   - **Verification Test:** Simulate 5,000 req/min and verify HTTP 429 response without database degradation.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Elevation of Privilege**
   - **Vulnerability Scenario:** Frontline staff member exploits API flaw to gain prescribing or admin rights. targeting `ARCH-CONT-009`.
   - **Architectural Control:** Hardened NestJS RolesGuard, immutable capability claim enforcement, zero-trust token inspection.
   - **Verification Test:** Attempt API call with forged role claim and confirm immediate HTTP 403 Forbidden.
   - **Residual Risk Level:** Low (Controlled)

#### Container Runtime Hardening Directives:
- **Container Security Profile:** Non-root execution (`USER 10001:10001`), read-only rootfs (`readOnlyRootFilesystem: true`).
- **Linux Capability Dropping:** `securityContext.capabilities.drop: ['ALL']`.
- **Network Policy:** Egress restricted to approved service CIDRs; ingress strictly via service mesh.
- **Vulnerability SLA:** Zero Critical/High CVEs allowed in base container image; nightly Trivy rescan.

---

### 02.10 STRIDE Threat Analysis: `ARCH-CONT-010` (Diagnostic Laboratory Service)
- **Container Identifier:** `ARCH-CONT-010`
- **Container Title:** Diagnostic Laboratory Service
- **Architectural Classification:** Diagnostics Domain
- **Runtime Technology:** NestJS / TypeScript
- **Deployment Context:** Cloud App Tier / Edge Sync
- **Associated Data Stores:** `PostgreSQL `lab_orders``
- **Governing Product Modules:** MODULE-016

#### Threat Profile & Specific Mitigations:
1. **Threat Category: Spoofing**
   - **Vulnerability Scenario:** Adversary impersonates an authorized staff member or node. targeting `ARCH-CONT-010`.
   - **Architectural Control:** RS256 JWT tokens with hardware-bound certificates, Argon2id MFA, mutual TLS (mTLS) for edge nodes.
   - **Verification Test:** Verify client certificate chain and check JWT signature against JWKS endpoint.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Tampering**
   - **Vulnerability Scenario:** Malicious modification of clinical records, prescriptions, or batch logs. targeting `ARCH-CONT-010`.
   - **Architectural Control:** TLS 1.3 in-flight encryption, AES-256 GCM storage, SHA-256 HMAC digital signatures on sealed encounters.
   - **Verification Test:** Assert checksum matches SHA-256 hash of payload before accepting updates.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Repudiation**
   - **Vulnerability Scenario:** Provider or pharmacist denies performing a critical clinical action. targeting `ARCH-CONT-010`.
   - **Architectural Control:** Cryptographic WORM append-only audit ledger linking every transaction to a verified staff key.
   - **Verification Test:** Query WORM audit chain to verify cryptographic signature and immutable timestamp.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Information Disclosure**
   - **Vulnerability Scenario:** Unauthorized exfiltration of sensitive patient diagnoses, HIV/TB status, or IDs. targeting `ARCH-CONT-010`.
   - **Architectural Control:** Field-level column encryption, strict ABAC clinic scoping, automated PII log scrubber.
   - **Verification Test:** Inspect logs for redacted patterns and verify ciphertext in database dumps.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Denial of Service**
   - **Vulnerability Scenario:** Volumetric DDoS attack or retry storms exhausting edge server memory or cloud APIs. targeting `ARCH-CONT-010`.
   - **Architectural Control:** Redis token-bucket rate limiting, edge offline fallback mode, Cloudflare/Envoy WAF traffic filtering.
   - **Verification Test:** Simulate 5,000 req/min and verify HTTP 429 response without database degradation.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Elevation of Privilege**
   - **Vulnerability Scenario:** Frontline staff member exploits API flaw to gain prescribing or admin rights. targeting `ARCH-CONT-010`.
   - **Architectural Control:** Hardened NestJS RolesGuard, immutable capability claim enforcement, zero-trust token inspection.
   - **Verification Test:** Attempt API call with forged role claim and confirm immediate HTTP 403 Forbidden.
   - **Residual Risk Level:** Low (Controlled)

#### Container Runtime Hardening Directives:
- **Container Security Profile:** Non-root execution (`USER 10001:10001`), read-only rootfs (`readOnlyRootFilesystem: true`).
- **Linux Capability Dropping:** `securityContext.capabilities.drop: ['ALL']`.
- **Network Policy:** Egress restricted to approved service CIDRs; ingress strictly via service mesh.
- **Vulnerability SLA:** Zero Critical/High CVEs allowed in base container image; nightly Trivy rescan.

---

### 02.11 STRIDE Threat Analysis: `ARCH-CONT-011` (Referral & EMS Telemetry Bridge)
- **Container Identifier:** `ARCH-CONT-011`
- **Container Title:** Referral & EMS Telemetry Bridge
- **Architectural Classification:** Care Continuity
- **Runtime Technology:** NestJS / REST Gateway
- **Deployment Context:** Cloud App Tier
- **Associated Data Stores:** `PostgreSQL `referrals``
- **Governing Product Modules:** MODULE-017

#### Threat Profile & Specific Mitigations:
1. **Threat Category: Spoofing**
   - **Vulnerability Scenario:** Adversary impersonates an authorized staff member or node. targeting `ARCH-CONT-011`.
   - **Architectural Control:** RS256 JWT tokens with hardware-bound certificates, Argon2id MFA, mutual TLS (mTLS) for edge nodes.
   - **Verification Test:** Verify client certificate chain and check JWT signature against JWKS endpoint.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Tampering**
   - **Vulnerability Scenario:** Malicious modification of clinical records, prescriptions, or batch logs. targeting `ARCH-CONT-011`.
   - **Architectural Control:** TLS 1.3 in-flight encryption, AES-256 GCM storage, SHA-256 HMAC digital signatures on sealed encounters.
   - **Verification Test:** Assert checksum matches SHA-256 hash of payload before accepting updates.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Repudiation**
   - **Vulnerability Scenario:** Provider or pharmacist denies performing a critical clinical action. targeting `ARCH-CONT-011`.
   - **Architectural Control:** Cryptographic WORM append-only audit ledger linking every transaction to a verified staff key.
   - **Verification Test:** Query WORM audit chain to verify cryptographic signature and immutable timestamp.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Information Disclosure**
   - **Vulnerability Scenario:** Unauthorized exfiltration of sensitive patient diagnoses, HIV/TB status, or IDs. targeting `ARCH-CONT-011`.
   - **Architectural Control:** Field-level column encryption, strict ABAC clinic scoping, automated PII log scrubber.
   - **Verification Test:** Inspect logs for redacted patterns and verify ciphertext in database dumps.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Denial of Service**
   - **Vulnerability Scenario:** Volumetric DDoS attack or retry storms exhausting edge server memory or cloud APIs. targeting `ARCH-CONT-011`.
   - **Architectural Control:** Redis token-bucket rate limiting, edge offline fallback mode, Cloudflare/Envoy WAF traffic filtering.
   - **Verification Test:** Simulate 5,000 req/min and verify HTTP 429 response without database degradation.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Elevation of Privilege**
   - **Vulnerability Scenario:** Frontline staff member exploits API flaw to gain prescribing or admin rights. targeting `ARCH-CONT-011`.
   - **Architectural Control:** Hardened NestJS RolesGuard, immutable capability claim enforcement, zero-trust token inspection.
   - **Verification Test:** Attempt API call with forged role claim and confirm immediate HTTP 403 Forbidden.
   - **Residual Risk Level:** Low (Controlled)

#### Container Runtime Hardening Directives:
- **Container Security Profile:** Non-root execution (`USER 10001:10001`), read-only rootfs (`readOnlyRootFilesystem: true`).
- **Linux Capability Dropping:** `securityContext.capabilities.drop: ['ALL']`.
- **Network Policy:** Egress restricted to approved service CIDRs; ingress strictly via service mesh.
- **Vulnerability SLA:** Zero Critical/High CVEs allowed in base container image; nightly Trivy rescan.

---

### 02.12 STRIDE Threat Analysis: `ARCH-CONT-012` (Citizen Portal & Multilingual Notification Service)
- **Container Identifier:** `ARCH-CONT-012`
- **Container Title:** Citizen Portal & Multilingual Notification Service
- **Architectural Classification:** Citizen Domain
- **Runtime Technology:** Node.js / BullMQ / Redis
- **Deployment Context:** Cloud App Tier
- **Associated Data Stores:** `Redis Queue / PostgreSQL`
- **Governing Product Modules:** MODULE-023, MODULE-024

#### Threat Profile & Specific Mitigations:
1. **Threat Category: Spoofing**
   - **Vulnerability Scenario:** Adversary impersonates an authorized staff member or node. targeting `ARCH-CONT-012`.
   - **Architectural Control:** RS256 JWT tokens with hardware-bound certificates, Argon2id MFA, mutual TLS (mTLS) for edge nodes.
   - **Verification Test:** Verify client certificate chain and check JWT signature against JWKS endpoint.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Tampering**
   - **Vulnerability Scenario:** Malicious modification of clinical records, prescriptions, or batch logs. targeting `ARCH-CONT-012`.
   - **Architectural Control:** TLS 1.3 in-flight encryption, AES-256 GCM storage, SHA-256 HMAC digital signatures on sealed encounters.
   - **Verification Test:** Assert checksum matches SHA-256 hash of payload before accepting updates.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Repudiation**
   - **Vulnerability Scenario:** Provider or pharmacist denies performing a critical clinical action. targeting `ARCH-CONT-012`.
   - **Architectural Control:** Cryptographic WORM append-only audit ledger linking every transaction to a verified staff key.
   - **Verification Test:** Query WORM audit chain to verify cryptographic signature and immutable timestamp.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Information Disclosure**
   - **Vulnerability Scenario:** Unauthorized exfiltration of sensitive patient diagnoses, HIV/TB status, or IDs. targeting `ARCH-CONT-012`.
   - **Architectural Control:** Field-level column encryption, strict ABAC clinic scoping, automated PII log scrubber.
   - **Verification Test:** Inspect logs for redacted patterns and verify ciphertext in database dumps.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Denial of Service**
   - **Vulnerability Scenario:** Volumetric DDoS attack or retry storms exhausting edge server memory or cloud APIs. targeting `ARCH-CONT-012`.
   - **Architectural Control:** Redis token-bucket rate limiting, edge offline fallback mode, Cloudflare/Envoy WAF traffic filtering.
   - **Verification Test:** Simulate 5,000 req/min and verify HTTP 429 response without database degradation.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Elevation of Privilege**
   - **Vulnerability Scenario:** Frontline staff member exploits API flaw to gain prescribing or admin rights. targeting `ARCH-CONT-012`.
   - **Architectural Control:** Hardened NestJS RolesGuard, immutable capability claim enforcement, zero-trust token inspection.
   - **Verification Test:** Attempt API call with forged role claim and confirm immediate HTTP 403 Forbidden.
   - **Residual Risk Level:** Low (Controlled)

#### Container Runtime Hardening Directives:
- **Container Security Profile:** Non-root execution (`USER 10001:10001`), read-only rootfs (`readOnlyRootFilesystem: true`).
- **Linux Capability Dropping:** `securityContext.capabilities.drop: ['ALL']`.
- **Network Policy:** Egress restricted to approved service CIDRs; ingress strictly via service mesh.
- **Vulnerability SLA:** Zero Critical/High CVEs allowed in base container image; nightly Trivy rescan.

---

### 02.13 STRIDE Threat Analysis: `ARCH-CONT-013` (Bi-directional Edge-Cloud Synchronization Service)
- **Container Identifier:** `ARCH-CONT-013`
- **Container Title:** Bi-directional Edge-Cloud Synchronization Service
- **Architectural Classification:** Sync Engine
- **Runtime Technology:** Go / gRPC / Vector Clocks
- **Deployment Context:** Edge Node & Cloud Worker
- **Associated Data Stores:** `SQLite Mutation Log`
- **Governing Product Modules:** MODULE-028

#### Threat Profile & Specific Mitigations:
1. **Threat Category: Spoofing**
   - **Vulnerability Scenario:** Adversary impersonates an authorized staff member or node. targeting `ARCH-CONT-013`.
   - **Architectural Control:** RS256 JWT tokens with hardware-bound certificates, Argon2id MFA, mutual TLS (mTLS) for edge nodes.
   - **Verification Test:** Verify client certificate chain and check JWT signature against JWKS endpoint.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Tampering**
   - **Vulnerability Scenario:** Malicious modification of clinical records, prescriptions, or batch logs. targeting `ARCH-CONT-013`.
   - **Architectural Control:** TLS 1.3 in-flight encryption, AES-256 GCM storage, SHA-256 HMAC digital signatures on sealed encounters.
   - **Verification Test:** Assert checksum matches SHA-256 hash of payload before accepting updates.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Repudiation**
   - **Vulnerability Scenario:** Provider or pharmacist denies performing a critical clinical action. targeting `ARCH-CONT-013`.
   - **Architectural Control:** Cryptographic WORM append-only audit ledger linking every transaction to a verified staff key.
   - **Verification Test:** Query WORM audit chain to verify cryptographic signature and immutable timestamp.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Information Disclosure**
   - **Vulnerability Scenario:** Unauthorized exfiltration of sensitive patient diagnoses, HIV/TB status, or IDs. targeting `ARCH-CONT-013`.
   - **Architectural Control:** Field-level column encryption, strict ABAC clinic scoping, automated PII log scrubber.
   - **Verification Test:** Inspect logs for redacted patterns and verify ciphertext in database dumps.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Denial of Service**
   - **Vulnerability Scenario:** Volumetric DDoS attack or retry storms exhausting edge server memory or cloud APIs. targeting `ARCH-CONT-013`.
   - **Architectural Control:** Redis token-bucket rate limiting, edge offline fallback mode, Cloudflare/Envoy WAF traffic filtering.
   - **Verification Test:** Simulate 5,000 req/min and verify HTTP 429 response without database degradation.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Elevation of Privilege**
   - **Vulnerability Scenario:** Frontline staff member exploits API flaw to gain prescribing or admin rights. targeting `ARCH-CONT-013`.
   - **Architectural Control:** Hardened NestJS RolesGuard, immutable capability claim enforcement, zero-trust token inspection.
   - **Verification Test:** Attempt API call with forged role claim and confirm immediate HTTP 403 Forbidden.
   - **Residual Risk Level:** Low (Controlled)

#### Container Runtime Hardening Directives:
- **Container Security Profile:** Non-root execution (`USER 10001:10001`), read-only rootfs (`readOnlyRootFilesystem: true`).
- **Linux Capability Dropping:** `securityContext.capabilities.drop: ['ALL']`.
- **Network Policy:** Egress restricted to approved service CIDRs; ingress strictly via service mesh.
- **Vulnerability SLA:** Zero Critical/High CVEs allowed in base container image; nightly Trivy rescan.

---

### 02.14 STRIDE Threat Analysis: `ARCH-CONT-014` (ABDM & National Health Grid Bridge)
- **Container Identifier:** `ARCH-CONT-014`
- **Container Title:** ABDM & National Health Grid Bridge
- **Architectural Classification:** Interoperability
- **Runtime Technology:** Java / Spring Boot / HAPI FHIR
- **Deployment Context:** Cloud DMZ Tier
- **Associated Data Stores:** `PostgreSQL `abdm_artifacts``
- **Governing Product Modules:** MODULE-029

#### Threat Profile & Specific Mitigations:
1. **Threat Category: Spoofing**
   - **Vulnerability Scenario:** Adversary impersonates an authorized staff member or node. targeting `ARCH-CONT-014`.
   - **Architectural Control:** RS256 JWT tokens with hardware-bound certificates, Argon2id MFA, mutual TLS (mTLS) for edge nodes.
   - **Verification Test:** Verify client certificate chain and check JWT signature against JWKS endpoint.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Tampering**
   - **Vulnerability Scenario:** Malicious modification of clinical records, prescriptions, or batch logs. targeting `ARCH-CONT-014`.
   - **Architectural Control:** TLS 1.3 in-flight encryption, AES-256 GCM storage, SHA-256 HMAC digital signatures on sealed encounters.
   - **Verification Test:** Assert checksum matches SHA-256 hash of payload before accepting updates.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Repudiation**
   - **Vulnerability Scenario:** Provider or pharmacist denies performing a critical clinical action. targeting `ARCH-CONT-014`.
   - **Architectural Control:** Cryptographic WORM append-only audit ledger linking every transaction to a verified staff key.
   - **Verification Test:** Query WORM audit chain to verify cryptographic signature and immutable timestamp.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Information Disclosure**
   - **Vulnerability Scenario:** Unauthorized exfiltration of sensitive patient diagnoses, HIV/TB status, or IDs. targeting `ARCH-CONT-014`.
   - **Architectural Control:** Field-level column encryption, strict ABAC clinic scoping, automated PII log scrubber.
   - **Verification Test:** Inspect logs for redacted patterns and verify ciphertext in database dumps.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Denial of Service**
   - **Vulnerability Scenario:** Volumetric DDoS attack or retry storms exhausting edge server memory or cloud APIs. targeting `ARCH-CONT-014`.
   - **Architectural Control:** Redis token-bucket rate limiting, edge offline fallback mode, Cloudflare/Envoy WAF traffic filtering.
   - **Verification Test:** Simulate 5,000 req/min and verify HTTP 429 response without database degradation.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Elevation of Privilege**
   - **Vulnerability Scenario:** Frontline staff member exploits API flaw to gain prescribing or admin rights. targeting `ARCH-CONT-014`.
   - **Architectural Control:** Hardened NestJS RolesGuard, immutable capability claim enforcement, zero-trust token inspection.
   - **Verification Test:** Attempt API call with forged role claim and confirm immediate HTTP 403 Forbidden.
   - **Residual Risk Level:** Low (Controlled)

#### Container Runtime Hardening Directives:
- **Container Security Profile:** Non-root execution (`USER 10001:10001`), read-only rootfs (`readOnlyRootFilesystem: true`).
- **Linux Capability Dropping:** `securityContext.capabilities.drop: ['ALL']`.
- **Network Policy:** Egress restricted to approved service CIDRs; ingress strictly via service mesh.
- **Vulnerability SLA:** Zero Critical/High CVEs allowed in base container image; nightly Trivy rescan.

---

### 02.15 STRIDE Threat Analysis: `ARCH-CONT-015` (Public Health Analytics & Syndromic BI Service)
- **Container Identifier:** `ARCH-CONT-015`
- **Container Title:** Public Health Analytics & Syndromic BI Service
- **Architectural Classification:** Analytics Domain
- **Runtime Technology:** Python / ClickHouse / Apache Superset
- **Deployment Context:** Cloud Analytics Tier
- **Associated Data Stores:** `ClickHouse Star Schema`
- **Governing Product Modules:** MODULE-030

#### Threat Profile & Specific Mitigations:
1. **Threat Category: Spoofing**
   - **Vulnerability Scenario:** Adversary impersonates an authorized staff member or node. targeting `ARCH-CONT-015`.
   - **Architectural Control:** RS256 JWT tokens with hardware-bound certificates, Argon2id MFA, mutual TLS (mTLS) for edge nodes.
   - **Verification Test:** Verify client certificate chain and check JWT signature against JWKS endpoint.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Tampering**
   - **Vulnerability Scenario:** Malicious modification of clinical records, prescriptions, or batch logs. targeting `ARCH-CONT-015`.
   - **Architectural Control:** TLS 1.3 in-flight encryption, AES-256 GCM storage, SHA-256 HMAC digital signatures on sealed encounters.
   - **Verification Test:** Assert checksum matches SHA-256 hash of payload before accepting updates.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Repudiation**
   - **Vulnerability Scenario:** Provider or pharmacist denies performing a critical clinical action. targeting `ARCH-CONT-015`.
   - **Architectural Control:** Cryptographic WORM append-only audit ledger linking every transaction to a verified staff key.
   - **Verification Test:** Query WORM audit chain to verify cryptographic signature and immutable timestamp.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Information Disclosure**
   - **Vulnerability Scenario:** Unauthorized exfiltration of sensitive patient diagnoses, HIV/TB status, or IDs. targeting `ARCH-CONT-015`.
   - **Architectural Control:** Field-level column encryption, strict ABAC clinic scoping, automated PII log scrubber.
   - **Verification Test:** Inspect logs for redacted patterns and verify ciphertext in database dumps.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Denial of Service**
   - **Vulnerability Scenario:** Volumetric DDoS attack or retry storms exhausting edge server memory or cloud APIs. targeting `ARCH-CONT-015`.
   - **Architectural Control:** Redis token-bucket rate limiting, edge offline fallback mode, Cloudflare/Envoy WAF traffic filtering.
   - **Verification Test:** Simulate 5,000 req/min and verify HTTP 429 response without database degradation.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Elevation of Privilege**
   - **Vulnerability Scenario:** Frontline staff member exploits API flaw to gain prescribing or admin rights. targeting `ARCH-CONT-015`.
   - **Architectural Control:** Hardened NestJS RolesGuard, immutable capability claim enforcement, zero-trust token inspection.
   - **Verification Test:** Attempt API call with forged role claim and confirm immediate HTTP 403 Forbidden.
   - **Residual Risk Level:** Low (Controlled)

#### Container Runtime Hardening Directives:
- **Container Security Profile:** Non-root execution (`USER 10001:10001`), read-only rootfs (`readOnlyRootFilesystem: true`).
- **Linux Capability Dropping:** `securityContext.capabilities.drop: ['ALL']`.
- **Network Policy:** Egress restricted to approved service CIDRs; ingress strictly via service mesh.
- **Vulnerability SLA:** Zero Critical/High CVEs allowed in base container image; nightly Trivy rescan.

---

### 02.16 STRIDE Threat Analysis: `ARCH-CONT-016` (Advisory Clinical AI Decision Support Engine)
- **Container Identifier:** `ARCH-CONT-016`
- **Container Title:** Advisory Clinical AI Decision Support Engine
- **Architectural Classification:** AI / ML Tier
- **Runtime Technology:** Python / FastAPI / ONNX Runtime
- **Deployment Context:** Cloud Analytics Tier
- **Associated Data Stores:** `Model Registry (MLflow)`
- **Governing Product Modules:** MODULE-015, MODULE-030

#### Threat Profile & Specific Mitigations:
1. **Threat Category: Spoofing**
   - **Vulnerability Scenario:** Adversary impersonates an authorized staff member or node. targeting `ARCH-CONT-016`.
   - **Architectural Control:** RS256 JWT tokens with hardware-bound certificates, Argon2id MFA, mutual TLS (mTLS) for edge nodes.
   - **Verification Test:** Verify client certificate chain and check JWT signature against JWKS endpoint.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Tampering**
   - **Vulnerability Scenario:** Malicious modification of clinical records, prescriptions, or batch logs. targeting `ARCH-CONT-016`.
   - **Architectural Control:** TLS 1.3 in-flight encryption, AES-256 GCM storage, SHA-256 HMAC digital signatures on sealed encounters.
   - **Verification Test:** Assert checksum matches SHA-256 hash of payload before accepting updates.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Repudiation**
   - **Vulnerability Scenario:** Provider or pharmacist denies performing a critical clinical action. targeting `ARCH-CONT-016`.
   - **Architectural Control:** Cryptographic WORM append-only audit ledger linking every transaction to a verified staff key.
   - **Verification Test:** Query WORM audit chain to verify cryptographic signature and immutable timestamp.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Information Disclosure**
   - **Vulnerability Scenario:** Unauthorized exfiltration of sensitive patient diagnoses, HIV/TB status, or IDs. targeting `ARCH-CONT-016`.
   - **Architectural Control:** Field-level column encryption, strict ABAC clinic scoping, automated PII log scrubber.
   - **Verification Test:** Inspect logs for redacted patterns and verify ciphertext in database dumps.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Denial of Service**
   - **Vulnerability Scenario:** Volumetric DDoS attack or retry storms exhausting edge server memory or cloud APIs. targeting `ARCH-CONT-016`.
   - **Architectural Control:** Redis token-bucket rate limiting, edge offline fallback mode, Cloudflare/Envoy WAF traffic filtering.
   - **Verification Test:** Simulate 5,000 req/min and verify HTTP 429 response without database degradation.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Elevation of Privilege**
   - **Vulnerability Scenario:** Frontline staff member exploits API flaw to gain prescribing or admin rights. targeting `ARCH-CONT-016`.
   - **Architectural Control:** Hardened NestJS RolesGuard, immutable capability claim enforcement, zero-trust token inspection.
   - **Verification Test:** Attempt API call with forged role claim and confirm immediate HTTP 403 Forbidden.
   - **Residual Risk Level:** Low (Controlled)

#### Container Runtime Hardening Directives:
- **Container Security Profile:** Non-root execution (`USER 10001:10001`), read-only rootfs (`readOnlyRootFilesystem: true`).
- **Linux Capability Dropping:** `securityContext.capabilities.drop: ['ALL']`.
- **Network Policy:** Egress restricted to approved service CIDRs; ingress strictly via service mesh.
- **Vulnerability SLA:** Zero Critical/High CVEs allowed in base container image; nightly Trivy rescan.

---

### 02.17 STRIDE Threat Analysis: `ARCH-CONT-017` (Cryptographic WORM Audit Service)
- **Container Identifier:** `ARCH-CONT-017`
- **Container Title:** Cryptographic WORM Audit Service
- **Architectural Classification:** Audit & Security
- **Runtime Technology:** Go / SHA-256 HMAC / Logstash
- **Deployment Context:** Isolated Cloud Security Subnet
- **Associated Data Stores:** `Encrypted Object Store`
- **Governing Product Modules:** MODULE-004, MODULE-005

#### Threat Profile & Specific Mitigations:
1. **Threat Category: Spoofing**
   - **Vulnerability Scenario:** Adversary impersonates an authorized staff member or node. targeting `ARCH-CONT-017`.
   - **Architectural Control:** RS256 JWT tokens with hardware-bound certificates, Argon2id MFA, mutual TLS (mTLS) for edge nodes.
   - **Verification Test:** Verify client certificate chain and check JWT signature against JWKS endpoint.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Tampering**
   - **Vulnerability Scenario:** Malicious modification of clinical records, prescriptions, or batch logs. targeting `ARCH-CONT-017`.
   - **Architectural Control:** TLS 1.3 in-flight encryption, AES-256 GCM storage, SHA-256 HMAC digital signatures on sealed encounters.
   - **Verification Test:** Assert checksum matches SHA-256 hash of payload before accepting updates.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Repudiation**
   - **Vulnerability Scenario:** Provider or pharmacist denies performing a critical clinical action. targeting `ARCH-CONT-017`.
   - **Architectural Control:** Cryptographic WORM append-only audit ledger linking every transaction to a verified staff key.
   - **Verification Test:** Query WORM audit chain to verify cryptographic signature and immutable timestamp.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Information Disclosure**
   - **Vulnerability Scenario:** Unauthorized exfiltration of sensitive patient diagnoses, HIV/TB status, or IDs. targeting `ARCH-CONT-017`.
   - **Architectural Control:** Field-level column encryption, strict ABAC clinic scoping, automated PII log scrubber.
   - **Verification Test:** Inspect logs for redacted patterns and verify ciphertext in database dumps.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Denial of Service**
   - **Vulnerability Scenario:** Volumetric DDoS attack or retry storms exhausting edge server memory or cloud APIs. targeting `ARCH-CONT-017`.
   - **Architectural Control:** Redis token-bucket rate limiting, edge offline fallback mode, Cloudflare/Envoy WAF traffic filtering.
   - **Verification Test:** Simulate 5,000 req/min and verify HTTP 429 response without database degradation.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Elevation of Privilege**
   - **Vulnerability Scenario:** Frontline staff member exploits API flaw to gain prescribing or admin rights. targeting `ARCH-CONT-017`.
   - **Architectural Control:** Hardened NestJS RolesGuard, immutable capability claim enforcement, zero-trust token inspection.
   - **Verification Test:** Attempt API call with forged role claim and confirm immediate HTTP 403 Forbidden.
   - **Residual Risk Level:** Low (Controlled)

#### Container Runtime Hardening Directives:
- **Container Security Profile:** Non-root execution (`USER 10001:10001`), read-only rootfs (`readOnlyRootFilesystem: true`).
- **Linux Capability Dropping:** `securityContext.capabilities.drop: ['ALL']`.
- **Network Policy:** Egress restricted to approved service CIDRs; ingress strictly via service mesh.
- **Vulnerability SLA:** Zero Critical/High CVEs allowed in base container image; nightly Trivy rescan.

---

### 02.18 STRIDE Threat Analysis: `ARCH-CONT-018` (Enterprise Relational Database Cluster)
- **Container Identifier:** `ARCH-CONT-018`
- **Container Title:** Enterprise Relational Database Cluster
- **Architectural Classification:** Data Tier
- **Runtime Technology:** PostgreSQL 16 Multi-AZ with Patroni
- **Deployment Context:** Private Cloud Database Subnet
- **Associated Data Stores:** `NVMe SSD SAN Storage`
- **Governing Product Modules:** ALL MODULES

#### Threat Profile & Specific Mitigations:
1. **Threat Category: Spoofing**
   - **Vulnerability Scenario:** Adversary impersonates an authorized staff member or node. targeting `ARCH-CONT-018`.
   - **Architectural Control:** RS256 JWT tokens with hardware-bound certificates, Argon2id MFA, mutual TLS (mTLS) for edge nodes.
   - **Verification Test:** Verify client certificate chain and check JWT signature against JWKS endpoint.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Tampering**
   - **Vulnerability Scenario:** Malicious modification of clinical records, prescriptions, or batch logs. targeting `ARCH-CONT-018`.
   - **Architectural Control:** TLS 1.3 in-flight encryption, AES-256 GCM storage, SHA-256 HMAC digital signatures on sealed encounters.
   - **Verification Test:** Assert checksum matches SHA-256 hash of payload before accepting updates.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Repudiation**
   - **Vulnerability Scenario:** Provider or pharmacist denies performing a critical clinical action. targeting `ARCH-CONT-018`.
   - **Architectural Control:** Cryptographic WORM append-only audit ledger linking every transaction to a verified staff key.
   - **Verification Test:** Query WORM audit chain to verify cryptographic signature and immutable timestamp.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Information Disclosure**
   - **Vulnerability Scenario:** Unauthorized exfiltration of sensitive patient diagnoses, HIV/TB status, or IDs. targeting `ARCH-CONT-018`.
   - **Architectural Control:** Field-level column encryption, strict ABAC clinic scoping, automated PII log scrubber.
   - **Verification Test:** Inspect logs for redacted patterns and verify ciphertext in database dumps.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Denial of Service**
   - **Vulnerability Scenario:** Volumetric DDoS attack or retry storms exhausting edge server memory or cloud APIs. targeting `ARCH-CONT-018`.
   - **Architectural Control:** Redis token-bucket rate limiting, edge offline fallback mode, Cloudflare/Envoy WAF traffic filtering.
   - **Verification Test:** Simulate 5,000 req/min and verify HTTP 429 response without database degradation.
   - **Residual Risk Level:** Low (Controlled)
1. **Threat Category: Elevation of Privilege**
   - **Vulnerability Scenario:** Frontline staff member exploits API flaw to gain prescribing or admin rights. targeting `ARCH-CONT-018`.
   - **Architectural Control:** Hardened NestJS RolesGuard, immutable capability claim enforcement, zero-trust token inspection.
   - **Verification Test:** Attempt API call with forged role claim and confirm immediate HTTP 403 Forbidden.
   - **Residual Risk Level:** Low (Controlled)

#### Container Runtime Hardening Directives:
- **Container Security Profile:** Non-root execution (`USER 10001:10001`), read-only rootfs (`readOnlyRootFilesystem: true`).
- **Linux Capability Dropping:** `securityContext.capabilities.drop: ['ALL']`.
- **Network Policy:** Egress restricted to approved service CIDRs; ingress strictly via service mesh.
- **Vulnerability SLA:** Zero Critical/High CVEs allowed in base container image; nightly Trivy rescan.

---

## 03. Threat Analysis Across 16 External Integration Interfaces
Comprehensive threat evaluation and defense controls for external integration interfaces:

### 03.01 External Threat Boundary: `EXT-001` (ABDM National Health Gateway)
- **External Entity:** ABDM National Health Gateway (National Health Authority (NHA))
- **Integration Protocol:** REST / HTTPS / FHIR R4 | **Format:** JSON / FHIR Bundle
- **Trust Boundary Tier:** `National DMZ`
- **Permitted Rate Limit:** 100 req/min
- **Outage Fallback Mode:** Asynchronous retry queue

#### Threat Vectors & Protective Controls:
1. **Threat - Man-in-the-Middle (MitM) Interception & Eavesdropping:**
   - *Attack Vector:* Traffic interception between BBMP cloud and `ABDM National Health Gateway`.
   - *Control:* Enforces TLS 1.3 with certificate pinning and mutual TLS (mTLS) client authentication.
   - *Verification:* TLS scanner confirms TLS 1.3 only; attempts to downgrade to TLS 1.2 terminate with handshake error.
2. **Threat - Malformed Payload Injection / Schema Poisoning:**
   - *Attack Vector:* Rogue or corrupted payloads from `ABDM National Health Gateway` attempting buffer overflow or SQL injection.
   - *Control:* Strict inbound Zod / Protobuf schema validation discarding unknown or oversized payload fields.
   - *Verification:* Automated fuzz testing with malformed JSON; service rejects invalid schema with HTTP 400.
3. **Threat - Upstream Service Outage & Resource Starvation:**
   - *Attack Vector:* Remote server latency causes worker thread exhaustion on the BBMP gateway.
   - *Control:* Circuit breaker pattern (Resilience4j) tripping after 5 failures in 10s; routes to fallback: `Asynchronous retry queue`.
   - *Verification:* Mock server timeout; gateway trips breaker in < 2,000ms and logs fallback status.
4. **Threat - Credential Hijacking & Replay Attack:**
   - *Attack Vector:* Stolen API keys or bearer tokens replayed against BBMP integration endpoints.
   - *Control:* Ephemeral JWT bearer tokens (TTL 300s) combined with IP whitelisting and cryptographic nonces.
   - *Verification:* Replaying token after 300 seconds yields HTTP 401 Unauthorized.

---

### 03.02 External Threat Boundary: `EXT-002` (Karnataka Central Drug Warehouse (KDLWS))
- **External Entity:** Karnataka Central Drug Warehouse (KDLWS) (State Health Department)
- **Integration Protocol:** REST / HTTPS / EDI | **Format:** JSON / EDIFACT
- **Trust Boundary Tier:** `State Intranet`
- **Permitted Rate Limit:** 30 req/min
- **Outage Fallback Mode:** Local indent cache

#### Threat Vectors & Protective Controls:
1. **Threat - Man-in-the-Middle (MitM) Interception & Eavesdropping:**
   - *Attack Vector:* Traffic interception between BBMP cloud and `Karnataka Central Drug Warehouse (KDLWS)`.
   - *Control:* Enforces TLS 1.3 with certificate pinning and mutual TLS (mTLS) client authentication.
   - *Verification:* TLS scanner confirms TLS 1.3 only; attempts to downgrade to TLS 1.2 terminate with handshake error.
2. **Threat - Malformed Payload Injection / Schema Poisoning:**
   - *Attack Vector:* Rogue or corrupted payloads from `Karnataka Central Drug Warehouse (KDLWS)` attempting buffer overflow or SQL injection.
   - *Control:* Strict inbound Zod / Protobuf schema validation discarding unknown or oversized payload fields.
   - *Verification:* Automated fuzz testing with malformed JSON; service rejects invalid schema with HTTP 400.
3. **Threat - Upstream Service Outage & Resource Starvation:**
   - *Attack Vector:* Remote server latency causes worker thread exhaustion on the BBMP gateway.
   - *Control:* Circuit breaker pattern (Resilience4j) tripping after 5 failures in 10s; routes to fallback: `Local indent cache`.
   - *Verification:* Mock server timeout; gateway trips breaker in < 2,000ms and logs fallback status.
4. **Threat - Credential Hijacking & Replay Attack:**
   - *Attack Vector:* Stolen API keys or bearer tokens replayed against BBMP integration endpoints.
   - *Control:* Ephemeral JWT bearer tokens (TTL 300s) combined with IP whitelisting and cryptographic nonces.
   - *Verification:* Replaying token after 300 seconds yields HTTP 401 Unauthorized.

---

### 03.03 External Threat Boundary: `EXT-003` (GVK-EMRI 108 Emergency Ambulance Dispatch)
- **External Entity:** GVK-EMRI 108 Emergency Ambulance Dispatch (Emergency Management Research Institute)
- **Integration Protocol:** REST / HTTPS | **Format:** JSON / CAD Event
- **Trust Boundary Tier:** `Emergency Gateway`
- **Permitted Rate Limit:** 120 req/min
- **Outage Fallback Mode:** Manual phone dispatch escalation

#### Threat Vectors & Protective Controls:
1. **Threat - Man-in-the-Middle (MitM) Interception & Eavesdropping:**
   - *Attack Vector:* Traffic interception between BBMP cloud and `GVK-EMRI 108 Emergency Ambulance Dispatch`.
   - *Control:* Enforces TLS 1.3 with certificate pinning and mutual TLS (mTLS) client authentication.
   - *Verification:* TLS scanner confirms TLS 1.3 only; attempts to downgrade to TLS 1.2 terminate with handshake error.
2. **Threat - Malformed Payload Injection / Schema Poisoning:**
   - *Attack Vector:* Rogue or corrupted payloads from `GVK-EMRI 108 Emergency Ambulance Dispatch` attempting buffer overflow or SQL injection.
   - *Control:* Strict inbound Zod / Protobuf schema validation discarding unknown or oversized payload fields.
   - *Verification:* Automated fuzz testing with malformed JSON; service rejects invalid schema with HTTP 400.
3. **Threat - Upstream Service Outage & Resource Starvation:**
   - *Attack Vector:* Remote server latency causes worker thread exhaustion on the BBMP gateway.
   - *Control:* Circuit breaker pattern (Resilience4j) tripping after 5 failures in 10s; routes to fallback: `Manual phone dispatch escalation`.
   - *Verification:* Mock server timeout; gateway trips breaker in < 2,000ms and logs fallback status.
4. **Threat - Credential Hijacking & Replay Attack:**
   - *Attack Vector:* Stolen API keys or bearer tokens replayed against BBMP integration endpoints.
   - *Control:* Ephemeral JWT bearer tokens (TTL 300s) combined with IP whitelisting and cryptographic nonces.
   - *Verification:* Replaying token after 300 seconds yields HTTP 401 Unauthorized.

---

### 03.04 External Threat Boundary: `EXT-004` (Karnataka State SMS Gateway (KSSD))
- **External Entity:** Karnataka State SMS Gateway (KSSD) (Centre for e-Governance (CeG))
- **Integration Protocol:** HTTPS POST API | **Format:** JSON / DLT Template
- **Trust Boundary Tier:** `State Gateway`
- **Permitted Rate Limit:** 500 req/sec
- **Outage Fallback Mode:** Message buffer in Redis BullMQ

#### Threat Vectors & Protective Controls:
1. **Threat - Man-in-the-Middle (MitM) Interception & Eavesdropping:**
   - *Attack Vector:* Traffic interception between BBMP cloud and `Karnataka State SMS Gateway (KSSD)`.
   - *Control:* Enforces TLS 1.3 with certificate pinning and mutual TLS (mTLS) client authentication.
   - *Verification:* TLS scanner confirms TLS 1.3 only; attempts to downgrade to TLS 1.2 terminate with handshake error.
2. **Threat - Malformed Payload Injection / Schema Poisoning:**
   - *Attack Vector:* Rogue or corrupted payloads from `Karnataka State SMS Gateway (KSSD)` attempting buffer overflow or SQL injection.
   - *Control:* Strict inbound Zod / Protobuf schema validation discarding unknown or oversized payload fields.
   - *Verification:* Automated fuzz testing with malformed JSON; service rejects invalid schema with HTTP 400.
3. **Threat - Upstream Service Outage & Resource Starvation:**
   - *Attack Vector:* Remote server latency causes worker thread exhaustion on the BBMP gateway.
   - *Control:* Circuit breaker pattern (Resilience4j) tripping after 5 failures in 10s; routes to fallback: `Message buffer in Redis BullMQ`.
   - *Verification:* Mock server timeout; gateway trips breaker in < 2,000ms and logs fallback status.
4. **Threat - Credential Hijacking & Replay Attack:**
   - *Attack Vector:* Stolen API keys or bearer tokens replayed against BBMP integration endpoints.
   - *Control:* Ephemeral JWT bearer tokens (TTL 300s) combined with IP whitelisting and cryptographic nonces.
   - *Verification:* Replaying token after 300 seconds yields HTTP 401 Unauthorized.

---

### 03.05 External Threat Boundary: `EXT-005` (Integrated Disease Surveillance Program (IDSP/IHIP))
- **External Entity:** Integrated Disease Surveillance Program (IDSP/IHIP) (National Centre for Disease Control (NCDC))
- **Integration Protocol:** REST / HTTPS | **Format:** JSON / CSV Format
- **Trust Boundary Tier:** `National Health Mesh`
- **Permitted Rate Limit:** 50 req/min
- **Outage Fallback Mode:** Daily batch retry

#### Threat Vectors & Protective Controls:
1. **Threat - Man-in-the-Middle (MitM) Interception & Eavesdropping:**
   - *Attack Vector:* Traffic interception between BBMP cloud and `Integrated Disease Surveillance Program (IDSP/IHIP)`.
   - *Control:* Enforces TLS 1.3 with certificate pinning and mutual TLS (mTLS) client authentication.
   - *Verification:* TLS scanner confirms TLS 1.3 only; attempts to downgrade to TLS 1.2 terminate with handshake error.
2. **Threat - Malformed Payload Injection / Schema Poisoning:**
   - *Attack Vector:* Rogue or corrupted payloads from `Integrated Disease Surveillance Program (IDSP/IHIP)` attempting buffer overflow or SQL injection.
   - *Control:* Strict inbound Zod / Protobuf schema validation discarding unknown or oversized payload fields.
   - *Verification:* Automated fuzz testing with malformed JSON; service rejects invalid schema with HTTP 400.
3. **Threat - Upstream Service Outage & Resource Starvation:**
   - *Attack Vector:* Remote server latency causes worker thread exhaustion on the BBMP gateway.
   - *Control:* Circuit breaker pattern (Resilience4j) tripping after 5 failures in 10s; routes to fallback: `Daily batch retry`.
   - *Verification:* Mock server timeout; gateway trips breaker in < 2,000ms and logs fallback status.
4. **Threat - Credential Hijacking & Replay Attack:**
   - *Attack Vector:* Stolen API keys or bearer tokens replayed against BBMP integration endpoints.
   - *Control:* Ephemeral JWT bearer tokens (TTL 300s) combined with IP whitelisting and cryptographic nonces.
   - *Verification:* Replaying token after 300 seconds yields HTTP 401 Unauthorized.

---

### 03.06 External Threat Boundary: `EXT-006` (BBMP Citizen Health Portal)
- **External Entity:** BBMP Citizen Health Portal (Bruhat Bengaluru Mahanagara Palike)
- **Integration Protocol:** REST / HTTPS / OAuth2 | **Format:** JSON
- **Trust Boundary Tier:** `Municipal Cloud`
- **Permitted Rate Limit:** 200 req/min
- **Outage Fallback Mode:** Cached appointment slots

#### Threat Vectors & Protective Controls:
1. **Threat - Man-in-the-Middle (MitM) Interception & Eavesdropping:**
   - *Attack Vector:* Traffic interception between BBMP cloud and `BBMP Citizen Health Portal`.
   - *Control:* Enforces TLS 1.3 with certificate pinning and mutual TLS (mTLS) client authentication.
   - *Verification:* TLS scanner confirms TLS 1.3 only; attempts to downgrade to TLS 1.2 terminate with handshake error.
2. **Threat - Malformed Payload Injection / Schema Poisoning:**
   - *Attack Vector:* Rogue or corrupted payloads from `BBMP Citizen Health Portal` attempting buffer overflow or SQL injection.
   - *Control:* Strict inbound Zod / Protobuf schema validation discarding unknown or oversized payload fields.
   - *Verification:* Automated fuzz testing with malformed JSON; service rejects invalid schema with HTTP 400.
3. **Threat - Upstream Service Outage & Resource Starvation:**
   - *Attack Vector:* Remote server latency causes worker thread exhaustion on the BBMP gateway.
   - *Control:* Circuit breaker pattern (Resilience4j) tripping after 5 failures in 10s; routes to fallback: `Cached appointment slots`.
   - *Verification:* Mock server timeout; gateway trips breaker in < 2,000ms and logs fallback status.
4. **Threat - Credential Hijacking & Replay Attack:**
   - *Attack Vector:* Stolen API keys or bearer tokens replayed against BBMP integration endpoints.
   - *Control:* Ephemeral JWT bearer tokens (TTL 300s) combined with IP whitelisting and cryptographic nonces.
   - *Verification:* Replaying token after 300 seconds yields HTTP 401 Unauthorized.

---

### 03.07 External Threat Boundary: `EXT-007` (National NCD Portal)
- **External Entity:** National NCD Portal (Ministry of Health and Family Welfare (MoHFW))
- **Integration Protocol:** REST / HTTPS | **Format:** JSON / FHIR
- **Trust Boundary Tier:** `National Portal`
- **Permitted Rate Limit:** 60 req/min
- **Outage Fallback Mode:** Offline NCD queue sync

#### Threat Vectors & Protective Controls:
1. **Threat - Man-in-the-Middle (MitM) Interception & Eavesdropping:**
   - *Attack Vector:* Traffic interception between BBMP cloud and `National NCD Portal`.
   - *Control:* Enforces TLS 1.3 with certificate pinning and mutual TLS (mTLS) client authentication.
   - *Verification:* TLS scanner confirms TLS 1.3 only; attempts to downgrade to TLS 1.2 terminate with handshake error.
2. **Threat - Malformed Payload Injection / Schema Poisoning:**
   - *Attack Vector:* Rogue or corrupted payloads from `National NCD Portal` attempting buffer overflow or SQL injection.
   - *Control:* Strict inbound Zod / Protobuf schema validation discarding unknown or oversized payload fields.
   - *Verification:* Automated fuzz testing with malformed JSON; service rejects invalid schema with HTTP 400.
3. **Threat - Upstream Service Outage & Resource Starvation:**
   - *Attack Vector:* Remote server latency causes worker thread exhaustion on the BBMP gateway.
   - *Control:* Circuit breaker pattern (Resilience4j) tripping after 5 failures in 10s; routes to fallback: `Offline NCD queue sync`.
   - *Verification:* Mock server timeout; gateway trips breaker in < 2,000ms and logs fallback status.
4. **Threat - Credential Hijacking & Replay Attack:**
   - *Attack Vector:* Stolen API keys or bearer tokens replayed against BBMP integration endpoints.
   - *Control:* Ephemeral JWT bearer tokens (TTL 300s) combined with IP whitelisting and cryptographic nonces.
   - *Verification:* Replaying token after 300 seconds yields HTTP 401 Unauthorized.

---

### 03.08 External Threat Boundary: `EXT-008` (Nikshay Portal (National TB Elimination))
- **External Entity:** Nikshay Portal (National TB Elimination) (Central TB Division (CTD))
- **Integration Protocol:** REST / HTTPS | **Format:** JSON
- **Trust Boundary Tier:** `National Health Mesh`
- **Permitted Rate Limit:** 60 req/min
- **Outage Fallback Mode:** Presumptive TB case queue

#### Threat Vectors & Protective Controls:
1. **Threat - Man-in-the-Middle (MitM) Interception & Eavesdropping:**
   - *Attack Vector:* Traffic interception between BBMP cloud and `Nikshay Portal (National TB Elimination)`.
   - *Control:* Enforces TLS 1.3 with certificate pinning and mutual TLS (mTLS) client authentication.
   - *Verification:* TLS scanner confirms TLS 1.3 only; attempts to downgrade to TLS 1.2 terminate with handshake error.
2. **Threat - Malformed Payload Injection / Schema Poisoning:**
   - *Attack Vector:* Rogue or corrupted payloads from `Nikshay Portal (National TB Elimination)` attempting buffer overflow or SQL injection.
   - *Control:* Strict inbound Zod / Protobuf schema validation discarding unknown or oversized payload fields.
   - *Verification:* Automated fuzz testing with malformed JSON; service rejects invalid schema with HTTP 400.
3. **Threat - Upstream Service Outage & Resource Starvation:**
   - *Attack Vector:* Remote server latency causes worker thread exhaustion on the BBMP gateway.
   - *Control:* Circuit breaker pattern (Resilience4j) tripping after 5 failures in 10s; routes to fallback: `Presumptive TB case queue`.
   - *Verification:* Mock server timeout; gateway trips breaker in < 2,000ms and logs fallback status.
4. **Threat - Credential Hijacking & Replay Attack:**
   - *Attack Vector:* Stolen API keys or bearer tokens replayed against BBMP integration endpoints.
   - *Control:* Ephemeral JWT bearer tokens (TTL 300s) combined with IP whitelisting and cryptographic nonces.
   - *Verification:* Replaying token after 300 seconds yields HTTP 401 Unauthorized.

---

### 03.09 External Threat Boundary: `EXT-009` (Reproductive and Child Health (RCH) Portal)
- **External Entity:** Reproductive and Child Health (RCH) Portal (MoHFW / Karnataka Health)
- **Integration Protocol:** REST / HTTPS | **Format:** JSON
- **Trust Boundary Tier:** `National Health Mesh`
- **Permitted Rate Limit:** 60 req/min
- **Outage Fallback Mode:** Antenatal offline buffer

#### Threat Vectors & Protective Controls:
1. **Threat - Man-in-the-Middle (MitM) Interception & Eavesdropping:**
   - *Attack Vector:* Traffic interception between BBMP cloud and `Reproductive and Child Health (RCH) Portal`.
   - *Control:* Enforces TLS 1.3 with certificate pinning and mutual TLS (mTLS) client authentication.
   - *Verification:* TLS scanner confirms TLS 1.3 only; attempts to downgrade to TLS 1.2 terminate with handshake error.
2. **Threat - Malformed Payload Injection / Schema Poisoning:**
   - *Attack Vector:* Rogue or corrupted payloads from `Reproductive and Child Health (RCH) Portal` attempting buffer overflow or SQL injection.
   - *Control:* Strict inbound Zod / Protobuf schema validation discarding unknown or oversized payload fields.
   - *Verification:* Automated fuzz testing with malformed JSON; service rejects invalid schema with HTTP 400.
3. **Threat - Upstream Service Outage & Resource Starvation:**
   - *Attack Vector:* Remote server latency causes worker thread exhaustion on the BBMP gateway.
   - *Control:* Circuit breaker pattern (Resilience4j) tripping after 5 failures in 10s; routes to fallback: `Antenatal offline buffer`.
   - *Verification:* Mock server timeout; gateway trips breaker in < 2,000ms and logs fallback status.
4. **Threat - Credential Hijacking & Replay Attack:**
   - *Attack Vector:* Stolen API keys or bearer tokens replayed against BBMP integration endpoints.
   - *Control:* Ephemeral JWT bearer tokens (TTL 300s) combined with IP whitelisting and cryptographic nonces.
   - *Verification:* Replaying token after 300 seconds yields HTTP 401 Unauthorized.

---

### 03.10 External Threat Boundary: `EXT-010` (UIDAI Aadhaar Authentication Service)
- **External Entity:** UIDAI Aadhaar Authentication Service (Unique Identification Authority of India)
- **Integration Protocol:** HTTPS / XML / Auth API | **Format:** Encrypted XML PID Block
- **Trust Boundary Tier:** `Statutory Sovereign`
- **Permitted Rate Limit:** 100 req/min
- **Outage Fallback Mode:** Fallback to municipal health ID

#### Threat Vectors & Protective Controls:
1. **Threat - Man-in-the-Middle (MitM) Interception & Eavesdropping:**
   - *Attack Vector:* Traffic interception between BBMP cloud and `UIDAI Aadhaar Authentication Service`.
   - *Control:* Enforces TLS 1.3 with certificate pinning and mutual TLS (mTLS) client authentication.
   - *Verification:* TLS scanner confirms TLS 1.3 only; attempts to downgrade to TLS 1.2 terminate with handshake error.
2. **Threat - Malformed Payload Injection / Schema Poisoning:**
   - *Attack Vector:* Rogue or corrupted payloads from `UIDAI Aadhaar Authentication Service` attempting buffer overflow or SQL injection.
   - *Control:* Strict inbound Zod / Protobuf schema validation discarding unknown or oversized payload fields.
   - *Verification:* Automated fuzz testing with malformed JSON; service rejects invalid schema with HTTP 400.
3. **Threat - Upstream Service Outage & Resource Starvation:**
   - *Attack Vector:* Remote server latency causes worker thread exhaustion on the BBMP gateway.
   - *Control:* Circuit breaker pattern (Resilience4j) tripping after 5 failures in 10s; routes to fallback: `Fallback to municipal health ID`.
   - *Verification:* Mock server timeout; gateway trips breaker in < 2,000ms and logs fallback status.
4. **Threat - Credential Hijacking & Replay Attack:**
   - *Attack Vector:* Stolen API keys or bearer tokens replayed against BBMP integration endpoints.
   - *Control:* Ephemeral JWT bearer tokens (TTL 300s) combined with IP whitelisting and cryptographic nonces.
   - *Verification:* Replaying token after 300 seconds yields HTTP 401 Unauthorized.

---

### 03.11 External Threat Boundary: `EXT-011` (Zero-Cost Municipal Voucher Billing Gateway)
- **External Entity:** Zero-Cost Municipal Voucher Billing Gateway (BBMP Health Accounts)
- **Integration Protocol:** REST / HTTPS | **Format:** JSON / Voucher Token
- **Trust Boundary Tier:** `Municipal Intranet`
- **Permitted Rate Limit:** 150 req/min
- **Outage Fallback Mode:** Local voucher offline issue

#### Threat Vectors & Protective Controls:
1. **Threat - Man-in-the-Middle (MitM) Interception & Eavesdropping:**
   - *Attack Vector:* Traffic interception between BBMP cloud and `Zero-Cost Municipal Voucher Billing Gateway`.
   - *Control:* Enforces TLS 1.3 with certificate pinning and mutual TLS (mTLS) client authentication.
   - *Verification:* TLS scanner confirms TLS 1.3 only; attempts to downgrade to TLS 1.2 terminate with handshake error.
2. **Threat - Malformed Payload Injection / Schema Poisoning:**
   - *Attack Vector:* Rogue or corrupted payloads from `Zero-Cost Municipal Voucher Billing Gateway` attempting buffer overflow or SQL injection.
   - *Control:* Strict inbound Zod / Protobuf schema validation discarding unknown or oversized payload fields.
   - *Verification:* Automated fuzz testing with malformed JSON; service rejects invalid schema with HTTP 400.
3. **Threat - Upstream Service Outage & Resource Starvation:**
   - *Attack Vector:* Remote server latency causes worker thread exhaustion on the BBMP gateway.
   - *Control:* Circuit breaker pattern (Resilience4j) tripping after 5 failures in 10s; routes to fallback: `Local voucher offline issue`.
   - *Verification:* Mock server timeout; gateway trips breaker in < 2,000ms and logs fallback status.
4. **Threat - Credential Hijacking & Replay Attack:**
   - *Attack Vector:* Stolen API keys or bearer tokens replayed against BBMP integration endpoints.
   - *Control:* Ephemeral JWT bearer tokens (TTL 300s) combined with IP whitelisting and cryptographic nonces.
   - *Verification:* Replaying token after 300 seconds yields HTTP 401 Unauthorized.

---

### 03.12 External Threat Boundary: `EXT-012` (Bio-Medical Waste Management (BMWM) Tracking)
- **External Entity:** Bio-Medical Waste Management (BMWM) Tracking (Karnataka State Pollution Control Board)
- **Integration Protocol:** REST / HTTPS | **Format:** JSON / Barcode Log
- **Trust Boundary Tier:** `Regulatory Gateway`
- **Permitted Rate Limit:** 30 req/min
- **Outage Fallback Mode:** Local waste register

#### Threat Vectors & Protective Controls:
1. **Threat - Man-in-the-Middle (MitM) Interception & Eavesdropping:**
   - *Attack Vector:* Traffic interception between BBMP cloud and `Bio-Medical Waste Management (BMWM) Tracking`.
   - *Control:* Enforces TLS 1.3 with certificate pinning and mutual TLS (mTLS) client authentication.
   - *Verification:* TLS scanner confirms TLS 1.3 only; attempts to downgrade to TLS 1.2 terminate with handshake error.
2. **Threat - Malformed Payload Injection / Schema Poisoning:**
   - *Attack Vector:* Rogue or corrupted payloads from `Bio-Medical Waste Management (BMWM) Tracking` attempting buffer overflow or SQL injection.
   - *Control:* Strict inbound Zod / Protobuf schema validation discarding unknown or oversized payload fields.
   - *Verification:* Automated fuzz testing with malformed JSON; service rejects invalid schema with HTTP 400.
3. **Threat - Upstream Service Outage & Resource Starvation:**
   - *Attack Vector:* Remote server latency causes worker thread exhaustion on the BBMP gateway.
   - *Control:* Circuit breaker pattern (Resilience4j) tripping after 5 failures in 10s; routes to fallback: `Local waste register`.
   - *Verification:* Mock server timeout; gateway trips breaker in < 2,000ms and logs fallback status.
4. **Threat - Credential Hijacking & Replay Attack:**
   - *Attack Vector:* Stolen API keys or bearer tokens replayed against BBMP integration endpoints.
   - *Control:* Ephemeral JWT bearer tokens (TTL 300s) combined with IP whitelisting and cryptographic nonces.
   - *Verification:* Replaying token after 300 seconds yields HTTP 401 Unauthorized.

---

### 03.13 External Threat Boundary: `EXT-013` (Central Referral Hospital LIMS)
- **External Entity:** Central Referral Hospital LIMS (BBMP Tertiary Hospitals (KC General, Bowring))
- **Integration Protocol:** HL7 v2 / FHIR R4 | **Format:** HL7 ORU_R01 / FHIR
- **Trust Boundary Tier:** `Hospital Intranet`
- **Permitted Rate Limit:** 60 req/min
- **Outage Fallback Mode:** Manual result printout

#### Threat Vectors & Protective Controls:
1. **Threat - Man-in-the-Middle (MitM) Interception & Eavesdropping:**
   - *Attack Vector:* Traffic interception between BBMP cloud and `Central Referral Hospital LIMS`.
   - *Control:* Enforces TLS 1.3 with certificate pinning and mutual TLS (mTLS) client authentication.
   - *Verification:* TLS scanner confirms TLS 1.3 only; attempts to downgrade to TLS 1.2 terminate with handshake error.
2. **Threat - Malformed Payload Injection / Schema Poisoning:**
   - *Attack Vector:* Rogue or corrupted payloads from `Central Referral Hospital LIMS` attempting buffer overflow or SQL injection.
   - *Control:* Strict inbound Zod / Protobuf schema validation discarding unknown or oversized payload fields.
   - *Verification:* Automated fuzz testing with malformed JSON; service rejects invalid schema with HTTP 400.
3. **Threat - Upstream Service Outage & Resource Starvation:**
   - *Attack Vector:* Remote server latency causes worker thread exhaustion on the BBMP gateway.
   - *Control:* Circuit breaker pattern (Resilience4j) tripping after 5 failures in 10s; routes to fallback: `Manual result printout`.
   - *Verification:* Mock server timeout; gateway trips breaker in < 2,000ms and logs fallback status.
4. **Threat - Credential Hijacking & Replay Attack:**
   - *Attack Vector:* Stolen API keys or bearer tokens replayed against BBMP integration endpoints.
   - *Control:* Ephemeral JWT bearer tokens (TTL 300s) combined with IP whitelisting and cryptographic nonces.
   - *Verification:* Replaying token after 300 seconds yields HTTP 401 Unauthorized.

---

### 03.14 External Threat Boundary: `EXT-014` (Central Pollution Control Board (CPCB) & Weather API)
- **External Entity:** Central Pollution Control Board (CPCB) & Weather API (CPCB / IMD Bengaluru)
- **Integration Protocol:** REST / HTTPS | **Format:** JSON / Time-series
- **Trust Boundary Tier:** `Public Data`
- **Permitted Rate Limit:** 10 req/min
- **Outage Fallback Mode:** Last known 24h average

#### Threat Vectors & Protective Controls:
1. **Threat - Man-in-the-Middle (MitM) Interception & Eavesdropping:**
   - *Attack Vector:* Traffic interception between BBMP cloud and `Central Pollution Control Board (CPCB) & Weather API`.
   - *Control:* Enforces TLS 1.3 with certificate pinning and mutual TLS (mTLS) client authentication.
   - *Verification:* TLS scanner confirms TLS 1.3 only; attempts to downgrade to TLS 1.2 terminate with handshake error.
2. **Threat - Malformed Payload Injection / Schema Poisoning:**
   - *Attack Vector:* Rogue or corrupted payloads from `Central Pollution Control Board (CPCB) & Weather API` attempting buffer overflow or SQL injection.
   - *Control:* Strict inbound Zod / Protobuf schema validation discarding unknown or oversized payload fields.
   - *Verification:* Automated fuzz testing with malformed JSON; service rejects invalid schema with HTTP 400.
3. **Threat - Upstream Service Outage & Resource Starvation:**
   - *Attack Vector:* Remote server latency causes worker thread exhaustion on the BBMP gateway.
   - *Control:* Circuit breaker pattern (Resilience4j) tripping after 5 failures in 10s; routes to fallback: `Last known 24h average`.
   - *Verification:* Mock server timeout; gateway trips breaker in < 2,000ms and logs fallback status.
4. **Threat - Credential Hijacking & Replay Attack:**
   - *Attack Vector:* Stolen API keys or bearer tokens replayed against BBMP integration endpoints.
   - *Control:* Ephemeral JWT bearer tokens (TTL 300s) combined with IP whitelisting and cryptographic nonces.
   - *Verification:* Replaying token after 300 seconds yields HTTP 401 Unauthorized.

---

### 03.15 External Threat Boundary: `EXT-015` (BBMP Municipal GIS & Ward Boundary Service)
- **External Entity:** BBMP Municipal GIS & Ward Boundary Service (BBMP Town Planning Department)
- **Integration Protocol:** REST / GeoJSON / WFS | **Format:** GeoJSON Polygons
- **Trust Boundary Tier:** `Municipal Intranet`
- **Permitted Rate Limit:** 50 req/min
- **Outage Fallback Mode:** Cached offline GeoJSON layers

#### Threat Vectors & Protective Controls:
1. **Threat - Man-in-the-Middle (MitM) Interception & Eavesdropping:**
   - *Attack Vector:* Traffic interception between BBMP cloud and `BBMP Municipal GIS & Ward Boundary Service`.
   - *Control:* Enforces TLS 1.3 with certificate pinning and mutual TLS (mTLS) client authentication.
   - *Verification:* TLS scanner confirms TLS 1.3 only; attempts to downgrade to TLS 1.2 terminate with handshake error.
2. **Threat - Malformed Payload Injection / Schema Poisoning:**
   - *Attack Vector:* Rogue or corrupted payloads from `BBMP Municipal GIS & Ward Boundary Service` attempting buffer overflow or SQL injection.
   - *Control:* Strict inbound Zod / Protobuf schema validation discarding unknown or oversized payload fields.
   - *Verification:* Automated fuzz testing with malformed JSON; service rejects invalid schema with HTTP 400.
3. **Threat - Upstream Service Outage & Resource Starvation:**
   - *Attack Vector:* Remote server latency causes worker thread exhaustion on the BBMP gateway.
   - *Control:* Circuit breaker pattern (Resilience4j) tripping after 5 failures in 10s; routes to fallback: `Cached offline GeoJSON layers`.
   - *Verification:* Mock server timeout; gateway trips breaker in < 2,000ms and logs fallback status.
4. **Threat - Credential Hijacking & Replay Attack:**
   - *Attack Vector:* Stolen API keys or bearer tokens replayed against BBMP integration endpoints.
   - *Control:* Ephemeral JWT bearer tokens (TTL 300s) combined with IP whitelisting and cryptographic nonces.
   - *Verification:* Replaying token after 300 seconds yields HTTP 401 Unauthorized.

---

### 03.16 External Threat Boundary: `EXT-016` (Cloud Hardware Security Module (KMS / HSM))
- **External Entity:** Cloud Hardware Security Module (KMS / HSM) (MeitY Empaneled Cloud Provider)
- **Integration Protocol:** PKCS#11 / REST KMS | **Format:** Binary Key Blocks
- **Trust Boundary Tier:** `Secure Hardware Enclave`
- **Permitted Rate Limit:** 1,000 req/sec
- **Outage Fallback Mode:** Local TPM 2.0 derived keys

#### Threat Vectors & Protective Controls:
1. **Threat - Man-in-the-Middle (MitM) Interception & Eavesdropping:**
   - *Attack Vector:* Traffic interception between BBMP cloud and `Cloud Hardware Security Module (KMS / HSM)`.
   - *Control:* Enforces TLS 1.3 with certificate pinning and mutual TLS (mTLS) client authentication.
   - *Verification:* TLS scanner confirms TLS 1.3 only; attempts to downgrade to TLS 1.2 terminate with handshake error.
2. **Threat - Malformed Payload Injection / Schema Poisoning:**
   - *Attack Vector:* Rogue or corrupted payloads from `Cloud Hardware Security Module (KMS / HSM)` attempting buffer overflow or SQL injection.
   - *Control:* Strict inbound Zod / Protobuf schema validation discarding unknown or oversized payload fields.
   - *Verification:* Automated fuzz testing with malformed JSON; service rejects invalid schema with HTTP 400.
3. **Threat - Upstream Service Outage & Resource Starvation:**
   - *Attack Vector:* Remote server latency causes worker thread exhaustion on the BBMP gateway.
   - *Control:* Circuit breaker pattern (Resilience4j) tripping after 5 failures in 10s; routes to fallback: `Local TPM 2.0 derived keys`.
   - *Verification:* Mock server timeout; gateway trips breaker in < 2,000ms and logs fallback status.
4. **Threat - Credential Hijacking & Replay Attack:**
   - *Attack Vector:* Stolen API keys or bearer tokens replayed against BBMP integration endpoints.
   - *Control:* Ephemeral JWT bearer tokens (TTL 300s) combined with IP whitelisting and cryptographic nonces.
   - *Verification:* Replaying token after 300 seconds yields HTTP 401 Unauthorized.

---

## 04. 30 Canonical Security Controls (ARCH-SEC-001 to ARCH-SEC-030)
Exhaustive catalog of 30 enterprise security controls governing the platform:

### 04.01 Security Control: `ARCH-SEC-001` (Zero-Trust Identity Verification)
- **Control Identifier:** `ARCH-SEC-001`
- **Security Domain:** Identity & Auth
- **Governing Standard:** NIST SP 800-207
- **Specification:** Every request must provide a valid cryptographic RS256 JWT token with claims verified against active Redis blacklist.
- **Enforcement Mechanism:** API Gateway JWT Guard
- **Automated Verification Test:** Automated unauthenticated request probe.

### 04.02 Security Control: `ARCH-SEC-002` (Argon2id Password Storage)
- **Control Identifier:** `ARCH-SEC-002`
- **Security Domain:** Credential Security
- **Governing Standard:** RFC 9106
- **Specification:** Staff passwords hashed using Argon2id with 64MB memory, 3 iterations, and 4 threads.
- **Enforcement Mechanism:** Auth Module Password Service
- **Automated Verification Test:** Hash format audit verifying argon2id prefix.

### 04.03 Security Control: `ARCH-SEC-003` (TOTP Multi-Factor Authentication)
- **Control Identifier:** `ARCH-SEC-003`
- **Security Domain:** MFA
- **Governing Standard:** RFC 6238
- **Specification:** Mandatory time-based one-time passwords for all clinical and administrative roles.
- **Enforcement Mechanism:** MFA Controller & TOTP Engine
- **Automated Verification Test:** Login attempt without MFA code rejected.

### 04.04 Security Control: `ARCH-SEC-004` (Segregation of Duties Enforcement (SOD-001))
- **Control Identifier:** `ARCH-SEC-004`
- **Security Domain:** Clinical Safety
- **Governing Standard:** MoHFW EHR Standards
- **Specification:** Hard barrier preventing a single user from possessing both prescribing and dispensing entitlements.
- **Enforcement Mechanism:** RBAC Capability Evaluator
- **Automated Verification Test:** Attempt to assign dual roles triggers rejection.

### 04.05 Security Control: `ARCH-SEC-005` (Tenancy Data Isolation Guard)
- **Control Identifier:** `ARCH-SEC-005`
- **Security Domain:** Data Privacy
- **Governing Standard:** DPDP Act 2023
- **Specification:** All database queries automatically filtered by user's assigned `clinic_id` in application repository.
- **Enforcement Mechanism:** Prisma / NestJS Tenancy Middleware
- **Automated Verification Test:** Cross-clinic query returns empty result set.

### 04.06 Security Control: `ARCH-SEC-006` (AES-256 GCM Column Encryption)
- **Control Identifier:** `ARCH-SEC-006`
- **Security Domain:** Data at Rest
- **Governing Standard:** FIPS 140-3
- **Specification:** Sensitive patient PII (names, phone, Aadhaar) encrypted before persistence.
- **Enforcement Mechanism:** PostgreSQL Crypto Interceptor
- **Automated Verification Test:** Database dump inspection verifies ciphertext.

### 04.07 Security Control: `ARCH-SEC-007` (TLS 1.3 Transport Encryption)
- **Control Identifier:** `ARCH-SEC-007`
- **Security Domain:** Data in Transit
- **Governing Standard:** RFC 8446
- **Specification:** All external and internal network communications encrypted with TLS 1.3.
- **Enforcement Mechanism:** Envoy Ingress & Service Mesh
- **Automated Verification Test:** SSL Labs Grade A+ verification scan.

### 04.08 Security Control: `ARCH-SEC-008` (Cryptographic WORM Audit Trail)
- **Control Identifier:** `ARCH-SEC-008`
- **Security Domain:** Non-Repudiation
- **Governing Standard:** DPDP Act 2023
- **Specification:** Every state mutation appends an immutable record with SHA-256 HMAC hash chaining.
- **Enforcement Mechanism:** WORM Audit Service
- **Automated Verification Test:** Tamper test altering row triggers chain break.

### 04.09 Security Control: `ARCH-SEC-009` (Automated PII Log Sanitizer)
- **Control Identifier:** `ARCH-SEC-009`
- **Security Domain:** Privacy Engineering
- **Governing Standard:** DPDP Act 2023
- **Specification:** Logging middleware scrubs patient names, phones, and identifiers before emission.
- **Enforcement Mechanism:** Winston / OpenTelemetry Filter
- **Automated Verification Test:** Log inspection confirms absence of raw PII.

### 04.10 Security Control: `ARCH-SEC-010` (Hardware TPM 2.0 Enclave Sealing)
- **Control Identifier:** `ARCH-SEC-010`
- **Security Domain:** Edge Appliance
- **Governing Standard:** TCG TPM 2.0
- **Specification:** Edge disk encryption keys sealed in Intel N100 TPM chip; released only on secure boot.
- **Enforcement Mechanism:** Linux LUKS TPM Enclave
- **Automated Verification Test:** Altered bootloader fails disk unlock.

### 04.11 Security Control: `ARCH-SEC-011` (Physical Chassis Intrusion Alarm)
- **Control Identifier:** `ARCH-SEC-011`
- **Security Domain:** Physical Security
- **Governing Standard:** NIST SP 800-53
- **Specification:** Edge server wall-cabinet switch detects unauthorized physical access and alerts helpdesk.
- **Enforcement Mechanism:** Edge Telemetry Daemon
- **Automated Verification Test:** Simulated chassis open fires telemetry alarm.

### 04.12 Security Control: `ARCH-SEC-012` (Distributed Redis Rate Limiting)
- **Control Identifier:** `ARCH-SEC-012`
- **Security Domain:** DDoS Protection
- **Governing Standard:** NIST SP 800-53
- **Specification:** Token-bucket rate limiting tiered by client type preventing volumetric denial of service.
- **Enforcement Mechanism:** Envoy / Redis Middleware
- **Automated Verification Test:** Load test confirms HTTP 429 on limit breach.

### 04.13 Security Control: `ARCH-SEC-013` (Dynamic RBAC Capability Evaluation)
- **Control Identifier:** `ARCH-SEC-013`
- **Security Domain:** Authorization
- **Governing Standard:** NIST SP 800-162
- **Specification:** Permissions evaluated dynamically per request based on cryptographic token claims.
- **Enforcement Mechanism:** NestJS RolesGuard
- **Automated Verification Test:** Probe with missing claim returns HTTP 403.

### 04.14 Security Control: `ARCH-SEC-014` (Emergency Break-Glass Protocol)
- **Control Identifier:** `ARCH-SEC-014`
- **Security Domain:** Clinical Override
- **Governing Standard:** MoHFW EHR Standards
- **Specification:** Enables emergency access to medical records during life-threatening crises with mandatory audit.
- **Enforcement Mechanism:** Emergency Triage Controller
- **Automated Verification Test:** Break-glass access emits high-priority alert.

### 04.15 Security Control: `ARCH-SEC-015` (Content Security Policy Level 3)
- **Control Identifier:** `ARCH-SEC-015`
- **Security Domain:** Frontend Security
- **Governing Standard:** W3C CSP Level 3
- **Specification:** Strict CSP headers preventing cross-site scripting and unauthorized script execution.
- **Enforcement Mechanism:** Next.js HTTP Header Middleware
- **Automated Verification Test:** Browser console confirms script block.

### 04.16 Security Control: `ARCH-SEC-016` (Mutual TLS Edge Mesh)
- **Control Identifier:** `ARCH-SEC-016`
- **Security Domain:** Edge Security
- **Governing Standard:** RFC 8705
- **Specification:** Edge mini-servers authenticate to cloud via X.509 client certificates signed by internal CA.
- **Enforcement Mechanism:** gRPC Sync Gateway
- **Automated Verification Test:** Connection with untrusted cert terminated.

### 04.17 Security Control: `ARCH-SEC-017` (HashiCorp Vault Secrets Engine)
- **Control Identifier:** `ARCH-SEC-017`
- **Security Domain:** Secrets Management
- **Governing Standard:** NIST SP 800-57
- **Specification:** All credentials, API keys, and database passwords retrieved dynamically from Vault.
- **Enforcement Mechanism:** Vault Agent / Kubernetes Sidecar
- **Automated Verification Test:** Zero plaintext secrets in source or manifests.

### 04.18 Security Control: `ARCH-SEC-018` (Static Application Security Testing)
- **Control Identifier:** `ARCH-SEC-018`
- **Security Domain:** DevSecOps
- **Governing Standard:** OWASP ASVS
- **Specification:** Automated SonarQube / Semgrep analysis in CI pipeline blocking PRs with security flaws.
- **Enforcement Mechanism:** GitHub Actions CI
- **Automated Verification Test:** Commit with vulnerable pattern fails build.

### 04.19 Security Control: `ARCH-SEC-019` (Software Composition Analysis (SCA))
- **Control Identifier:** `ARCH-SEC-019`
- **Security Domain:** Supply Chain
- **Governing Standard:** NIST SP 800-161
- **Specification:** Nightly vulnerability scans with Snyk / Trivy; blocks deployment on High/Critical CVEs.
- **Enforcement Mechanism:** CI Deployment Gate
- **Automated Verification Test:** Vulnerable package dependency fails deploy.

### 04.20 Security Control: `ARCH-SEC-020` (CERT-In Incident Triage Workflow)
- **Control Identifier:** `ARCH-SEC-020`
- **Security Domain:** Incident Response
- **Governing Standard:** CERT-In Rules 2022
- **Specification:** Automated runbooks ensuring security incident reporting within statutory 6-hour SLA.
- **Enforcement Mechanism:** SIEM / PagerDuty Escalation
- **Automated Verification Test:** Incident drill exercises 6-hour dispatch.

### 04.21 Security Control: `ARCH-SEC-021` (Container Non-Root Isolation)
- **Control Identifier:** `ARCH-SEC-021`
- **Security Domain:** Container Security
- **Governing Standard:** CIS Docker Benchmark
- **Specification:** All microservices run as non-root UID 10001 with read-only root filesystems.
- **Enforcement Mechanism:** Kubernetes SecurityContext
- **Automated Verification Test:** Container root write attempt fails.

### 04.22 Security Control: `ARCH-SEC-022` (Micro-Segmented VPC Subnets)
- **Control Identifier:** `ARCH-SEC-022`
- **Security Domain:** Network Security
- **Governing Standard:** NIST SP 800-125B
- **Specification:** Cloud subnets isolated with network security groups; databases unreachable from internet.
- **Enforcement Mechanism:** Cloud VPC Routing
- **Automated Verification Test:** Direct external connection to port 5432 fails.

### 04.23 Security Control: `ARCH-SEC-023` (Database Row-Level Encryption)
- **Control Identifier:** `ARCH-SEC-023`
- **Security Domain:** Data at Rest
- **Governing Standard:** FIPS 140-3
- **Specification:** PostgreSQL tables utilize pgcrypto / application AES-256 for clinical notes.
- **Enforcement Mechanism:** Database Persistence Layer
- **Automated Verification Test:** Raw disk inspection reveals ciphertext.

### 04.24 Security Control: `ARCH-SEC-024` (Ephemeral Session Token Lifetimes)
- **Control Identifier:** `ARCH-SEC-024`
- **Security Domain:** Session Management
- **Governing Standard:** OWASP Session Mgmt
- **Specification:** Access tokens valid for 15 minutes; refresh tokens valid for 8 hours with rotation.
- **Enforcement Mechanism:** IAM Token Service
- **Automated Verification Test:** Expired token returns HTTP 401.

### 04.25 Security Control: `ARCH-SEC-025` (Idempotency Lock Protection)
- **Control Identifier:** `ARCH-SEC-025`
- **Security Domain:** Transaction Security
- **Governing Standard:** RFC 7231
- **Specification:** Enforces distributed Redis locks preventing replay or duplicate financial transactions.
- **Enforcement Mechanism:** Idempotency Interceptor
- **Automated Verification Test:** Duplicate request with same key returns cached response.

### 04.26 Security Control: `ARCH-SEC-026` (Clinic LAN Network Separation)
- **Control Identifier:** `ARCH-SEC-026`
- **Security Domain:** Perimeter Security
- **Governing Standard:** NIST SP 800-94
- **Specification:** Clinical medical device LAN (VLAN 10) completely isolated from public waiting area (VLAN 20).
- **Enforcement Mechanism:** Clinic Managed Switch
- **Automated Verification Test:** Ping from VLAN 20 to VLAN 10 blocked.

### 04.27 Security Control: `ARCH-SEC-027` (Automated Daily Vulnerability Rescan)
- **Control Identifier:** `ARCH-SEC-027`
- **Security Domain:** Vulnerability Mgmt
- **Governing Standard:** ISO 27001
- **Specification:** Daily automated scans of public IP ranges and container registries for zero-day flaws.
- **Enforcement Mechanism:** Qualys / OpenVAS Scanner
- **Automated Verification Test:** Daily report generated for CISO.

### 04.28 Security Control: `ARCH-SEC-028` (Digital Personal Consent Lifecycle)
- **Control Identifier:** `ARCH-SEC-028`
- **Security Domain:** Data Governance
- **Governing Standard:** DPDP Act 2023
- **Specification:** Tracks citizen consent granting, duration, purpose limitation, and revocation.
- **Enforcement Mechanism:** Consent Management Service
- **Automated Verification Test:** Revoked consent blocks health record export.

### 04.29 Security Control: `ARCH-SEC-029` (Anti-Tamper Firmware Verification)
- **Control Identifier:** `ARCH-SEC-029`
- **Security Domain:** Appliance Integrity
- **Governing Standard:** NIST SP 800-193
- **Specification:** UEFI Secure Boot verifies signature of bootloader and Linux kernel before startup.
- **Enforcement Mechanism:** Intel N100 UEFI
- **Automated Verification Test:** Modified kernel image fails boot.

### 04.30 Security Control: `ARCH-SEC-030` (Penetration Testing & Red Teaming)
- **Control Identifier:** `ARCH-SEC-030`
- **Security Domain:** Assurance
- **Governing Standard:** CERT-In Empaneled
- **Specification:** Bi-annual independent gray-box penetration testing by CERT-In empaneled security agency.
- **Enforcement Mechanism:** Security Audit Board
- **Automated Verification Test:** Formal sign-off report prior to production release.

## 05. Detailed Role Profiles Across All 30 Platform Roles
Exhaustive specifications, capability grants, segregation-of-duties invariants, and JWT claims across all 30 platform roles:

### 05.01 Role Specification: `ROLE-001` (Citizen / Patient)
- **Role Code:** `ROLE-001`
- **Role Title:** Citizen / Patient
- **Operational Description:** Outpatient citizen receiving primary healthcare services.
- **Data Tenancy Scope:** Own citizen profile and medical summary.
- **Segregation of Duties Rule:** N/A - End citizen user.
- **Clinical & Governance Policy:** Read-only access to own medical summary; cannot alter clinical notes or audit records.

#### Explicit Permitted Capabilities:
- `GRANT`: `citizen:profile:read`
- `GRANT`: `citizen:appointments:book`
- `GRANT`: `citizen:token:view`
- `GRANT`: `citizen:record:abdm:share`

#### Strictly Forbidden Capabilities:
- `DENY`: `encounter:write`
- `DENY`: `prescription:write`
- `DENY`: `pharmacy:dispense`
- `DENY`: `system:admin`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-001-001",
  "role": "ROLE-001",
  "role_title": "Citizen / Patient",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["citizen:profile:read", "citizen:appointments:book", "citizen:token:view", "citizen:record:abdm:share"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.02 Role Specification: `ROLE-002` (Authorized Guardian)
- **Role Code:** `ROLE-002`
- **Role Title:** Authorized Guardian
- **Operational Description:** Parent or legal guardian of pediatric or geriatric patient.
- **Data Tenancy Scope:** Dependent minor or senior citizen records.
- **Segregation of Duties Rule:** N/A - Citizen surrogate.
- **Clinical & Governance Policy:** Requires verified guardianship proof before proxy access is granted.

#### Explicit Permitted Capabilities:
- `GRANT`: `citizen:profile:read`
- `GRANT`: `citizen:surrogate:consent`
- `GRANT`: `citizen:token:view`

#### Strictly Forbidden Capabilities:
- `DENY`: `encounter:write`
- `DENY`: `prescription:write`
- `DENY`: `pharmacy:dispense`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-002-001",
  "role": "ROLE-002",
  "role_title": "Authorized Guardian",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["citizen:profile:read", "citizen:surrogate:consent", "citizen:token:view"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.03 Role Specification: `ROLE-003` (Frontline Staff Nurse)
- **Role Code:** `ROLE-003`
- **Role Title:** Frontline Staff Nurse
- **Operational Description:** Nursing officer conducting intake, vitals, triage, and immunizations.
- **Data Tenancy Scope:** Assigned clinic facility patients during active shift.
- **Segregation of Duties Rule:** Cannot prescribe medications or dispense pharmacy stock.
- **Clinical & Governance Policy:** Permitted to capture vital signs and triage acuity; prohibited from prescribing.

#### Explicit Permitted Capabilities:
- `GRANT`: `patient:register`
- `GRANT`: `vitals:record`
- `GRANT`: `token:issue`
- `GRANT`: `mews:calculate`
- `GRANT`: `immunization:log`

#### Strictly Forbidden Capabilities:
- `DENY`: `prescription:sign`
- `DENY`: `pharmacy:dispense`
- `DENY`: `audit:purge`
- `DENY`: `system:configure`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-003-001",
  "role": "ROLE-003",
  "role_title": "Frontline Staff Nurse",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["patient:register", "vitals:record", "token:issue", "mews:calculate", "immunization:log"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.04 Role Specification: `ROLE-004` (Medical Officer (Doctor))
- **Role Code:** `ROLE-004`
- **Role Title:** Medical Officer (Doctor)
- **Operational Description:** Licensed primary care physician diagnosing and prescribing care.
- **Data Tenancy Scope:** Assigned clinic facility active patient encounters.
- **Segregation of Duties Rule:** PROHIBITED from dispensing pharmacy stock (SOD-001).
- **Clinical & Governance Policy:** Statutory clinical authority; electronic signature attached to all SOAP notes and prescriptions.

#### Explicit Permitted Capabilities:
- `GRANT`: `encounter:soap:write`
- `GRANT`: `prescription:sign`
- `GRANT`: `lab:order`
- `GRANT`: `referral:create`
- `GRANT`: `break_glass:trigger`

#### Strictly Forbidden Capabilities:
- `DENY`: `pharmacy:dispense`
- `DENY`: `stock:adjust`
- `DENY`: `audit:purge`
- `DENY`: `system:configure`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-004-001",
  "role": "ROLE-004",
  "role_title": "Medical Officer (Doctor)",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["encounter:soap:write", "prescription:sign", "lab:order", "referral:create", "break_glass:trigger"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.05 Role Specification: `ROLE-005` (Specialist Consultant)
- **Role Code:** `ROLE-005`
- **Role Title:** Specialist Consultant
- **Operational Description:** Secondary/tertiary hospital specialist conducting tele-consultations.
- **Data Tenancy Scope:** Patients referred across BBMP secondary care network.
- **Segregation of Duties Rule:** PROHIBITED from dispensing pharmacy stock.
- **Clinical & Governance Policy:** Reviews referred primary dossiers and provides advisory specialist opinions.

#### Explicit Permitted Capabilities:
- `GRANT`: `encounter:review`
- `GRANT`: `telemed:consult:write`
- `GRANT`: `referral:counter:sign`
- `GRANT`: `lab:confirmatory:order`

#### Strictly Forbidden Capabilities:
- `DENY`: `pharmacy:dispense`
- `DENY`: `stock:receive`
- `DENY`: `clinic:admin`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-005-001",
  "role": "ROLE-005",
  "role_title": "Specialist Consultant",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["encounter:review", "telemed:consult:write", "referral:counter:sign", "lab:confirmatory:order"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.06 Role Specification: `ROLE-006` (Clinic Pharmacist)
- **Role Code:** `ROLE-006`
- **Role Title:** Clinic Pharmacist
- **Operational Description:** Licensed pharmacist dispensing medications and managing clinic inventory.
- **Data Tenancy Scope:** Assigned clinic pharmacy dispensary and stock room.
- **Segregation of Duties Rule:** PROHIBITED from creating or altering prescriptions (SOD-001).
- **Clinical & Governance Policy:** Verifies 2D DataMatrix barcode on drug strip before dispensing; cannot alter doctor's dosage.

#### Explicit Permitted Capabilities:
- `GRANT`: `pharmacy:dispense`
- `GRANT`: `inventory:batch:scan`
- `GRANT`: `indent:create`
- `GRANT`: `counseling:log`

#### Strictly Forbidden Capabilities:
- `DENY`: `prescription:create`
- `DENY`: `prescription:alter`
- `DENY`: `encounter:soap:write`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-006-001",
  "role": "ROLE-006",
  "role_title": "Clinic Pharmacist",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["pharmacy:dispense", "inventory:batch:scan", "indent:create", "counseling:log"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.07 Role Specification: `ROLE-007` (Inventory Stock Clerk)
- **Role Code:** `ROLE-007`
- **Role Title:** Inventory Stock Clerk
- **Operational Description:** Storekeeper assisting pharmacist with logistics and warehousing.
- **Data Tenancy Scope:** Assigned clinic drug store room.
- **Segregation of Duties Rule:** Cannot dispense medications directly to patients.
- **Clinical & Governance Policy:** Logs incoming shipments from KDLWS; records daily vaccine refrigerator temperatures.

#### Explicit Permitted Capabilities:
- `GRANT`: `inventory:receive`
- `GRANT`: `indent:draft`
- `GRANT`: `stock:count`
- `GRANT`: `coldchain:log`

#### Strictly Forbidden Capabilities:
- `DENY`: `pharmacy:dispense`
- `DENY`: `prescription:sign`
- `DENY`: `clinical:notes:view`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-007-001",
  "role": "ROLE-007",
  "role_title": "Inventory Stock Clerk",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["inventory:receive", "indent:draft", "stock:count", "coldchain:log"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.08 Role Specification: `ROLE-008` (Laboratory Technician)
- **Role Code:** `ROLE-008`
- **Role Title:** Laboratory Technician
- **Operational Description:** Medical lab technologist conducting 58 rapid point-of-care tests.
- **Data Tenancy Scope:** Assigned clinic laboratory diagnostic section.
- **Segregation of Duties Rule:** Cannot formulate clinical diagnoses or alter orders.
- **Clinical & Governance Policy:** Enters quantitative and qualitative test values; triggers immediate panic value escalations.

#### Explicit Permitted Capabilities:
- `GRANT`: `lab:specimen:receive`
- `GRANT`: `lab:result:enter`
- `GRANT`: `panic:alert`
- `GRANT`: `qc:log:write`

#### Strictly Forbidden Capabilities:
- `DENY`: `prescription:sign`
- `DENY`: `encounter:write`
- `DENY`: `pharmacy:dispense`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-008-001",
  "role": "ROLE-008",
  "role_title": "Laboratory Technician",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["lab:specimen:receive", "lab:result:enter", "panic:alert", "qc:log:write"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.09 Role Specification: `ROLE-009` (ANM Outreach Nurse)
- **Role Code:** `ROLE-009`
- **Role Title:** ANM Outreach Nurse
- **Operational Description:** Auxiliary Nurse Midwife executing field screening and immunizations.
- **Data Tenancy Scope:** Assigned municipal ward and field outreach cohorts.
- **Segregation of Duties Rule:** Cannot alter doctor clinical diagnoses.
- **Clinical & Governance Policy:** Conducts community health screenings; synchronizes offline mobile data on clinic return.

#### Explicit Permitted Capabilities:
- `GRANT`: `ncd:field:screen`
- `GRANT`: `immunization:log`
- `GRANT`: `recall:execute`
- `GRANT`: `mch:antenatal:log`

#### Strictly Forbidden Capabilities:
- `DENY`: `prescription:sign`
- `DENY`: `lab:panic:override`
- `DENY`: `facility:admin`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-009-001",
  "role": "ROLE-009",
  "role_title": "ANM Outreach Nurse",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["ncd:field:screen", "immunization:log", "recall:execute", "mch:antenatal:log"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.10 Role Specification: `ROLE-010` (ASHA Health Volunteer)
- **Role Code:** `ROLE-010`
- **Role Title:** ASHA Health Volunteer
- **Operational Description:** Community health volunteer tracking chronic disease defaulters.
- **Data Tenancy Scope:** Assigned municipal polling booth or community ward.
- **Segregation of Duties Rule:** Read-only outreach lists; zero EMR clinical access.
- **Clinical & Governance Policy:** Conducts door-to-door visit reminders for hypertension and diabetes follow-ups.

#### Explicit Permitted Capabilities:
- `GRANT`: `ncd:defaulter:roster:view`
- `GRANT`: `citizen:outreach:log`
- `GRANT`: `camp:attendance:log`

#### Strictly Forbidden Capabilities:
- `DENY`: `clinical:notes:view`
- `DENY`: `prescription:write`
- `DENY`: `patient:delete`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-010-001",
  "role": "ROLE-010",
  "role_title": "ASHA Health Volunteer",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["ncd:defaulter:roster:view", "citizen:outreach:log", "camp:attendance:log"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.11 Role Specification: `ROLE-011` (Clinic Facility Admin)
- **Role Code:** `ROLE-011`
- **Role Title:** Clinic Facility Admin
- **Operational Description:** Administrative manager overseeing clinic facility operations.
- **Data Tenancy Scope:** Assigned clinic operational infrastructure.
- **Segregation of Duties Rule:** Zero access to patient clinical health records.
- **Clinical & Governance Policy:** Manages room assignments, duty rosters, hardware helpdesk tickets, and utility logs.

#### Explicit Permitted Capabilities:
- `GRANT`: `staff:roster:manage`
- `GRANT`: `appliance:status:view`
- `GRANT`: `kiosk:reset`
- `GRANT`: `maintenance:ticket:create`

#### Strictly Forbidden Capabilities:
- `DENY`: `clinical:notes:view`
- `DENY`: `prescription:view`
- `DENY`: `lab:results:view`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-011-001",
  "role": "ROLE-011",
  "role_title": "Clinic Facility Admin",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["staff:roster:manage", "appliance:status:view", "kiosk:reset", "maintenance:ticket:create"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.12 Role Specification: `ROLE-012` (Zonal Chief Medical Officer)
- **Role Code:** `ROLE-012`
- **Role Title:** Zonal Chief Medical Officer
- **Operational Description:** Senior BBMP health administrator supervising zonal clinics.
- **Data Tenancy Scope:** Assigned BBMP Zone (20+ primary clinics).
- **Segregation of Duties Rule:** Read-only aggregate & governance; no direct prescribing.
- **Clinical & Governance Policy:** Inspects clinic performance, reviews clinical audit metrics, and reallocates medical personnel.

#### Explicit Permitted Capabilities:
- `GRANT`: `zonal:kpi:view`
- `GRANT`: `audit:review`
- `GRANT`: `resource:allocate`
- `GRANT`: `epidemic:investigate`

#### Strictly Forbidden Capabilities:
- `DENY`: `direct:prescribing`
- `DENY`: `pharmacy:dispense`
- `DENY`: `data:purge`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-012-001",
  "role": "ROLE-012",
  "role_title": "Zonal Chief Medical Officer",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["zonal:kpi:view", "audit:review", "resource:allocate", "epidemic:investigate"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.13 Role Specification: `ROLE-013` (Municipal Epidemiologist)
- **Role Code:** `ROLE-013`
- **Role Title:** Municipal Epidemiologist
- **Operational Description:** Public health physician tracking disease incidence and outbreaks.
- **Data Tenancy Scope:** City-wide BBMP health data (183 clinics).
- **Segregation of Duties Rule:** De-identified and aggregated health records only.
- **Clinical & Governance Policy:** Analyzes daily fever trends, spatial dengue clusters, and submits statutory IDSP Form P/L/S reports.

#### Explicit Permitted Capabilities:
- `GRANT`: `analytics:syndromic:read`
- `GRANT`: `idsp:export`
- `GRANT`: `cluster:investigate`
- `GRANT`: `alert:broadcast:draft`

#### Strictly Forbidden Capabilities:
- `DENY`: `patient:pii:view`
- `DENY`: `direct:prescribing`
- `DENY`: `inventory:alter`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-013-001",
  "role": "ROLE-013",
  "role_title": "Municipal Epidemiologist",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["analytics:syndromic:read", "idsp:export", "cluster:investigate", "alert:broadcast:draft"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.14 Role Specification: `ROLE-014` (NQAS Quality Auditor)
- **Role Code:** `ROLE-014`
- **Role Title:** NQAS Quality Auditor
- **Operational Description:** National Quality Assurance Standards inspector.
- **Data Tenancy Scope:** City-wide BBMP clinics undergoing quality accreditation.
- **Segregation of Duties Rule:** Read-only inspection views; zero modification.
- **Clinical & Governance Policy:** Audits facility cleanliness, drug availability, waiting times, and statutory SOP adherence.

#### Explicit Permitted Capabilities:
- `GRANT`: `quality:audit:read`
- `GRANT`: `checklist:evaluate`
- `GRANT`: `compliance:log`
- `GRANT`: `facility:inspect`

#### Strictly Forbidden Capabilities:
- `DENY`: `patient:pii:view`
- `DENY`: `clinical:notes:edit`
- `DENY`: `pharmacy:dispense`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-014-001",
  "role": "ROLE-014",
  "role_title": "NQAS Quality Auditor",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["quality:audit:read", "checklist:evaluate", "compliance:log", "facility:inspect"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.15 Role Specification: `ROLE-015` (108 Paramedic / Transit)
- **Role Code:** `ROLE-015`
- **Role Title:** 108 Paramedic / Transit
- **Operational Description:** Emergency medical technician operating 108 ambulance transfer.
- **Data Tenancy Scope:** Active transit referral emergency case.
- **Segregation of Duties Rule:** Emergency handover window only (2-hour TTL).
- **Clinical & Governance Policy:** Streams continuous vitals during secondary hospital transit; confirms physical patient handover.

#### Explicit Permitted Capabilities:
- `GRANT`: `ems:telemetry:write`
- `GRANT`: `transit:vitals:log`
- `GRANT`: `handover:confirm`
- `GRANT`: `emergency:dossier:view`

#### Strictly Forbidden Capabilities:
- `DENY`: `routine:clinic:records`
- `DENY`: `prescription:sign`
- `DENY`: `system:admin`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-015-001",
  "role": "ROLE-015",
  "role_title": "108 Paramedic / Transit",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["ems:telemetry:write", "transit:vitals:log", "handover:confirm", "emergency:dossier:view"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.16 Role Specification: `ROLE-016` (State Logistics Officer)
- **Role Code:** `ROLE-016`
- **Role Title:** State Logistics Officer
- **Operational Description:** Karnataka State Central Drug Warehouse (KDLWS) manager.
- **Data Tenancy Scope:** State-wide drug depot and warehouse logistics.
- **Segregation of Duties Rule:** Warehouse logistics domain only.
- **Clinical & Governance Policy:** Reviews aggregated municipal drug indents, allocates batches, and authorizes delivery manifests.

#### Explicit Permitted Capabilities:
- `GRANT`: `indent:approve`
- `GRANT`: `depot:dispatch:sign`
- `GRANT`: `formulary:edit`
- `GRANT`: `state:inventory:view`

#### Strictly Forbidden Capabilities:
- `DENY`: `patient:clinical:records`
- `DENY`: `direct:dispensing`
- `DENY`: `clinic:roster`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-016-001",
  "role": "ROLE-016",
  "role_title": "State Logistics Officer",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["indent:approve", "depot:dispatch:sign", "formulary:edit", "state:inventory:view"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.17 Role Specification: `ROLE-017` (Municipal Ombudsman)
- **Role Code:** `ROLE-017`
- **Role Title:** Municipal Ombudsman
- **Operational Description:** Independent grievance officer investigating citizen complaints.
- **Data Tenancy Scope:** Municipal citizen grievance registry.
- **Segregation of Duties Rule:** Grievance records only; zero clinical health data.
- **Clinical & Governance Policy:** Investigates patient grievances regarding staff rudeness, drug stockouts, or excessive wait times.

#### Explicit Permitted Capabilities:
- `GRANT`: `grievance:investigate`
- `GRANT`: `sla:escalate`
- `GRANT`: `feedback:audit`
- `GRANT`: `hearing:schedule`

#### Strictly Forbidden Capabilities:
- `DENY`: `patient:clinical:records`
- `DENY`: `prescription:edit`
- `DENY`: `system:admin`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-017-001",
  "role": "ROLE-017",
  "role_title": "Municipal Ombudsman",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["grievance:investigate", "sla:escalate", "feedback:audit", "hearing:schedule"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.18 Role Specification: `ROLE-018` (Hardware Field Technician)
- **Role Code:** `ROLE-018`
- **Role Title:** Hardware Field Technician
- **Operational Description:** IT hardware support technician servicing clinic appliances.
- **Data Tenancy Scope:** Physical hardware appliances and edge mini-servers.
- **Segregation of Duties Rule:** Zero software database or patient health record access.
- **Clinical & Governance Policy:** Replaces jammed thermal printers, tests UPS battery discharge cycles, and executes hardware firmware updates.

#### Explicit Permitted Capabilities:
- `GRANT`: `hardware:telemetry:read`
- `GRANT`: `appliance:reboot`
- `GRANT`: `ups:test`
- `GRANT`: `printer:calibrate`

#### Strictly Forbidden Capabilities:
- `DENY`: `patient:data:read`
- `DENY`: `clinical:records`
- `DENY`: `audit:purge`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-018-001",
  "role": "ROLE-018",
  "role_title": "Hardware Field Technician",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["hardware:telemetry:read", "appliance:reboot", "ups:test", "printer:calibrate"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.19 Role Specification: `ROLE-019` (Platform SRE / DevOps)
- **Role Code:** `ROLE-019`
- **Role Title:** Platform SRE / DevOps
- **Operational Description:** Site reliability engineer managing cloud infrastructure.
- **Data Tenancy Scope:** Cloud infrastructure and Kubernetes clusters.
- **Segregation of Duties Rule:** Zero plaintext PHI access; all data encrypted at rest.
- **Clinical & Governance Policy:** Monitors container health, executes database failover drills, and optimizes connection pools.

#### Explicit Permitted Capabilities:
- `GRANT`: `k8s:cluster:manage`
- `GRANT`: `db:backup:trigger`
- `GRANT`: `dr:failover:test`
- `GRANT`: `infra:scale`

#### Strictly Forbidden Capabilities:
- `DENY`: `plaintext:phi:read`
- `DENY`: `prescription:edit`
- `DENY`: `clinical:notes:view`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-019-001",
  "role": "ROLE-019",
  "role_title": "Platform SRE / DevOps",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["k8s:cluster:manage", "db:backup:trigger", "dr:failover:test", "infra:scale"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.20 Role Specification: `ROLE-020` (Data Protection Officer)
- **Role Code:** `ROLE-020`
- **Role Title:** Data Protection Officer
- **Operational Description:** Statutory privacy officer enforcing DPDP Act 2023 compliance.
- **Data Tenancy Scope:** Privacy audit ledgers and consent registers city-wide.
- **Segregation of Duties Rule:** Privacy governance domain only.
- **Clinical & Governance Policy:** Audits compliance with citizen consent directives and investigates potential data breach incidents.

#### Explicit Permitted Capabilities:
- `GRANT`: `dpdp:audit:inspect`
- `GRANT`: `consent:revocation:audit`
- `GRANT`: `breach:report`
- `GRANT`: `pii:flow:audit`

#### Strictly Forbidden Capabilities:
- `DENY`: `direct:prescribing`
- `DENY`: `clinical:intervention`
- `DENY`: `system:code:edit`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-020-001",
  "role": "ROLE-020",
  "role_title": "Data Protection Officer",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["dpdp:audit:inspect", "consent:revocation:audit", "breach:report", "pii:flow:audit"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.21 Role Specification: `ROLE-021` (State HMIS Officer)
- **Role Code:** `ROLE-021`
- **Role Title:** State HMIS Officer
- **Operational Description:** Health Management Information System statistical officer.
- **Data Tenancy Scope:** Aggregated municipal health performance metrics.
- **Segregation of Duties Rule:** Aggregated indicator reports only.
- **Clinical & Governance Policy:** Collates monthly municipal health indicators for upload to the Ministry of Health national portal.

#### Explicit Permitted Capabilities:
- `GRANT`: `hmis:monthly:export`
- `GRANT`: `statutory:form:generate`
- `GRANT`: `national:portal:sync`

#### Strictly Forbidden Capabilities:
- `DENY`: `patient:pii:view`
- `DENY`: `clinical:encounter:edit`
- `DENY`: `pharmacy:dispense`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-021-001",
  "role": "ROLE-021",
  "role_title": "State HMIS Officer",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["hmis:monthly:export", "statutory:form:generate", "national:portal:sync"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.22 Role Specification: `ROLE-022` (Bio-Medical Waste Inspector)
- **Role Code:** `ROLE-022`
- **Role Title:** Bio-Medical Waste Inspector
- **Operational Description:** State pollution control board environmental officer.
- **Data Tenancy Scope:** Facility bio-medical waste logs and color-coded bins.
- **Segregation of Duties Rule:** Waste manifests only; zero patient records.
- **Clinical & Governance Policy:** Inspects segregation of sharps, infected plastics, and anatomical waste per statutory rules.

#### Explicit Permitted Capabilities:
- `GRANT`: `bmwm:manifest:verify`
- `GRANT`: `waste:barcodes:scan`
- `GRANT`: `color_bins:inspect`
- `GRANT`: `disposal:certify`

#### Strictly Forbidden Capabilities:
- `DENY`: `patient:clinical:records`
- `DENY`: `pharmacy:records`
- `DENY`: `staff:rosters`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-022-001",
  "role": "ROLE-022",
  "role_title": "Bio-Medical Waste Inspector",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["bmwm:manifest:verify", "waste:barcodes:scan", "color_bins:inspect", "disposal:certify"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.23 Role Specification: `ROLE-023` (Hospital Pathologist)
- **Role Code:** `ROLE-023`
- **Role Title:** Hospital Pathologist
- **Operational Description:** Secondary hospital consultant reviewing complex lab investigations.
- **Data Tenancy Scope:** Referred laboratory investigations from primary clinics.
- **Segregation of Duties Rule:** Secondary laboratory diagnostics only.
- **Clinical & Governance Policy:** Provides confirmatory interpretation for peripheral blood smears, cervical pap smears, and biopsies.

#### Explicit Permitted Capabilities:
- `GRANT`: `lab:confirmatory:sign`
- `GRANT`: `histology:report:sign`
- `GRANT`: `smear:review:write`

#### Strictly Forbidden Capabilities:
- `DENY`: `primary:triage:write`
- `DENY`: `pharmacy:dispense`
- `DENY`: `system:admin`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-023-001",
  "role": "ROLE-023",
  "role_title": "Hospital Pathologist",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["lab:confirmatory:sign", "histology:report:sign", "smear:review:write"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.24 Role Specification: `ROLE-024` (Ward Committee Member)
- **Role Code:** `ROLE-024`
- **Role Title:** Ward Committee Member
- **Operational Description:** Elected citizen representative reviewing ward health facility.
- **Data Tenancy Scope:** Aggregated metrics for assigned municipal ward.
- **Segregation of Duties Rule:** Publicly disclosable anonymized metrics only.
- **Clinical & Governance Policy:** Reviews clinic footfall, patient satisfaction scores, and facility operational hours in ward meetings.

#### Explicit Permitted Capabilities:
- `GRANT`: `ward:footfall:view`
- `GRANT`: `public:kpi:inspect`
- `GRANT`: `stockout:summary:view`

#### Strictly Forbidden Capabilities:
- `DENY`: `patient:individual:records`
- `DENY`: `staff:disciplinary`
- `DENY`: `clinical:notes`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-024-001",
  "role": "ROLE-024",
  "role_title": "Ward Committee Member",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["ward:footfall:view", "public:kpi:inspect", "stockout:summary:view"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.25 Role Specification: `ROLE-025` (Nikshay TB Supervisor)
- **Role Code:** `ROLE-025`
- **Role Title:** Nikshay TB Supervisor
- **Operational Description:** National Tuberculosis Elimination Program (NTEP) supervisor.
- **Data Tenancy Scope:** Municipal tuberculosis patient cohort.
- **Segregation of Duties Rule:** TB program cohort records only.
- **Clinical & Governance Policy:** Tracks sputum test results, anti-TB medication compliance, and direct benefit transfer incentives.

#### Explicit Permitted Capabilities:
- `GRANT`: `tb:registry:manage`
- `GRANT`: `nikshay:export:trigger`
- `GRANT`: `dbt:incentive:verify`
- `GRANT`: `contact:trace:log`

#### Strictly Forbidden Capabilities:
- `DENY`: `unrelated:medical:records`
- `DENY`: `pharmacy:stock:dispense`
- `DENY`: `system:admin`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-025-001",
  "role": "ROLE-025",
  "role_title": "Nikshay TB Supervisor",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["tb:registry:manage", "nikshay:export:trigger", "dbt:incentive:verify", "contact:trace:log"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.26 Role Specification: `ROLE-026` (RCH Maternal Health Lead)
- **Role Code:** `ROLE-026`
- **Role Title:** RCH Maternal Health Lead
- **Operational Description:** Reproductive and Child Health program coordinator.
- **Data Tenancy Scope:** Maternal and child health patient registry.
- **Segregation of Duties Rule:** MCH program scope only.
- **Clinical & Governance Policy:** Monitors antenatal checkups, high-risk pregnancy alerts, and childhood immunization coverage.

#### Explicit Permitted Capabilities:
- `GRANT`: `mch:anc:manage`
- `GRANT`: `immunization:cohort:track`
- `GRANT`: `high_risk_pregnancy:flag`

#### Strictly Forbidden Capabilities:
- `DENY`: `general:adult:prescribing`
- `DENY`: `billing:vouchers`
- `DENY`: `system:admin`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-026-001",
  "role": "ROLE-026",
  "role_title": "RCH Maternal Health Lead",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["mch:anc:manage", "immunization:cohort:track", "high_risk_pregnancy:flag"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.27 Role Specification: `ROLE-027` (Billing Reconciler)
- **Role Code:** `ROLE-027`
- **Role Title:** Billing Reconciler
- **Operational Description:** Municipal accounts auditor verifying zero-cost health vouchers.
- **Data Tenancy Scope:** Financial billing voucher tokens.
- **Segregation of Duties Rule:** Zero clinical notes access; voucher tokens only.
- **Clinical & Governance Policy:** Reconciles free diagnostic and pharmacy service counts against municipal budget allocations.

#### Explicit Permitted Capabilities:
- `GRANT`: `voucher:reconcile`
- `GRANT`: `audit:claims:verify`
- `GRANT`: `finance:report:generate`

#### Strictly Forbidden Capabilities:
- `DENY`: `patient:clinical:notes`
- `DENY`: `prescription:medical:reasons`
- `DENY`: `doctor:soap`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-027-001",
  "role": "ROLE-027",
  "role_title": "Billing Reconciler",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["voucher:reconcile", "audit:claims:verify", "finance:report:generate"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.28 Role Specification: `ROLE-028` (Disaster Commander)
- **Role Code:** `ROLE-028`
- **Role Title:** Disaster Commander
- **Operational Description:** BBMP disaster management authority incident commander.
- **Data Tenancy Scope:** City-wide emergency health resources during active disaster.
- **Segregation of Duties Rule:** Disaster event scope during activation.
- **Clinical & Governance Policy:** Directs clinic staff to mass casualty response, orders emergency supplies, and diverts ambulances.

#### Explicit Permitted Capabilities:
- `GRANT`: `disaster:divert:order`
- `GRANT`: `triage:mass:override`
- `GRANT`: `facility:emergency:declare`

#### Strictly Forbidden Capabilities:
- `DENY`: `routine:outpatient:edits`
- `DENY`: `pharmacy:stock:theft`
- `DENY`: `permanent:records:delete`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-028-001",
  "role": "ROLE-028",
  "role_title": "Disaster Commander",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["disaster:divert:order", "triage:mass:override", "facility:emergency:declare"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.29 Role Specification: `ROLE-029` (Tele-Mental Health Counselor)
- **Role Code:** `ROLE-029`
- **Role Title:** Tele-Mental Health Counselor
- **Operational Description:** Tele-MANAS counselor providing mental health consultation.
- **Data Tenancy Scope:** Referred mental health tele-consultation encounters.
- **Segregation of Duties Rule:** Mental health counseling domain only.
- **Clinical & Governance Policy:** Conducts structured psychological assessments and documents supportive counseling notes.

#### Explicit Permitted Capabilities:
- `GRANT`: `telemed:counseling:write`
- `GRANT`: `phq9:evaluate`
- `GRANT`: `gad7:evaluate`
- `GRANT`: `crisis:refer:escalate`

#### Strictly Forbidden Capabilities:
- `DENY`: `pharmacy:dispense`
- `DENY`: `general:lab:order`
- `DENY`: `facility:roster`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-029-001",
  "role": "ROLE-029",
  "role_title": "Tele-Mental Health Counselor",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["telemed:counseling:write", "phq9:evaluate", "gad7:evaluate", "crisis:refer:escalate"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

### 05.30 Role Specification: `ROLE-030` (Penetration Tester)
- **Role Code:** `ROLE-030`
- **Role Title:** Penetration Tester
- **Operational Description:** Authorized security analyst conducting vulnerability testing.
- **Data Tenancy Scope:** Isolated ephemeral sandbox environment only.
- **Segregation of Duties Rule:** Synthetic test environment only; strictly zero production access.
- **Clinical & Governance Policy:** Executes penetration tests against mock data to discover and remediate security vulnerabilities.

#### Explicit Permitted Capabilities:
- `GRANT`: `security:synthetic:probe`
- `GRANT`: `api:fuzz:test`
- `GRANT`: `sandbox:evaluate`

#### Strictly Forbidden Capabilities:
- `DENY`: `production:patient:data`
- `DENY`: `live:clinical:records`
- `DENY`: `real:prescriptions`

#### Example Cryptographic JWT Claims Representation:
```json
{
  "sub": "usr-uuidv7-role-030-001",
  "role": "ROLE-030",
  "role_title": "Penetration Tester",
  "clinic_id": "BBMP-CLN-042",
  "capabilities": ["security:synthetic:probe", "api:fuzz:test", "sandbox:evaluate"],
  "iss": "https://auth.namma.bbmp.gov.in",
  "exp": 1788502500
}
```

---

## 06. Network Architecture, Micro-Segmentation & Firewalls
Multi-tiered network security topology protecting data across transit boundaries:
1. **Cloud Virtual Private Cloud (VPC) Topology:**
   - **Public Ingress Subnet (AZ A/B/C):** Cloudflare CDN / WAF -> Envoy API Gateway (TLS Termination, Rate Limiting).
   - **DMZ Subnet:** ABDM Bridge, KDLWS EDI Gateway, SMS Gateway Webhooks. Strict egress proxies.
   - **Application Tier Subnet (Private):** Kubernetes Worker Nodes hosting Modular Monolith containers. Zero direct internet ingress.
   - **Database Tier Subnet (Isolated):** PostgreSQL 16 Primary and Replicas, Redis Cluster, ClickHouse. Ingress strictly permitted from Application Subnet via port 5432 / 6379 / 9000.
   - **Security Subnet (Air-Gapped / Isolated):** HashiCorp Vault and Cryptographic WORM Audit Store.
2. **Clinic Local Area Network (LAN) Topology:**
   - **VLAN 10 (Medical Operations LAN):** Doctor laptops, nurse tablets, edge mini-server, thermal receipt printers, 2D barcode scanners. Static DHCP with MAC address filtering.
   - **VLAN 20 (Public / Waiting Hall):** Citizen Wi-Fi (when available), waiting hall TV screen display. Strictly isolated from VLAN 10 via firewall rules; zero access to edge mini-server port 8443.

## 07. DPDP Act 2023 Statutory Compliance & Privacy Architecture
Mechanisms enforcing India's Digital Personal Data Protection Act (DPDP Act 2023):
1. **Affirmative Bilingual Consent:** Captured via Kannada and English digital consent artifact prior to health data processing.
2. **Right to Correction & Grievance:** Citizens can submit demographic correction requests and lodge grievances through municipal kiosks.
3. **Automated PII Sanitization in Logs:** Middleware filters strip Aadhaar numbers (UIDAI regular expression), phone numbers, and patient names before sending logs to OpenTelemetry / ElasticSearch collectors.
4. **Data Fiduciary Audit Trail:** Every access to an individual citizen's health record generates an immutable access log accessible to the Data Protection Officer (`ROLE-020`).

## 08. CERT-In Incident Response & Forensic Runbook
Step-by-step incident response playbook complying with statutory 6-hour reporting mandates:
1. **T0 (0-15 Minutes) - Automated Detection & Alerting:** SIEM alerts trigger PagerDuty incident for SRE on-call upon detection of brute-force anomalies, database dump attempts, or WORM hash mismatches.
2. **T1 (15-45 Minutes) - Containment & Isolation:** Revoke compromised JWT sessions via Redis distributed blacklist; isolate affected edge mini-server or container pod via network security group quarantine.
3. **T2 (45-120 Minutes) - Forensic Triage & Evidence Preservation:** Capture cryptographic disk snapshots and memory dumps of quarantined nodes; seal audit trail.
4. **T3 (120-240 Minutes) - Remediation & System Recovery:** Deploy security patches or rotate compromised certificates; restore clean state from verified immutable backups.
5. **T4 (Within 360 Minutes / 6 Hours) - Statutory CERT-In Notification:** Chief Information Security Officer (CISO) submits formal Incident Report Form to incident@cert-in.org.in detailing attack vector, impact scope, and remediation actions.
