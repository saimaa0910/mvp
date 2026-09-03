# ⚡ Non-Functional Requirements Specification
## Namma Clinic Digital Health & Operations Platform
**Document Code:** REQ-NFR-03 | **Status:** Approved Baseline | **Date:** September 2026

---

### 1. System Quality Attributes & SLA Thresholds

| ID | Title | Specification & Threshold | Priority | Verification Method | Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| NFR-001 | Sub-Second Latency | API p95 latency < 300ms under standard clinic concurrency (50 requests/sec). | Critical | Load Testing with k6 | TD-ARC-01 |
| NFR-002 | High Availability | 99.9% uptime during operational clinic hours (08:00 to 20:00 IST Monday-Saturday). | Critical | Synthetic Uptime Monitors | TD-OPS-04 |
| NFR-003 | Offline Resilience | Complete offline operation capability for 8+ hours with zero browser crash. | Critical | Chaos Browser Disconnect | TD-ARC-01 |
| NFR-004 | Data Integrity | Zero data loss (RPO = 0) during network partition or abrupt client shutdown. | Critical | Transactional Flush Test | TD-DB-03 |
| NFR-005 | Concurrent Clinic Scale | Support 183 concurrent clinics with peak 500 active staff sessions without degradation. | High | Distributed Stress Test | DPR Sec 6 |
| NFR-006 | Low Bandwidth Optimization | Initial app load < 2MB; subsequent REST payload size < 15KB compressed. | High | Bundle Analyzer & Chrome DevTools | TD-ARC-01 |
| NFR-007 | Accessibility (WCAG) | Comply with WCAG 2.1 Level AA for all doctor, nurse, and citizen interfaces. | Medium | Axe Accessibility Scanner | UM-BIL-01 |
| NFR-008 | Disaster Recovery (RTO) | Recovery Time Objective < 60 minutes in the event of primary AZ cloud failure. | High | Multi-AZ RDS Failover Drill | TD-OPS-04 |
