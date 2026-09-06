"""
gen_sec_15_threats.py
Generator for docs/10-security/15-threat-model.md
Produces >= 2,000 substantive lines detailing enterprise STRIDE threat model.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.security.security_gen_common import write_sec_doc, format_threat, make_sec_bdd_scenario
from scripts.security.security_core_data import THREAT_RECORDS

def generate_doc():
    lines = []
    lines.append("# Enterprise STRIDE Threat Model & Attack Tree Register")
    lines.append("## Namma Clinic Digital Health & Operations Platform")
    lines.append("### Greater Bengaluru Authority (GBA) / BBMP Health Department")
    lines.append("**Standard:** Microsoft STRIDE / NIST SP 800-30 / OWASP Threat Modeling | **Status:** APPROVED BASELINE | **Code:** `SEC-DOC-15`")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Threat Modeling Methodology & System Attack Surface")
    lines.append("The Namma Clinic Threat Model provides a systematic evaluation of adversaries, attack paths, entry points, and vulnerability vectors across all 18 platform containers (`ARCH-CONT-001` through `ARCH-CONT-018`). Applying the **STRIDE** methodology (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege), the threat model evaluates risks unique to primary healthcare delivery in urban Bengaluru.")
    lines.append("")
    lines.append("### 1.1 Threat Actor Profiles")
    lines.append("1. **Curious / Malicious Insider:** Healthcare staff attempting unauthorized snooping into neighbors', family members', or VIPs' clinical records.")
    lines.append("2. **Opportunistic Physical Intruder:** Thief burglarizing clinic premises after operating hours to steal mini-PCs or thermal printers.")
    lines.append("3. **External Cybercrime Syndicate:** Financially motivated adversaries attempting ransomware deployment, extortion, or darknet health record exfiltration.")
    lines.append("4. **Disgruntled Administrative Personnel:** Staff member attempting inventory manipulation, medication diversion, or audit log tampering.")
    lines.append("5. **Automated Credential Stuffing Botnets:** Internet-wide automated scripts targeting public API gateway login endpoints.")
    lines.append("")
    lines.append("### 1.2 STRIDE Threat Surface Diagram")
    lines.append("```mermaid")
    lines.append("flowchart TD")
    lines.append("    subgraph Attackers [Threat Actors]")
    lines.append("        Ext[External Cyber Attacker] -->|DDoS / Injection / BOLA| WAF[Cloud Ingress]")
    lines.append("        Ins[Malicious Insider Staff] -->|Snooping / Rx Fraud| PWA[Clinic Terminal]")
    lines.append("        Burg[Physical Intruder] -->|Hardware Theft| MiniPC[Mini-PC Hardware]")
    lines.append("    end")
    lines.append("    subgraph STRIDE [STRIDE Threat Categories]")
    lines.append("        WAF --> S[Spoofing: Identity Forgery]")
    lines.append("        WAF --> T[Tampering: Prescription & Log Alteration]")
    lines.append("        PWA --> R[Repudiation: Action Denial]")
    lines.append("        PWA --> I[Information Disclosure: PII/PHI Exfiltration]")
    lines.append("        MiniPC --> D[Denial of Service: Subnet Ransomware]")
    lines.append("        MiniPC --> E[Elevation of Privilege: Admin Takeover]")
    lines.append("    end")
    lines.append("    subgraph Defense [Defensive Countermeasures]")
    lines.append("        S --> mTLS[mTLS, Argon2id, WebAuthn]")
    lines.append("        T --> HashChain[SHA-256 Hash Chain & HMAC]")
    lines.append("        R --> WORM[Immutable S3 Object Lock]")
    lines.append("        I --> AES[AES-256-GCM & Field Encryption]")
    lines.append("        D --> Offline[Autonomous Offline Mode & Restore]")
    lines.append("        E --> RBAC[Dual-Engine RBAC & ABAC]")
    lines.append("    end")
    lines.append("```")
    lines.append("")

    # Add all 100 Threat Records
    lines.append("## 2. Authoritative Threat Register (THREAT-001 to THREAT-100)")
    lines.append("The following 100 records provide the comprehensive threat model for the Namma Clinic Platform:")
    lines.append("")
    for t in THREAT_RECORDS:
        lines.extend(format_threat(t))

    # Add BDD scenarios
    lines.append("## 3. Threat Mitigation Verification Scenarios (BDD Acceptance)")
    lines.append("The following scenarios specify automated acceptance tests verifying threat mitigations:")
    lines.append("")
    for i in range(1, 21):
        lines.extend(make_sec_bdd_scenario(
            f"THREAT-SCENARIO-{i:03d}: Verification of Resistance Against {THREAT_RECORDS[((i-1)%len(THREAT_RECORDS))]['title']}",
            [
                f"An adversary attempts exploitation vector described in THREAT-{((i-1)%100)+1:03d}",
                f"The target asset is {THREAT_RECORDS[((i-1)%len(THREAT_RECORDS))]['asset']}",
                f"Defensive controls {THREAT_RECORDS[((i-1)%len(THREAT_RECORDS))]['preventive_controls']} are active"
            ],
            f"The adversary executes attack path variant {i}",
            [
                "The defensive barrier intercepts attack and prevents unauthorized state change",
                "The anomaly is detected by SIEM and logged to the immutable audit trail",
                "Residual risk remains within approved low threshold"
            ]
        ))

    return write_sec_doc("15-threat-model.md", "\n".join(lines), min_substantive=2000)

if __name__ == "__main__":
    generate_doc()
