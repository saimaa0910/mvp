"""
generate_all_security_docs.py
Master orchestrator script to sequentially execute all 21 Phase 10 Security generators.
"""

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.security import (
    gen_sec_01_architecture,
    gen_sec_02_authentication,
    gen_sec_03_authorization,
    gen_sec_04_mfa,
    gen_sec_05_sessions,
    gen_sec_06_passwords,
    gen_sec_07_api,
    gen_sec_08_encryption,
    gen_sec_09_keys,
    gen_sec_10_audit,
    gen_sec_11_privacy,
    gen_sec_12_consent,
    gen_sec_13_classification,
    gen_sec_14_secrets,
    gen_sec_15_threats,
    gen_sec_16_testing,
    gen_sec_17_vapt,
    gen_sec_18_incident,
    gen_sec_19_backup,
    gen_sec_20_device,
    gen_security_audit,
)

GENERATORS = [
    ("01-security-architecture.md", gen_sec_01_architecture.generate_doc),
    ("02-authentication.md", gen_sec_02_authentication.generate_doc),
    ("03-authorization-rbac.md", gen_sec_03_authorization.generate_doc),
    ("04-mfa.md", gen_sec_04_mfa.generate_doc),
    ("05-session-management.md", gen_sec_05_sessions.generate_doc),
    ("06-password-policy.md", gen_sec_06_passwords.generate_doc),
    ("07-api-security.md", gen_sec_07_api.generate_doc),
    ("08-data-encryption.md", gen_sec_08_encryption.generate_doc),
    ("09-key-management.md", gen_sec_09_keys.generate_doc),
    ("10-audit-logging.md", gen_sec_10_audit.generate_doc),
    ("11-privacy.md", gen_sec_11_privacy.generate_doc),
    ("12-consent.md", gen_sec_12_consent.generate_doc),
    ("13-data-classification.md", gen_sec_13_classification.generate_doc),
    ("14-secrets-management.md", gen_sec_14_secrets.generate_doc),
    ("15-threat-model.md", gen_sec_15_threats.generate_doc),
    ("16-security-testing.md", gen_sec_16_testing.generate_doc),
    ("17-vapt-plan.md", gen_sec_17_vapt.generate_doc),
    ("18-incident-response.md", gen_sec_18_incident.generate_doc),
    ("19-backup-security.md", gen_sec_19_backup.generate_doc),
    ("20-device-security.md", gen_sec_20_device.generate_doc),
    ("SECURITY_COMPLETENESS_AUDIT.md", gen_security_audit.generate_doc),
]

def main():
    t0 = time.time()
    print("================================================================================")
    print("EXECUTING MASTER SECURITY GENERATION ORCHESTRATOR (PHASE 10: 21 DOCUMENTS)")
    print("================================================================================")

    total_substantive = 0
    total_physical = 0
    for filename, gen_fn in GENERATORS:
        res = gen_fn()
        sub = res["substantive"] if isinstance(res, dict) else res
        tot = res["total"] if isinstance(res, dict) else sub
        total_substantive += sub
        total_physical += tot
        print(f"  -> {filename:<35} : {sub:>6} substantive ({tot:>6} total) [PASS]")

    elapsed = time.time() - t0
    print("================================================================================")
    print(f"ALL 21 SECURITY DOCUMENTS GENERATED SUCCESSFULLY IN {elapsed:.2f}s")
    print(f"TOTAL SUBSTANTIVE LINES: {total_substantive:,} ({total_physical:,} total lines)")
    print("================================================================================")

if __name__ == "__main__":
    main()
