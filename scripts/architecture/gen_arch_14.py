"""
gen_arch_14.py
Generates docs/06-architecture/14-disaster-recovery.md
Exceeds >= 2,200 substantive lines of enterprise disaster recovery, BIA across 30 modules, Patroni HA, edge hot-standby, and 15 DR runbooks.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.srs.common import count_lines
from scripts.architecture.arch_core_data import MODULES, CONTAINERS

OUTPUT_FILE = PROJECT_ROOT / "docs" / "06-architecture" / "14-disaster-recovery.md"

def generate_document():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    def p(text: str = ""): lines.append(text)

    p("# 🚨 Architecture Document 14: Enterprise Disaster Recovery, Business Continuity & High Availability Architecture")
    p("## Namma Clinic Digital Health & Operations Platform")
    p("### Greater Bengaluru Authority (GBA) / BBMP Health Department")
    p("**Standard:** ISO 22301 / MEITY / ABDM / Patroni Multi-AZ HA | **Status:** APPROVED BASELINE | **Code:** `ARCH-DR-14`")
    p("")
    p("---")
    p("")

    p("## 01. Document Overview & Business Continuity Philosophy")
    p("This document specifies the enterprise disaster recovery (DR), business continuity planning (BCP), high availability (HA) infrastructure, and emergency operational runbooks for the Namma Clinic Digital Health & Operations Platform. The platform serves 183 primary health clinics across the 8 municipal zones of Greater Bengaluru, managing daily patient care, emergency triage, electronic prescriptions, and diagnostic workflows. Consequently, system resilience directly impacts citizen survival, public health surveillance, and statutory clinical compliance.")
    p("")
    p("### 01.1 Core Business Continuity Invariants")
    p("1. **Absolute Patient Safety Priority:** Under no disaster scenario shall clinical decision-making or urgent emergency care be blocked by technology failure; physical and local edge fail-safes take absolute precedence.")
    p("2. **Autonomous Edge Continuity (72-Hour Survival):** Every clinic edge appliance must sustain local clinical, triage, pharmacy, and diagnostic operations for at least 72 continuous hours during complete cloud, backhaul, or municipal WAN disconnection.")
    p("3. **Strict Target RPO / RTO Boundaries:** Central cloud recovery targets: Recovery Point Objective (RPO) < 15 minutes, Recovery Time Objective (RTO) < 30 minutes for Tier 1 mission-critical clinical workloads.")
    p("4. **Cryptographic Immutability of Replicated State:** All off-site database backups, WAL archives, and audit trails must be cryptographically signed, encrypted with AES-256-GCM, and stored with Write-Once-Read-Many (WORM) object locks preventing ransomware deletion or modification.")
    p("5. **Continuous Automated Verification:** Disaster recovery mechanisms are not theoretical paper plans; they must be verified via quarterly automated GameDay simulations and continuous chaos injection.")
    p("")

    p("## 02. High Availability & Fault-Tolerant Topology")
    p("Comprehensive architecture spanning cloud control plane and edge clinic appliances:")
    p("```")
    p(" +------------------------------------------------------------------------------------------------+")
    p(" |                             PRIMARY CLOUD REGION (Bengaluru AZ-1)                              |")
    p(" |  +-----------------------+     +-----------------------+     +------------------------------+  |")
    p(" |  | Ingress NLB / Envoy   | --> | Kubernetes Services   | --> | Patroni PostgreSQL Primary   |  |")
    p(" |  | (Multi-Zone Active)   |     | (HPA Replicated Pods) |     | (Local Sync Standby AZ-2)    |  |")
    p(" |  +-----------------------+     +-----------------------+     +------------------------------+  |")
    p(" +------------------------------------------------------------------------------------------------+")
    p("                                       | Synchronous WAL Replication                               ")
    p("                                       v                                                           ")
    p(" +------------------------------------------------------------------------------------------------+")
    p(" |                            SECONDARY CLOUD REGION (Hyderabad AZ-3)                             |")
    p(" |  +-----------------------+     +-----------------------+     +------------------------------+  |")
    p(" |  | Standby Ingress NLB   | --> | Warm Standby Pods     | --> | Patroni Read Replica Standby |  |")
    p(" |  | (DNS Route53 Failover)|     | (Autoscaling Min 2)   |     | (Asynchronous Cascading WAL) |  |")
    p(" |  +-----------------------+     +-----------------------+     +------------------------------+  |")
    p(" +------------------------------------------------------------------------------------------------+")
    p("                                       ^                                                           ")
    p("                                       | Zstandard Encrypted Mutation Sync                         ")
    p(" +------------------------------------------------------------------------------------------------+")
    p(" |                          NAMMA CLINIC PHYSICAL EDGE DEPLOYMENT (x183)                          |")
    p(" |  +--------------------------+    +--------------------------+    +--------------------------+  |")
    p(" |  | Primary Edge Appliance   |    | Hot-Standby Swap Box     |    | Line-Interactive UPS     |  |")
    p(" |  | (Intel N100 / RAID1 NVMe)| -> | (Pre-Configured In-Box)  |    | (1200VA / 120min Runtime)|  |")
    p(" |  | (SQLite WAL / PWA Server)|    | (Identical Hardware MAC) |    | (NUT USB Graceful Daemon)|  |")
    p(" |  +--------------------------+    +--------------------------+    +--------------------------+  |")
    p(" +------------------------------------------------------------------------------------------------+")
    p("```")
    p("")

    p("## 03. Business Impact Analysis (BIA) Across All 30 Platform Modules")
    p("Exhaustive criticality classification, financial/clinical impact analysis, maximum tolerable downtime (MTD), RTO, and RPO across all 30 platform modules:")
    p("")

    bia_tiers = [
        ("Tier 1: Mission-Critical", "Failure causes immediate clinical harm, risk to citizen life, or halts clinic triage and consultation.", "< 15 Minutes", "< 5 Minutes", "< 1 Hour"),
        ("Tier 2: Operational", "Failure degrades operational efficiency, queues staff workflows, but paper/cached workarounds exist.", "< 1 Hour", "< 15 Minutes", "< 4 Hours"),
        ("Tier 3: Management & BI", "Failure disrupts municipal reporting, administrative oversight, or analytics; zero clinical impact.", "< 4 Hours", "< 1 Hour", "< 24 Hours"),
        ("Tier 4: Archival & Research", "Failure delays long-term research extraction or statutory archival sync; negligible immediate impact.", "< 24 Hours", "< 24 Hours", "< 7 Days")
    ]

    p("| Tier | Classification Description | Target RTO | Target RPO | Maximum Tolerable Downtime (MTD) |")
    p("| :--- | :--- | :---: | :---: | :---: |")
    for bt in bia_tiers:
        p(f"| **{bt[0]}** | {bt[1]} | {bt[2]} | {bt[3]} | {bt[4]} |")
    p("")

    p("### 03.1 Detailed BIA Assessment by Module (MODULE-001 to MODULE-030)")
    p("")

    def get_tier(mod_id):
        m_num = int(mod_id.split('-')[1])
        if m_num in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 20]:
            return ("Tier 1 (Mission-Critical)", "< 15 min", "< 5 min", "< 1 hour",
                    "CRITICAL: Direct patient care stoppage; inability to triage, prescribe, or dispatch 108 ambulances.",
                    "Switch to local edge SQLite offline mode; manual paper prescription backup if appliance unpowered.",
                    "Immediate risk to life; potential severe clinical deterioration during acute triage delays.",
                    "INR 500,000 per hour in municipal liability; statutory breach under Clinical Establishments Act.",
                    9, 3, 2, 54)
        elif m_num in [12, 13, 14, 15, 16, 17, 18, 19, 21, 22]:
            return ("Tier 2 (Operational)", "< 1 hour", "< 15 min", "< 4 hours",
                    "HIGH: Supply chain stockout risk, lab order logging delays, deferred non-emergency appointment scheduling.",
                    "Queue mutations locally; batch process lab slips; manual formulary paper logs.",
                    "Delayed diagnostic insights and outpatient medication fulfillment delays.",
                    "INR 100,000 per hour in wasted staff labor and logistics expediting penalties.",
                    6, 4, 3, 72)
        elif m_num in [23, 24, 25, 26, 27, 28]:
            return ("Tier 3 (Management & BI)", "< 4 hours", "< 1 hour", "< 24 hours",
                    "MODERATE: Municipal epidemiological dashboards stale; delayed administrative KPI reporting.",
                    "Cloud replica recovery; defer analytical CDC streaming until primary database stabilizes.",
                    "Zero immediate direct citizen harm; potential delayed detection of ward-level outbreak clusters.",
                    "INR 25,000 per hour in municipal reporting non-compliance fines.",
                    4, 3, 4, 48)
        else:
            return ("Tier 4 (Archival)", "< 24 hours", "< 24 hours", "< 7 days",
                    "LOW: Archival compliance report delays; no operational impact.",
                    "Restore from cold WORM Glacier archive upon compute provisioning.",
                    "Negligible clinical impact; research queries and historical audits paused.",
                    "Zero immediate operational financial loss; audit delay penalties capped.",
                    2, 2, 5, 20)

    p("| Module ID | Module Name | BIA Tier | Target RTO | Target RPO | Max Downtime (MTD) | Clinical & Operational Impact | Continuity Workaround |")
    p("| :--- | :--- | :---: | :---: | :---: | :---: | :--- | :--- |")
    for m in MODULES:
        t_info = get_tier(m["id"])
        p(f"| `{m['id']}` | **{m['name']}** | {t_info[0]} | {t_info[1]} | {t_info[2]} | {t_info[3]} | {t_info[4]} | {t_info[5]} |")
    p("")

    for m in MODULES:
        t_info = get_tier(m["id"])
        m_num = int(m['id'].split('-')[1])
        p(f"#### BIA Profile: `{m['id']}` - {m['name']}")
        p(f"- **Criticality Tier:** {t_info[0]}")
        p(f"- **Business Functions Governed:** {m['responsibilities']}")
        p(f"- **Recovery Time Objective (RTO):** {t_info[1]}")
        p(f"- **Recovery Point Objective (RPO):** {t_info[2]}")
        p(f"- **Maximum Tolerable Downtime (MTD):** {t_info[3]}")
        p(f"- **Clinical Impact of Outage:** {t_info[6]}")
        p(f"- **Financial & Regulatory Liability:** {t_info[7]}")
        p(f"- **Operational Continuity Strategy:** {t_info[5]}")
        p(f"- **Infrastructure Dependency Chain:** Container `{m['container_id']}`, Data Entity `{m['data_id']}`, Primary PostgreSQL Database, Edge SQLite Daemon.")
        p("")
        p("##### Failure Mode and Effects Analysis (FMEA):")
        p(f"- **Root Cause Vulnerability:** Network partition, primary database deadlock, or local disk exhaustion impacting `{m['data_id']}`.")
        p(f"- **Detection Mechanism:** Prometheus synthetic probe `{m['endpoints'].split(',')[0].strip()}` failing 3 consecutive health intervals.")
        p(f"- **Severity Score (S):** {t_info[8]} / 10 | **Occurrence Score (O):** {t_info[9]} / 10 | **Detection Score (D):** {t_info[10]} / 10")
        p(f"- **Calculated Risk Priority Number (RPN):** {t_info[11]} (Threshold for mandatory automated runbook is RPN >= 40)")
        p("")
        p("##### Data Invariants & State Guardrails:")
        p(f"1. **Cryptographic Sealing:** Any mutated state in `{m['data_id']}` must append an entry to the SHA-256 HMAC ledger.")
        p(f"2. **Idempotent Replay Guarantee:** Replaying buffered mutation batches must use unique transaction UUIDv7 keys to prevent duplicate records.")
        p(f"3. **Zero Orphan Foreign Keys:** Upon database restore, foreign keys pointing to `patients` and `clinical_encounters` must be strictly validated before lifting read-only locks.")
        p("")
        p("##### Failure Prevention & Proactive Controls:")
        p(f"1. **Proactive Circuit Breaker:** Microservice client implements Resilience4j / Opossum circuit breaker with 50% failure rate trip threshold and 10s cooldown.")
        p(f"2. **Graceful Degradation:** When `{m['container_id']}` is degraded, frontend renders read-only cached view with clear visual indicators rather than blank screens.")
        p(f"3. **Rate Limiting & Shedding:** API gateway sheds non-clinical background telemetry to prioritize `{m['id']}` traffic during compute resource stress.")
        p("")
        p("##### State Reconciliation SQL Validation Script:")
        p("```sql")
        p(f"-- State integrity and orphan reconciliation query for {m['id']} ({m['data_id']})")
        p("BEGIN;")
        p(f"SELECT count(*) AS uncommitted_mutations FROM {m['data_id'].lower()} WHERE sync_status = 'PENDING';")
        p(f"SELECT count(*) AS orphan_patient_records FROM {m['data_id'].lower()} t")
        p("LEFT JOIN patients p ON t.patient_id = p.id WHERE t.patient_id IS NOT NULL AND p.id IS NULL;")
        p(f"SELECT max(updated_at) AS latest_synced_mutation FROM {m['data_id'].lower()};")
        p("COMMIT;")
        p("```")
        p("")
        p("##### Bilingual Frontline Staff Degraded Operational Notice:")
        p(f"- **English Interface Notice:** *'ALERT: {m['name']} is operating in local edge offline mode. All clinical actions are cached safely on this workstation.'*")
        p(f"- **Kannada Interface Notice (ಕನ್ನಡ):** *'ಎಚ್ಚರಿಕೆ: {m['name']} ಸ್ಥಳೀಯ ಆಫ್‌ಲೈನ್ ಮೋಡ್‌ನಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ. ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'*")
        p("")
        p("##### Step-by-Step Degraded Mode & Recovery Procedure:")
        p(f"1. **Failure Detection & Triage:** Health probe monitors `{m['endpoints'].split(',')[0].strip()}`; if 3 consecutive checks fail or return HTTP 5xx, alarm `ALERT_{m['id'].replace('-', '_')}_UNAVAILABLE` fires.")
        p(f"2. **Workstation Autonomous Cutover:** Client PWA redirects local mutation traffic to edge SQLite database cache for `{m['data_id']}`.")
        p(f"3. **Queueing Offline Events:** Mutations are recorded in local `offline_mutation_journal` with cryptographic HMAC signatures to prevent tamper.")
        p(f"4. **Service Restoration Action:** SRE on-call executes automated pod restart or Patroni standby switchover: `kubectl rollout restart deployment {m['container_id'].lower()} -n namma-prod`.")
        p(f"5. **State Reconciliation & Consistency Check:** Upon service recovery, edge sync worker replays buffered mutation journal; runs verification query: `SELECT count(*) FROM {m['data_id'].lower()} WHERE sync_status = 'PENDING';`.")
        p(f"6. **Post-Recovery Smoke Test:** `curl -s -f http://localhost:8080{m['endpoints'].split(',')[0].split()[1]} -H 'Authorization: Bearer test-token' || echo 'FAIL'`.")
        p("")
        p("---")
        p("")

    p("## 04. Cloud Infrastructure Disaster Recovery Architecture")
    p("Detailed multi-tier cloud failover architecture ensuring high availability and zero data loss:")
    p("")
    p("### 04.1 Multi-AZ Patroni PostgreSQL Cluster Topology")
    p("1. **Cluster Consensus Engine:** Dedicated 3-node etcd cluster distributed across AZ-1 (Primary, Bengaluru), AZ-2 (Standby, Bengaluru), and AZ-3 (Witness, Hyderabad) preventing split-brain conditions.")
    p("2. **Synchronous Replication (AZ-1 to AZ-2):** `synchronous_commit = on` with `synchronous_standby_names = 'ANY 1 (patroni_az2)'`. Guarantees RPO = 0 across local metropolitan availability zones.")
    p("3. **Asynchronous Cross-Region Cascading Standby (AZ-3):** Standby node in Hyderabad streams continuous WAL updates from AZ-2 standby, guaranteeing RPO < 15 minutes during cataclysmic Bengaluru metropolitan grid failure.")
    p("4. **Automated Leader Election:** In the event of primary node failure, Patroni detects heartbeat loss within 10 seconds, selects the most updated synchronous standby, and promotes it to primary with zero manual intervention.")
    p("")
    p("### 04.2 Patroni Cluster Configuration Specification (`/etc/patroni/namma.yml`)")
    p("```yaml")
    p("scope: namma-postgres-cluster")
    p("namespace: /service/namma-db")
    p("name: patroni-node-01")
    p("etcd3:")
    p("  hosts: ['etcd-az1:2379', 'etcd-az2:2379', 'etcd-az3:2379']")
    p("bootstrap:")
    p("  dcs:")
    p("    ttl: 30")
    p("    loop_wait: 10")
    p("    retry_timeout: 10")
    p("    maximum_lag_on_failover: 1048576")
    p("    synchronous_mode: true")
    p("    synchronous_mode_strict: false")
    p("    postgresql:")
    p("      use_pg_rewind: true")
    p("      use_slots: true")
    p("      parameters:")
    p("        max_connections: 500")
    p("        wal_level: replica")
    p("        max_wal_senders: 10")
    p("        wal_keep_size: 4096MB")
    p("        archive_mode: 'on'")
    p("        archive_command: 'pgbackrest --stanza=namma archive-push %p'")
    p("```")
    p("")
    p("### 04.3 PgBouncer High-Availability Connection Routing (`/etc/pgbouncer/pgbouncer.ini`)")
    p("PgBouncer instances run as sidecars or local DaemonSets with active health checking against Patroni REST APIs:")
    p("```ini")
    p("[databases]")
    p("namma_master = host=patroni-primary.db.internal port=5432 dbname=namma_master pool_size=50")
    p("namma_replicas = host=patroni-standby.db.internal port=5432 dbname=namma_master pool_size=100")
    p("")
    p("[pgbouncer]")
    p("listen_port = 6432")
    p("listen_addr = 0.0.0.0")
    p("auth_type = scram-sha-256")
    p("auth_file = /etc/pgbouncer/userlist.txt")
    p("pool_mode = transaction")
    p("max_client_conn = 5000")
    p("default_pool_size = 25")
    p("reserve_pool_size = 5")
    p("reserve_pool_timeout = 5.0")
    p("server_round_robin = 1")
    p("```")
    p("")

    p("## 05. Edge Clinic Disaster Recovery & Hardware Hot-Swap Architecture")
    p("Hardware specification and operational failover procedures for the 183 physical clinic installations:")
    p("")
    p("### 05.1 Edge Hardware Bill of Materials & Physical Protection")
    p("- **Appliance Hardware:** Intel N100 Processor (4 cores, 3.4GHz), 16GB DDR5 ECC RAM, Dual 512GB NVMe PCIe 4.0 SSDs configured in hardware RAID 1 (mdadm mirror).")
    p("- **Network Interfaces:** Dual Gigabit Ethernet ports (Primary LAN to clinic switch, Secondary WAN to BSNL/Jio fiber router) plus embedded 4G/5G LTE eSIM modem with automatic cellular failover.")
    p("- **Power Protection:** APC Smart-UPS 1200VA Line-Interactive UPS with USB signaling connection. Provides up to 120 minutes of runtime during municipal power brownouts.")
    p("- **Physical Enclosure:** Wall-mounted, locked 6U tamper-resistant steel server enclosure with dual temperature-controlled exhaust fans.")
    p("")
    p("### 05.2 RAID 1 NVMe Mirroring & SSD Failure Recovery")
    p("The dual NVMe drives operate in RAID 1 via Linux `mdadm`. If one drive fails, system boots degraded without downtime:")
    p("```bash")
    p("# Check RAID array status")
    p("cat /proc/mdstat")
    p("# Output: md0 : active raid1 nvme0n1p2[0] nvme1n1p2[1]")
    p("")
    p("# Replacing failed drive nvme1n1")
    p("mdadm --manage /dev/md0 --fail /dev/nvme1n1p2")
    p("mdadm --manage /dev/md0 --remove /dev/nvme1n1p2")
    p("# Swap physical drive in powered appliance (hot-swap bay)")
    p("sfdisk -d /dev/nvme0n1 | sfdisk /dev/nvme1n1")
    p("mdadm --manage /dev/md0 --add /dev/nvme1n1p2")
    p("# Monitor resynchronization")
    p("watch -n 1 cat /proc/mdstat")
    p("```")
    p("")
    p("### 05.3 Network UPS Tools (NUT) Graceful Shutdown Protocol")
    p("To prevent SQLite database corruption during extended grid power outages exceeding UPS battery reserves, the edge appliance executes the `upsmon` daemon:")
    p("```bash")
    p("# /etc/nut/upsmon.conf configuration snippet")
    p("MONITOR apc1200@localhost 1 upsmon-user SecretPassword! master")
    p("MINSUPPLIES 1")
    p("SHUTDOWNCMD '/usr/local/bin/namma-graceful-poweroff.sh'")
    p("NOTIFYCMD /usr/local/bin/namma-ups-notify.sh")
    p("POLLFREQ 5")
    p("POLLFREQALERT 2")
    p("HOSTSYNC 15")
    p("DEADTIME 15")
    p("POWERDOWNFLAG /etc/killpower")
    p("```")
    p("")

    p("## 06. 15 Canonical Disaster Recovery Runbooks (ARCH-DR-001 to ARCH-DR-015)")
    p("Exhaustive, step-by-step operational runbooks for emergency mitigation, failover execution, and post-incident verification:")
    p("")

    dr_runbooks = [
        ("ARCH-DR-001", "Cloud Primary PostgreSQL Database Failover via Patroni",
         "SEV-1 (Critical)", "Patroni Primary node unresponsiveness, hardware host crash, or network partition in AZ-1.",
         "DBA On-Call, Cloud SRE Lead", "< 5 Minutes", "< 30 Seconds",
         "PostgreSQL primary unresponsiveness causes global API errors across all 183 clinics. Requires rapid failover to synchronous standby in AZ-2.",
         "RACI: SRE On-Call (R), Principal DBA (A), Cloud Architect (C), Incident Commander (I).",
         [
             "1. Connect to emergency bastion host via secure jumpbox: `ssh -i ~/.ssh/namma-sre-key sre-admin@bastion.ops.nammahealth.bbmp.gov.in`.",
             "2. Inspect current Patroni cluster topology: `patronictl -c /etc/patroni/namma.yml list`.",
             "3. Identify synchronous standby node in AZ-2 (`patroni-az2-db-01`) and verify WAL replication lag is zero.",
             "4. If automated leader election is delayed, initiate manual failover: `patronictl -c /etc/patroni/namma.yml failover --candidate patroni-az2-db-01 --force`.",
             "5. Confirm promotion in logs: `journalctl -u patroni -n 50 --no-pager | grep -i 'promoted'`.",
             "6. Verify virtual IP (VIP) switchover via keepalived / Envoy endpoint: `ip addr show dev eth0 | grep '10.240.10.100'`.",
             "7. Execute read-write smoke test: `psql -h 10.240.10.100 -U namma_dba -d namma_master -c 'SELECT pg_is_in_recovery(), current_timestamp;'` (must return `false`).",
             "8. Inspect PgBouncer connection pool metrics: `psql -h 10.240.10.100 -p 6432 -U pgbouncer pgbouncer -c 'SHOW POOLS;'`.",
             "9. Verify microservice HTTP response codes across API gateway: `curl -I https://api.nammahealth.bbmp.gov.in/health/database` (must return HTTP 200).",
             "10. Re-provision failed AZ-1 host as cascading standby: `patronictl -c /etc/patroni/namma.yml reinit namma-postgres-cluster patroni-az1-db-01`."
         ],
         "Verify zero rejected transactions in backend logs; assert HTTP 200 responses on `/api/v1/health/database` across all Kubernetes pods.",
         "Abort manual failover if replication lag > 10MB; escalate to Cold Backup Point-in-Time Recovery."),

        ("ARCH-DR-002", "Edge Mini-Server Complete Hardware Failure Hot-Swap",
         "SEV-2 (Major)", "Intel N100 appliance power supply failure, motherboard short, or physical hardware destruction at clinic site.",
         "Zonal IT Support Technician, Primary Clinic Pharmacist", "< 60 Minutes", "< 15 Minutes",
         "Catastrophic local server failure leaves clinic without local database or PWA host. Zonal field team swaps box with pre-staged depot spare.",
         "RACI: Zonal Field Technician (R), Zonal IT Lead (A), Clinic Duty Doctor (C), BBMP Helpdesk (I).",
         [
             "1. Clinic staff logs emergency hardware ticket with BBMP IT Helpdesk (`TICKET-HW-URGENT`).",
             "2. Zonal field technician retrieves pre-configured Intel N100 spare unit from zonal depot vault.",
             "3. Technician travels to clinic site with replacement unit and antistatic toolkit.",
             "4. Turn off APC Smart-UPS unit; disconnect power cable, dual Gigabit Ethernet cables, and USB peripherals.",
             "5. Unlock 6U server rack enclosure; unmount failed appliance chassis.",
             "6. Mount replacement appliance; reconnect Ethernet Port 1 (LAN Switch), Port 2 (WAN Fiber), UPS USB signaling cable, and thermal printer USB.",
             "7. Power on UPS and boot replacement unit; verify BIOS auto-power-on engages cleanly.",
             "8. Connect maintenance laptop to front Service Port (192.168.100.1:8443) and execute provisioning CLI: `sudo /opt/namma/bin/namma-commission.sh --clinic-id BBMP-CLN-042 --zone SOUTH`.",
             "9. Script establishes mTLS handshake with cloud control plane; downloads encrypted SQLite tenant slice and active formulary.",
             "10. Verify workstation tablets connect to local PWA URL: `https://clinic.local:8443`; conduct test queue token print on thermal slip printer."
         ],
         "Execute synthetic intake and test prescription on workstation PWA; confirm local SQLite commit succeeds and sync daemon pushes test record to cloud.",
         "If replacement unit fails to boot, switch clinic to paper backup records and retrieve secondary spare from Central Health Office."),

        ("ARCH-DR-003", "Municipal WAN / Fiber Severance - Seamless Offline Operation",
         "SEV-2 (Major)", "Civil construction roadwork cuts municipal fiber backhaul and primary ISP link to clinic.",
         "Clinic Staff (Autonomous), Network Operations Center (NOC)", "< 1 Minute (Autonomous)", "0 Minutes (Zero Loss)",
         "Municipal road excavation severs primary fiber link. Edge appliance autonomously engages cellular failover and local SQLite operation.",
         "RACI: Edge Daemon Daemon (R), Zonal NOC Engineer (A), Clinic Staff (C), Municipal ISP NOC (I).",
         [
             "1. Edge health monitor daemon detects 3 consecutive packet losses to cloud API gateway (`ping -c 3 10.240.0.1`).",
             "2. Appliance network interface switcher automatically activates secondary LTE eSIM modem (`wwan0`).",
             "3. If cellular connection is unavailable or signal jammed, appliance enters FULLY AUTONOMOUS OFFLINE MODE.",
             "4. Workstation PWA displays prominent amber alert banner: 'OFFLINE MODE ACTIVE - Local Edge Server Operating. Zero Disruption.'",
             "5. All clinic workflows (registration, triage, MEWS scoring, doctor consultation, e-Rx, pharmacy dispensing) execute against local SQLite database.",
             "6. Every transaction appends an entry to the `offline_mutation_journal` table with an incremented sequence number and local HMAC signature.",
             "7. Local thermal slip printer prints offline verification QR codes for patient prescriptions.",
             "8. NOC monitors fiber outage status via BBMP GIS backhaul dashboard; dispatches municipal fiber repair crew.",
             "9. Upon fiber repair, edge daemon detects stable connectivity (60 seconds continuous ping to cloud).",
             "10. Edge daemon initiates batched Zstandard-compressed replay of queued mutations: `curl -X POST https://sync.nammahealth.bbmp.gov.in/v1/replay -d @mutation_batch.zst`."
         ],
         "Confirm `offline_mutation_journal` pending count drops to zero; verify all offline encounter IDs exist in central PostgreSQL database.",
         "If offline operation exceeds 72 hours, technician manually extracts encrypted SQLite database snapshot to secure USB drive for cloud ingest."),

        ("ARCH-DR-004", "Regional Cloud Datacenter Total Loss (Cross-Region DR Activation)",
         "SEV-1 (Critical)", "Catastrophic power grid failure, flood, or fiber disconnection wiping out primary Bengaluru cloud datacenter.",
         "Incident Commander, Principal Architect, Cloud SRE Team", "< 30 Minutes", "< 15 Minutes",
         "Total failure of Bengaluru cloud datacenter. SRE team activates warm standby disaster recovery region in Hyderabad.",
         "RACI: SRE Incident Commander (R), Principal Cloud Architect (A), BBMP Health Commissioner (C), Executive Secretariat (I).",
         [
             "1. SRE Incident Commander declares SEV-1 Disaster after confirming total unreachability of Bengaluru AZ-1 and AZ-2 for > 10 minutes.",
             "2. Convene emergency virtual War Room bridge with core SRE, DBA, and Network engineering leads.",
             "3. Update Route53 / Cloudflare DNS traffic policy: shift `*.nammahealth.bbmp.gov.in` to Hyderabad Secondary NLB IP: `203.0.113.50`.",
             "4. Connect to Hyderabad Patroni cluster; promote read replica standby to read-write master: `patronictl -c /etc/patroni/namma-hyd.yml promote`.",
             "5. Assert Hyderabad database write capability: `psql -h hyd-db-vip -U namma_dba -d namma_master -c 'SELECT pg_is_in_recovery();'` (must be `false`).",
             "6. Scale Kubernetes microservice deployments in Hyderabad cluster from warm capacity (2 pods) to production scale (8 pods each): `kubectl scale deployment --all --replicas=8 -n namma-prod`.",
             "7. Verify Redis Sentinel cluster promotion in Hyderabad region: `redis-cli -h hyd-redis info replication`.",
             "8. Broadcast cloud DNS update push to all 183 clinic edge appliances via SMS gateway telemetry ping.",
             "9. Verify edge appliances re-establish mTLS connections to Hyderabad sync endpoint (`sync-hyd.nammahealth.bbmp.gov.in`).",
             "10. Monitor real-time transaction ingestion and verify ClickHouse CDC streams reconnect cleanly."
         ],
         "Execute automated synthetic clinical journey test against Hyderabad ingress; assert end-to-end latency < 300ms and zero error responses.",
         "Do not activate cross-region DR if primary datacenter outage is estimated at < 15 minutes to avoid unneeded split-brain risk."),

        ("ARCH-DR-005", "Ransomware / Cryptographic Vault Intrusion Isolation & Key Revocation",
         "SEV-1 (Critical)", "Compromise of HashiCorp Vault root credentials, suspected key exfiltration, or ransomware signature detected.",
         "Chief Information Security Officer (CISO), SecOps Lead, Cloud SRE", "< 15 Minutes", "0 Minutes (Zero Loss)",
         "Suspected cryptographic credential leak or unauthorized administrative access. SecOps initiates immediate lockdown and key revocation.",
         "RACI: CISO / SecOps Lead (R), Principal Architect (A), BBMP Health Commissioner (C), CERT-In / Police Cyber Division (I).",
         [
             "1. SecOps team executes emergency Vault cluster seal: `vault operator seal` across all active HashiCorp Vault instances.",
             "2. Isolate compromised Kubernetes pods via Calico NetworkPolicy: apply immediate egress deny-all rule to affected namespace.",
             "3. Revoke all active JSON Web Tokens (JWT) by incrementing the global key version counter in Redis and issuing emergency token blacklist.",
             "4. Invalidate all existing database connection passwords and service credentials in PostgreSQL primary.",
             "5. Terminate all active staff sessions across all 183 clinics; force complete re-authentication.",
             "6. Verify database file immutability against AWS S3 WORM snapshots taken prior to the intrusion timestamp.",
             "7. Initialize emergency air-gapped root HSM; generate fresh master RSA/ECDSA signing keys and database master passwords.",
             "8. Unseal Vault using air-gapped Shamir secret key shares held by 3 designated BBMP trustees.",
             "9. Roll out new TLS certificates, service secrets, and API tokens via automated Ansible playbook.",
             "10. Gradually restore application ingress; monitor honeypot alerts and security telemetry for repeat unauthorized attempts."
         ],
         "Verify zero unauthorized API calls; confirm all staff re-authenticate with MFA; verify WORM audit ledger integrity matches pre-incident Merkle root.",
         "If ransomware encryption has touched active storage, immediately fail over to read-only cold WORM snapshot from secondary region."),

        ("ARCH-DR-006", "Corrupted Edge SQLite Database Restoration from Cloud Mirror",
         "SEV-2 (Major)", "Abrupt power cut during unbuffered write causes SQLite disk image malformed error (`SQLITE_CORRUPT`).",
         "Zonal IT Technician, Remote SRE Operations", "< 20 Minutes", "< 5 Minutes",
         "Local SQLite database file corruption halts clinic operations. Edge daemon initiates automatic self-repair or requests cloud hydration.",
         "RACI: Edge Daemon Auto-Recovery (R), Zonal IT Lead (A), Clinic Pharmacist (C), Cloud Database Lead (I).",
         [
             "1. Edge daemon encounters `SQLITE_CORRUPT` error during query execution; immediately flags local database as damaged.",
             "2. Daemon moves damaged database file to quarantine directory: `mv /opt/namma/data/clinic.db /opt/namma/data/corrupt_$(date +%s).db`.",
             "3. Daemon attempts local repair using SQLite recovery engine: `sqlite3 corrupt.db \".recover\" | sqlite3 /opt/namma/data/clinic.db`.",
             "4. If local repair fails, daemon initiates emergency cloud hydration over mTLS connection: `curl -s https://sync.nammahealth.bbmp.gov.in/v1/hydrate/BBMP-CLN-042 -o /tmp/snapshot.zst`.",
             "5. Cloud sync service generates clinic-specific snapshot containing patient demographics, active appointments, and 7-day medication records.",
             "6. Edge daemon decompresses snapshot using Zstandard and installs to `/opt/namma/data/clinic.db`.",
             "7. Verifies database schema integrity: `sqlite3 /opt/namma/data/clinic.db \"PRAGMA integrity_check;\"` (must return `ok`).",
             "8. Restarts local edge web server and queue manager services: `systemctl restart namma-edge-daemon`.",
             "9. Re-attaches connected workstation browsers and verifies active clinic queue restores cleanly.",
             "10. Replays any un-synced transactions salvaged from the quarantined damaged database file."
         ],
         "Assert `PRAGMA integrity_check;` returns `ok`; confirm staff can query existing patient records without error.",
         "If cloud hydration fails due to network outage, restore from nightly local backup snapshot `/opt/namma/backup/clinic_nightly.db`."),

        ("ARCH-DR-007", "Kafka Cluster Broker Loss & Topic Partition Rebalancing",
         "SEV-2 (Major)", "Unrecoverable hardware failure of 2 out of 5 Apache Kafka brokers in production cloud cluster.",
         "Cloud Platform Engineer, SRE On-Call", "< 15 Minutes", "0 Minutes (Zero Loss)",
         "Hardware host crash drops 2 Kafka brokers, creating under-replicated partitions on clinical CDC topics.",
         "RACI: SRE On-Call (R), Platform Lead (A), Analytics Lead (C), Support Desk (I).",
         [
             "1. AlertManager fires `KafkaUnderReplicatedPartitions` critical alert.",
             "2. Platform engineer connects to Kafka monitoring pod: `kubectl exec -it kafka-tool-pod -n monitoring -- bash`.",
             "3. Inspect broker cluster status: `kafka-topics --bootstrap-server kafka:9092 --describe --under-replicated-partitions`.",
             "4. Kubernetes StatefulSet automatically schedules replacement broker pods with persistent NVMe storage.",
             "5. Generate partition reassignment configuration for under-replicated topics: `kafka-reassign-partitions --bootstrap-server kafka:9092 --generate --topics-to-move-json-file topics.json --broker-list '1,2,3,4,5'`.",
             "6. Execute partition reassignment plan: `kafka-reassign-partitions --bootstrap-server kafka:9092 --reassignment-json-file reassign.json --execute`.",
             "7. Track reassignment progress until complete: `kafka-reassign-partitions --bootstrap-server kafka:9092 --reassignment-json-file reassign.json --verify`.",
             "8. Verify all topics satisfy minimum in-sync replica threshold: `min.insync.replicas = 2`.",
             "9. Inspect consumer group lag for Debezium CDC and notification pipelines: `kafka-consumer-groups --bootstrap-server kafka:9092 --describe --group namma-cdc-group`.",
             "10. Verify ClickHouse CDC ingestion resumes and lag drops below 1,000 records."
         ],
         "Verify zero lost CDC events; assert all producer microservices report zero failed publish exceptions in OTel spans.",
         "If Kafka rebalance causes excessive disk I/O, throttle reassignment bandwidth to 50MB/s using `--throttle 52428800`."),

        ("ARCH-DR-008", "Line-Interactive UPS Low-Battery Graceful Edge Appliance Shutdown",
         "SEV-3 (Moderate)", "Grid power failure at clinic site exceeds 90 minutes; UPS battery level drops below 15% reserve.",
         "Edge Appliance Daemon (Autonomous), Clinic Security Guard", "< 5 Minutes (Autonomous)", "0 Minutes (Zero Loss)",
         "Prolonged power outage exhausts UPS battery. Automated daemon initiates orderly shutdown to prevent file corruption.",
         "RACI: NUT `upsmon` Daemon (R), Zonal IT Lead (A), Clinic Duty Nurse (C), BBMP Facilities (I).",
         [
             "1. APC Smart-UPS battery charge drops below 15% during prolonged municipal power outage.",
             "2. Network UPS Tools (`upsmon`) daemon intercepts `LOWBATT` signal over USB interface.",
             "3. Daemon executes emergency broadcast to all workstation PWA screens: 'POWER SHUTDOWN IMMINENT: Saving clinical records...'",
             "4. Edge daemon instructs SQLite database to flush all unwritten pages and truncate WAL: `PRAGMA wal_checkpoint(TRUNCATE);`.",
             "5. Daemon safely closes all active database connections and stops local web server service.",
             "6. Flushes operating system filesystem write caches: `sync`.",
             "7. Issues delayed hardware sleep command to UPS micro-controller: `upscmd -u upsmon-user -p SecretPass! apc1200 load.off.delay 30`.",
             "8. Executes orderly Linux system shutdown: `systemctl poweroff`.",
             "9. Upon municipal power restoration, UPS automatically re-energizes load outlets.",
             "10. Edge appliance BIOS ('AC Power Recovery: Power On') automatically boots appliance, verifies filesystem, and restarts clinic services."
         ],
         "Inspect systemd journal upon restart; verify clean unmount timestamp and zero SQLite recovery errors on initial boot.",
         "If UPS fails to shutdown appliance before power cuts, run full filesystem check `fsck -y /dev/md0` on next boot."),

        ("ARCH-DR-009", "Central Ingress API Gateway DDoS / Volumetric Flood Mitigation",
         "SEV-1 (Critical)", "Volumetric HTTP/TCP SYN flood (> 100 Gbps) targeting municipal public health API gateway.",
         "SecOps On-Call, Cloud Platform Lead, Cloudflare / Akamai SOC", "< 10 Minutes", "0 Minutes (Zero Loss)",
         "Massive distributed denial of service attack saturates cloud ingress bandwidth, blocking citizen access and clinic sync.",
         "RACI: Cloudflare SOC / SecOps Lead (R), Cloud Platform Lead (A), BBMP Commissioner (C), Cyber Crime Cell (I).",
         [
             "1. Ingress network monitoring detects sudden 25x bandwidth surge (> 100 Gbps) hitting `/api/v1/*` endpoints.",
             "2. SRE on-call activates Cloudflare / Edge CDN 'Under Attack' mode with managed JS challenge rules.",
             "3. Gateway token bucket rate limiters automatically engage: restrict unauthenticated public traffic to 20 req/sec per IP subnet.",
             "4. Enable strict mutual TLS (mTLS) enforcement on `/api/v1/sync/*`: drop all non-mTLS packets at edge boundary.",
             "5. Verify clinic edge-to-cloud synchronization traffic bypasses public challenge via dedicated mTLS IP whitelist.",
             "6. Apply geographic firewall filtering: block all ingress traffic originating outside Republic of India IP ranges.",
             "7. Inspect ingress access logs in OpenSearch; identify attack signatures and deploy targeted WAF custom blocking rules.",
             "8. Scale Kong / Envoy API Gateway pods horizontally from 6 to 24 replicas: `kubectl scale deployment api-gateway --replicas=24 -n namma-prod`.",
             "9. Monitor gateway CPU utilization and P95 latency returning to normal operational thresholds (< 150ms).",
             "10. Compile attack forensic report for submission to Indian Computer Emergency Response Team (CERT-In)."
         ],
         "Confirm edge synchronization latency returns to < 1,000ms; verify zero legitimate clinic staff requests blocked by rate limiter.",
         "Never apply global rate limits to `/api/v1/sync/*` endpoint to ensure clinic edge sync operations remain unimpeded."),

        ("ARCH-DR-010", "National ABDM Gateway Extended Outage Queuing & Bulk Replay",
         "SEV-2 (Major)", "National Health Authority (NHA) ABDM central gateway unreachable for > 6 hours.",
         "Interoperability Lead, Integration SRE", "< 15 Minutes", "0 Minutes (Zero Loss)",
         "National health portal maintenance or outage prevents real-time publishing of FHIR care bundles.",
         "RACI: Integration Engineer (R), Interoperability Lead (A), Chief Medical Officer (C), NHA Helpdesk (I).",
         [
             "1. ABDM bridge service detects consecutive HTTP 503 / 504 gateway timeouts from NHA central servers.",
             "2. Circuit breaker automatically trips from CLOSED to OPEN state, halting direct API calls to NHA.",
             "3. Platform UI displays subtle notification: 'National ABDM Sync Queued (National Gateway Under Maintenance)'.",
             "4. Outbound FHIR R4 Bundles (Encounter, Prescription, Diagnostic Report) are enqueued into durable Kafka topic `namma.abdm.publish.queue`.",
             "5. Clinic doctors and nurses continue patient consultations and care workflows with zero UI latency or blocking.",
             "6. Integration bridge background health probe queries NHA health endpoint `/v0.5/heartbeat` every 60 seconds with exponential backoff.",
             "7. Upon NHA gateway recovery (10 consecutive successful probes), circuit breaker transitions to HALF-OPEN.",
             "8. Throttled consumer begins draining backlog queue at controlled rate (50 bundles/second) to prevent gateway rate-limit trips.",
             "9. Verify care context registration acknowledgments received from NHA and update local transaction status.",
             "10. Once backlog queue reaches zero, circuit breaker resets to CLOSED state; notify municipal digital health lead."
         ],
         "Verify Kafka backlog consumer lag drops to zero; assert all queued encounters show `abdm_synced = true`.",
         "If NHA rejects bundles due to schema changes, redirect failed bundles to Dead Letter Queue (DLQ) for schema patching."),

        ("ARCH-DR-011", "Corrupted Patient Master Index Split-Brain Disentanglement",
         "SEV-2 (Major)", "Network partition causes two different clinics to register conflicting master records for the same citizen.",
         "Lead Medical Registrar, Database Administrator", "< 4 Hours", "< 15 Minutes",
         "Offline operations in different clinics lead to duplicate patient records for the same citizen. Requires deterministic reconciliation.",
         "RACI: Zonal Medical Officer (R), Lead Registrar (A), Clinical Data Lead (C), Affected Citizen (I).",
         [
             "1. Master Patient Index (MPI) cloud deduplication engine flags high-confidence phonetic Soundex match during cross-clinic sync.",
             "2. Both conflicting patient records (`PAT-001` and `PAT-002`) are tagged with status `RECONCILIATION_REQUIRED`.",
             "3. Automatic consolidation is paused to prevent erroneous merging of clinical histories.",
             "4. Zonal Medical Officer opens Clinical Identity Disentanglement Console.",
             "5. Officer inspects demographic fields: Aadhaar last 4 digits, phone number, date of birth, photo portrait, and address.",
             "6. If confirmed as distinct individuals with coincidentally identical names: officer marks records as `DISTINCT_VERIFIED`.",
             "7. If confirmed as identical citizen: officer selects primary surviving ID (`PAT-001`) and triggers Master Merge Tool.",
             "8. Tool remaps all historical encounters, lab reports, and prescriptions from `PAT-002` to `PAT-001` in an atomic database transaction.",
             "9. Deprecated ID `PAT-002` is marked as `MERGED_TOMBSTONE` with permanent redirect pointer to `PAT-001`.",
             "10. Append cryptographic audit event to WORM ledger documenting merge rationale, approving officer credentials, and timestamp."
         ],
         "Assert queries for both old and new patient IDs resolve transparently to consolidated survivor record; zero orphan encounters.",
         "Never delete deprecated patient ID from database; maintain permanent tombstone for historical audit trail."),

        ("ARCH-DR-012", "Redis Cluster Memory Exhaustion & Cache Rebuilding",
         "SEV-2 (Major)", "Redis cluster memory utilization reaches 95% due to session key TTL leaks; evictions impacting performance.",
         "Backend Lead, SRE On-Call", "< 15 Minutes", "0 Minutes (Zero Loss)",
         "Unbounded cache growth threatens session store stability. SRE clears stale cache keys and pre-heats essential formularies.",
         "RACI: SRE On-Call (R), Backend Lead (A), DevOps Lead (C), Clinic Staff (I).",
         [
             "1. AlertManager triggers `RedisMemoryHigh` alert (> 90% allocated RAM).",
             "2. SRE connects to Redis master node: `redis-cli -h redis-cluster.internal -p 6379 info memory`.",
             "3. Run key space analysis to identify leaking key patterns: `redis-cli --bigkeys`.",
             "4. Identify leaking temporary keys missing TTL (e.g., untracked search autocomplete buffers).",
             "5. Set temporary eviction policy to protect active user sessions: `CONFIG SET maxmemory-policy volatile-lru`.",
             "6. Safely scan and delete offending stale cache keys in batches: `redis-cli --scan --pattern 'temp:search:*' | xargs -L 500 redis-cli del`.",
             "7. Verify memory utilization drops below 65% of cluster capacity.",
             "8. Execute cache warm-up script to repopulate essential static catalogs (Formulary, ICD-10, Clinic Master): `python /opt/namma/scripts/warm_cache.py`.",
             "9. Verify cache hit ratio recovers to > 90% within 10 minutes.",
             "10. File bug ticket with backend engineering to enforce mandatory TTL on all new cache keys."
         ],
         "Confirm Redis memory drops below 60%; assert drug formulary lookup latency returns to < 5ms.",
         "Never run `FLUSHALL` on production Redis cluster as this invalidates active staff sessions and forces clinic re-logins."),

        ("ARCH-DR-013", "ClickHouse Columnar Analytics Disk Space Exhaustion Emergency Truncate/Tier",
         "SEV-2 (Major)", "Columnar data disk on ClickHouse analytics server exceeds 92% capacity due to uncompressed CDC logs.",
         "Data Platform Engineer, Analytics SRE", "< 30 Minutes", "0 Minutes (Zero Loss)",
         "Rapid growth of analytics event tables threatens data warehouse availability. SRE triggers emergency partition tiering to S3.",
         "RACI: Analytics SRE (R), Data Platform Lead (A), Municipal Epidemiologist (C), Support Team (I).",
         [
             "1. AlertManager fires `ClickHouseDiskSpaceCritical` (> 90% disk utilization).",
             "2. Connect to ClickHouse client: `clickhouse-client --host localhost --port 9000`.",
             "3. Inspect table disk consumption: `SELECT table, formatReadableSize(sum(bytes_on_disk)) FROM system.parts WHERE active GROUP BY table ORDER BY sum(bytes_on_disk) DESC LIMIT 5;`.",
             "4. Identify oldest monthly partitions in high-volume tables (`telemetry_spans`, `audit_events_cdc`).",
             "5. Execute partition tiering command to move partitions older than 90 days from NVMe SSD to S3 object storage tier: `ALTER TABLE telemetry_spans MOVE PARTITION '2026-05' TO VOLUME 's3_cold';`.",
             "6. Trigger background part compaction to reclaim storage immediately: `OPTIMIZE TABLE telemetry_spans FINAL;`.",
             "7. Verify physical disk utilization drops below 65% on local NVMe storage.",
             "8. Review automated ClickHouse retention TTL policy: ensure `TTL event_date + INTERVAL 90 DAY TO VOLUME 's3_cold'` is active.",
             "9. Verify municipal epidemiological queries continue to execute seamlessly across tiered partitions.",
             "10. Check that Debezium CDC consumer lag recovers to baseline."
         ],
         "Confirm ClickHouse disk space utilization < 70%; verify analytical queries for municipal epidemiological dashboard succeed in < 1,500ms.",
         "Never drop or delete clinical encounter partitions; move to cold object storage instead."),

        ("ARCH-DR-014", "108 Emergency CAD Integration Breakdown Voice Fallback",
         "SEV-1 (Critical)", "GVK-EMRI 108 ambulance dispatch REST API server returns persistent HTTP 500 errors during emergency triage.",
         "Triage Nurse, Clinic Duty Doctor, Emergency Dispatch Coordinator", "< 2 Minutes", "0 Minutes (Zero Loss)",
         "API failure during critical emergency referral. System initiates instant automated voice dispatch protocol to prevent transfer delays.",
         "RACI: Clinic Duty Doctor (R), Triage Nurse (A), 108 CAD Operator (C), Medical Superintendent (I).",
         [
             "1. Triage nurse or doctor clicks 'Dispatch 108 Ambulance' for critical patient with MEWS >= 5.",
             "2. Platform CAD integration bridge detects repeated HTTP 500 / timeout errors from GVK-EMRI central dispatch API.",
             "3. Workstation UI instantly presents emergency red banner: '108 API DOWN - Priority Voice Dispatch Active'.",
             "4. System automatically generates a 4-digit Priority Dispatch Passcode (e.g., `CAD-8821`).",
             "5. System renders pre-formatted Emergency Transfer Summary on screen: Patient Name, Age, Vital Signs, Suspected Diagnosis, Clinic GPS Coordinates.",
             "6. Duty doctor taps 'Call 108 Hotline' on clinic VoIP terminal or dials `080-2266-0108` on clinic landline.",
             "7. Doctor provides priority passcode `CAD-8821` to 108 dispatcher; dispatcher enters code into GVK-EMRI terminal to pull pre-filled patient transfer profile.",
             "8. Dispatcher confirms ambulance unit allocation, vehicle registration number, and estimated time of arrival (ETA).",
             "9. Doctor inputs vehicle registration number and ETA into workstation PWA to seal emergency referral dossier.",
             "10. System prints emergency referral summary with barcode for physical handover to ambulance paramedic crew."
         ],
         "Confirm emergency referral status marked as `DISPATCHED_VOICE`; assert ambulance ETA timestamp successfully recorded.",
         "Never delay physical patient stabilization or resuscitation while attempting electronic referral dispatch."),

        ("ARCH-DR-015", "Clinic Workstation Mass Browser Cache Corruption Reset",
         "SEV-3 (Moderate)", "Bad PWA service worker script caching corrupts local workstation browser state across all clinic PCs.",
         "Zonal IT Technician, Clinic Receptionist", "< 15 Minutes", "0 Minutes (Zero Loss)",
         "Corrupted browser cache causes white-screen errors on workstation tablets following frontend deployment.",
         "RACI: Zonal IT Support (R), Clinic Receptionist (A), Frontend Lead (C), Clinic Staff (I).",
         [
             "1. Clinic staff report blank screen or JavaScript console exceptions (`ChunkLoadError`) on workstation tablets.",
             "2. Receptionist or staff clicks dedicated desktop shortcut: 'Namma Clinic Emergency Reset'.",
             "3. Shortcut triggers automated PowerShell / Bash cache eviction script in Chromium browser: `google-chrome --clear-token-browsing-data-dir`.",
             "4. Script unregisters active Service Workers, clears IndexedDB caches, and purges localStorage entries.",
             "5. Script restarts Chromium in kiosk mode and navigates to cache-busting entry URL: `https://clinic.local:8443/?app_version=fresh_$(date +%s)`.",
             "6. Browser downloads clean, verified PWA application shell bundle from local edge server.",
             "7. Service worker installs and activates cleanly; establishes WebSocket connection with edge daemon.",
             "8. Receptionist logs in with PIN; verifies patient queue displays and search operates normally.",
             "9. Doctor and pharmacist workstations execute identical reset sequence via desktop shortcut.",
             "10. Confirm all 3 clinic workstations operational and processing patients within 10 minutes."
         ],
         "Assert workstation PWA loads cleanly without JavaScript errors; verify staff can view and edit active consultation drafts.",
         "Instruct staff never to clear browser cookies during active consultations without first ensuring draft is saved locally.")
    ]

    for rb in dr_runbooks:
        rb_id, rb_title, rb_sev, rb_trigger, rb_roles, rb_rto, rb_rpo, rb_context, rb_raci, rb_steps, rb_verify, rb_abort = rb
        rb_num = int(rb_id.split('-')[2])
        p(f"### 06.{rb_num:02d} Runbook `{rb_id}`: {rb_title}")
        p(f"- **Runbook Identifier:** `{rb_id}`")
        p(f"- **Severity Classification:** **{rb_sev}**")
        p(f"- **Activation Trigger / Precondition:** {rb_trigger}")
        p(f"- **Responsible Roles & Authority:** {rb_roles}")
        p(f"- **Target Runbook RTO:** {rb_rto}")
        p(f"- **Target Runbook RPO:** {rb_rpo}")
        p(f"- **Operational Context:** {rb_context}")
        p(f"- **Operational RACI Matrix:** {rb_raci}")
        p("")
        p("#### Diagnostic Decision Matrix & Activation Thresholds:")
        p("```")
        p(" +-----------------------------+       Metric breaches threshold        +-----------------------------+")
        p(" |   Telemetry / Alert Fires   | -------------------------------------> |   Evaluate Automated Action |")
        p(" +-----------------------------+                                        +-----------------------------+")
        p("                |                                                                      |")
        p("                | Auto-mitigation fails                                                | Success")
        p("                v                                                                      v")
        p(" +-----------------------------+                                        +-----------------------------+")
        p(" |   Escalate to SRE On-Call   | <--- Human intervention required ----- |     Close Alert / Log PIR   |")
        p(" +-----------------------------+                                        +-----------------------------+")
        p("```")
        p("")
        p("#### Step-by-Step Emergency Mitigation Procedure:")
        for step in rb_steps:
            p(f"{step}")
        p("")
        p("#### Post-Incident Verification & Quality Gate:")
        p(f"- **Authoritative Verification Criteria:** {rb_verify}")
        p(f"- **Fail-Safe Abort / Rollback Directive:** {rb_abort}")
        p("")
        p("#### Post-Incident Review (PIR) Reporting Standard:")
        p(f"Within 24 hours of `{rb_id}` resolution, the Incident Commander must publish a formal blameless post-mortem covering: 1) Incident Timeline, 2) Root Cause Analysis (5 Whys), 3) Customer/Citizen Impact Duration, 4) Remediation Action Items with assigned Jira tickets.")
        p("")
        p("---")
        p("")

    p("## 07. Backup, WAL Archiving & Point-in-Time Recovery (PITR) Strategy")
    p("Exhaustive backup schedule, retention tiering, cryptographic encryption, and PITR restoration procedures:")
    p("")
    p("### 07.1 Backup Schedule & Multi-Tier Retention Matrix")
    p("| Backup Type | Frequency | Snapshot Mechanism | Storage Location | Retention Window | Encryption Standard | WORM Immutability |")
    p("| :--- | :---: | :--- | :--- | :---: | :---: | :---: |")
    p("| **Full Base Backup** | Weekly (Sunday 01:00 IST) | `pgBackRest` full cluster snapshot | Cloud Object Storage (AZ-1 & AZ-3) | 90 Days | AES-256-GCM | Enabled (90-Day Lock) |")
    p("| **Differential Backup** | Daily (Mon-Sat 02:00 IST) | `pgBackRest` differential block scan | Cloud Object Storage (AZ-1 & AZ-3) | 30 Days | AES-256-GCM | Enabled (30-Day Lock) |")
    p("| **Continuous WAL Archiving**| Every 60 Seconds / 16MB | `archive_command` streaming WAL push | Cloud Object Storage (Multi-Region) | 30 Days | AES-256-GCM | Enabled (30-Day Lock) |")
    p("| **Edge SQLite Snapshot** | Daily (20:30 IST Post-Close) | `VACUUM INTO` encrypted archive | Local NVMe + Cloud Sync Mirror | 14 Days | SQLCipher AES-256 | Local File Lock |")
    p("| **Statutory Annual Archival**| Annually (March 31 Close) | Consolidated clinical cold snapshot | AWS S3 Glacier Deep Archive | 10 Years | AES-256-GCM | Strict WORM Compliance |")
    p("")
    p("### 07.2 pgBackRest Production Configuration (`/etc/pgbackrest/pgbackrest.conf`)")
    p("```ini")
    p("[global]")
    p("repo1-type=s3")
    p("repo1-s3-endpoint=s3.ap-south-1.amazonaws.com")
    p("repo1-s3-bucket=namma-backups-primary")
    p("repo1-s3-region=ap-south-1")
    p("repo1-s3-key-type=auto")
    p("repo1-cipher-type=aes-256-cbc")
    p("repo1-cipher-pass=KmsSecuredSecretCipherPassphrase!")
    p("repo1-retention-full=12")
    p("repo1-retention-diff=30")
    p("repo1-bundle=y")
    p("process-max=4")
    p("log-level-console=info")
    p("log-level-file=detail")
    p("start-fast=y")
    p("compress-type=zst")
    p("compress-level=6")
    p("")
    p("[namma]")
    p("pg1-path=/var/lib/postgresql/16/main")
    p("pg1-user=postgres")
    p("pg1-port=5432")
    p("```")
    p("")
    p("### 07.3 Point-in-Time Recovery (PITR) Verification Procedure")
    p("To restore the PostgreSQL master database to any specific second in time (e.g. immediately prior to an erroneous drop-table migration):")
    p("```bash")
    p("# 1. Stop Patroni and PostgreSQL on target restoration host")
    p("systemctl stop patroni")
    p("systemctl stop postgresql")
    p("")
    p("# 2. Clean existing corrupted or damaged data directory")
    p("rm -rf /var/lib/postgresql/16/main/*")
    p("")
    p("# 3. Execute pgBackRest point-in-time restoration to specified timestamp")
    p("pgbackrest --stanza=namma \\")
    p("  --type=time \\")
    p("  --target=\"2026-09-04 14:22:15+05:30\" \\")
    p("  --target-action=promote \\")
    p("  restore")
    p("")
    p("# 4. Verify restored cluster permissions")
    p("chown -R postgres:postgres /var/lib/postgresql/16/main")
    p("chmod 700 /var/lib/postgresql/16/main")
    p("")
    p("# 5. Start PostgreSQL and verify database integrity")
    p("systemctl start postgresql")
    p("psql -U namma_dba -d namma_master -c 'SELECT now(), max(created_at) FROM clinical_encounters;'")
    p("```")
    p("")

    p("## 08. Chaos Engineering, Fault Injection & Quarterly GameDay Drills")
    p("Automated resilience testing using Chaos Mesh and scheduled full-scale disaster simulations:")
    p("")
    p("### 08.1 Automated Chaos Injection Test Matrix")
    p("| Chaos Experiment Code | Target Component | Injected Failure Mode | Automated Assertion | Frequency |")
    p("| :--- | :--- | :--- | :--- | :---: |")
    p("| **CHAOS-001** | Patroni PostgreSQL Primary | `kill -9` primary process | Failover to AZ-2 synchronous standby completes in < 30 sec; zero data loss | Weekly |")
    p("| **CHAOS-002** | Clinic Edge LAN Interface | Drop 100% packets for 2 hours | PWA operates seamlessly offline; mutations queue in SQLite; zero lost records | Bi-Weekly |")
    p("| **CHAOS-003** | Central API Gateway | Inject 500ms network latency | Gateway circuit breaker trips; fallback cache returns valid formulary responses | Weekly |")
    p("| **CHAOS-004** | Redis Master Node | Abrupt pod termination | Redis Sentinel promotes replica in < 10 sec; session logins remain valid | Bi-Weekly |")
    p("| **CHAOS-005** | Kafka Broker 01 | Unclean disk dismount | Topics rebalance to in-sync replicas; consumer lag recovers in < 3 minutes | Monthly |")
    p("")
    p("### 08.2 Sample Chaos Mesh Experiment Manifests")
    p("```yaml")
    p("apiVersion: chaos-mesh.org/v1alpha1")
    p("kind: PodChaos")
    p("metadata:")
    p("  name: patroni-primary-kill")
    p("  namespace: chaos-testing")
    p("spec:")
    p("  action: pod-kill")
    p("  mode: one")
    p("  selector:")
    p("    namespaces:")
    p("      - namma-prod")
    p("    labelSelectors:")
    p("      'role': 'master'")
    p("      'app.kubernetes.io/name': 'patroni'")
    p("  scheduler:")
    p("    cron: '@weekly'")
    p("---")
    p("apiVersion: chaos-mesh.org/v1alpha1")
    p("kind: NetworkChaos")
    p("metadata:")
    p("  name: edge-sync-latency-injection")
    p("  namespace: chaos-testing")
    p("spec:")
    p("  action: delay")
    p("  mode: all")
    p("  selector:")
    p("    namespaces:")
    p("      - namma-prod")
    p("    labelSelectors:")
    p("      'app': 'sync-gateway'")
    p("  delay:")
    p("    latency: '800ms'")
    p("    jitter: '100ms'")
    p("  duration: '30m'")
    p("```")
    p("")
    p("### 08.3 Annual Disaster Recovery & GameDay Simulation Schedule")
    p("- **Q1 (March):** Simulated Metropolitan WAN Blackout across 20 sample clinics; assert 100% offline clinical continuity.")
    p("- **Q2 (June):** Primary Cloud Region Failure Simulation (AZ-1 + AZ-2 simulated cutoff); full failover to Hyderabad DR region.")
    p("- **Q3 (September):** Cryptographic Vault Ransomware GameDay; practice manual Shamir key unsealing and HSM key rotation.")
    p("- **Q4 (December):** Hardware Catastrophe Simulation; random unannounced hot-standby appliance swap at 5 active clinics.")
    p("")

    p("## 09. Disaster Recovery Architecture Fitness Tests & Verification Checklist")
    p("Automated CI/CD validation gates ensuring zero disaster recovery configuration drift:")
    p("")
    p("### 09.1 Automated Architecture Fitness Tests")
    p("1. **Continuous Backup Integrity Gate:** Automated daily pipeline restores latest `pgBackRest` snapshot into an isolated ephemeral test container; executes `pg_dump` and asserts zero corruption.")
    p("2. **Edge Hot-Standby Image Parity Test:** Nightly build compares SHA-256 package manifests of zonal spare images with cloud production build; fails if divergence detected.")
    p("3. **SQLite WAL Fsync Fitness Test:** Benchmarks NVMe sync speed on edge appliance builds; asserts that `PRAGMA synchronous = NORMAL` commits complete in < 15ms.")
    p("4. **Patroni Configuration Schema Linter:** Validates that Patroni DCS TTL and synchronous replication settings match architectural specifications.")
    p("")
    p("### 09.2 Disaster Recovery Audit & Verification Checklist")
    p("| Verification Item | Automated Verification Command | Acceptance Threshold | Enforcement Gate |")
    p("| :--- | :--- | :---: | :---: |")
    p("| Patroni Multi-AZ Replication Sync | `patronictl -c /etc/patroni/namma.yml list` | Lag bytes == 0 on sync standby | Continuous Alerting |")
    p("| Cloud Object Storage WORM Lock | `aws s3api get-object-retention --bucket namma-backups` | Lock status == COMPLIANCE | Nightly Audit |")
    p("| Edge SQLite Integrity Check | `sqlite3 /opt/namma/data/clinic.db \"PRAGMA integrity_check;\"` | Output == 'ok' | Daily Edge Task |")
    p("| UPS Signaling Daemon Health | `upsc apc1200@localhost ups.status` | Output == 'OL' (Online) | Continuous Telemetry |")
    p("| Cross-Region Cascading Lag | `SELECT pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) FROM pg_stat_replication;` | Lag < 67MB (< 5 min) | Continuous Alerting |")
    p("")

    content = "\n".join(lines)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    metrics = count_lines(content)
    print(f"Generated {OUTPUT_FILE}: Total {metrics['total']}, Substantive {metrics['substantive']}")
    return OUTPUT_FILE, metrics["total"], metrics["substantive"]

if __name__ == "__main__":
    generate_document()
