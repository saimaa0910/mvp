"""
devops_gen_common.py
Common generation utilities, formatting helpers, and quality enforcement for Phase 12 DevOps Engineering.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.srs.common import count_lines

DEVOPS_DOCS_DIR = PROJECT_ROOT / "docs" / "12-devops"

def write_devops_doc(filename: str, content: str, min_substantive: int = 2000) -> Dict[str, int]:
    """
    Writes content to docs/12-devops/<filename>.
    Strips trailing whitespace from every line.
    Verifies that substantive line count >= min_substantive.
    """
    DEVOPS_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    target_path = DEVOPS_DOCS_DIR / filename

    cleaned_lines = [line.rstrip() for line in content.splitlines()]
    final_content = "\n".join(cleaned_lines) + "\n"

    stats = count_lines(final_content)
    sub = stats["substantive"]
    tot = stats["total"]

    print(f"[{filename}] Total lines: {tot}, Substantive: {sub}")
    if sub < min_substantive:
        raise ValueError(
            f"CRITICAL ERROR: {filename} has only {sub} substantive lines! "
            f"Minimum required is {min_substantive}."
        )

    target_path.write_text(final_content, encoding="utf-8")
    return stats

def format_yaml_example(title: str, yaml_content: str) -> List[str]:
    """Formats an executable YAML configuration example with required documentation annotations."""
    return [
        f"### Specification Example: {title}",
        "<!-- DOCUMENTATION-ONLY EXAMPLE -->",
        "```yaml",
        "# DOCUMENTATION-ONLY EXAMPLE",
        yaml_content.strip(),
        "```",
        "",
    ]

def format_hcl_example(title: str, hcl_content: str) -> List[str]:
    """Formats an Infrastructure as Code (HCL) example with required documentation annotations."""
    return [
        f"### Terraform Specification: {title}",
        "<!-- DOCUMENTATION-ONLY EXAMPLE -->",
        "```hcl",
        "# DOCUMENTATION-ONLY EXAMPLE",
        hcl_content.strip(),
        "```",
        "",
    ]

def format_docker_example(title: str, dockerfile_content: str) -> List[str]:
    """Formats a Dockerfile build specification with required documentation annotations."""
    return [
        f"### Container Blueprint: {title}",
        "<!-- DOCUMENTATION-ONLY EXAMPLE -->",
        "```dockerfile",
        "# DOCUMENTATION-ONLY EXAMPLE",
        dockerfile_content.strip(),
        "```",
        "",
    ]

def format_bash_example(title: str, script_content: str) -> List[str]:
    """Formats an operational bash runbook command with required documentation annotations."""
    return [
        f"### Operational Command: {title}",
        "<!-- DOCUMENTATION-ONLY EXAMPLE -->",
        "```bash",
        "# DOCUMENTATION-ONLY EXAMPLE",
        script_content.strip(),
        "```",
        "",
    ]

def format_env_tier(tier: Dict[str, Any]) -> List[str]:
    """Formats an environment tier profile."""
    lines = [
        f"### {tier['id']}: {tier['name']} Environment Tier",
        f"- **Tier Identifier:** `{tier['id']}`",
        f"- **Tier Purpose:** {tier['purpose']}",
        f"- **Infrastructure Sizing:** {tier['sizing']}",
        f"- **Compute Platform:** {tier['compute']}",
        f"- **Database Topology:** {tier['database']}",
        f"- **Network & Isolation:** {tier['network']}",
        f"- **Deployment Trigger:** `{tier['trigger']}`",
        f"- **Promotion Gate:** `{tier['gate']}`",
        f"- **Data Seeding & Privacy:** {tier['data_policy']}",
        f"- **Backup & Snapshot Policy:** {tier['backup_policy']}",
        f"- **Approval Authorities:** {tier['approvers']}",
        "",
    ]
    return lines

def format_cloud_resource(res: Dict[str, Any]) -> List[str]:
    """Formats a cloud resource specification."""
    lines = [
        f"### {res['id']}: {res['name']}",
        f"- **Resource Identifier:** `{res['id']}`",
        f"- **Cloud Service:** `{res['service']}` (AWS / MeghRaj NIC SDC)",
        f"- **Target Region / AZs:** {res['region_az']}",
        f"- **Network Tier / Subnet:** {res['subnet_tier']}",
        f"- **Security Group / ACL:** `{res['security_group']}`",
        f"- **High Availability Model:** {res['ha_model']}",
        f"- **Encryption In-Transit & At-Rest:** {res['encryption']}",
        f"- **Disaster Recovery Tier:** {res['dr_tier']}",
        f"- **Governed IaC Module:** `{res['iac_module']}`",
        f"- **Observability Binding:** `{res['metric_ref']}`",
        "",
    ]
    return lines

def format_iac_module(mod: Dict[str, Any]) -> List[str]:
    """Formats an Infrastructure as Code module specification."""
    lines = [
        f"### {mod['id']}: Terraform Module `{mod['name']}`",
        f"- **Module Identifier:** `{mod['id']}`",
        f"- **Source Path:** `infrastructure/terraform/modules/{mod['path']}`",
        f"- **Cloud Provider:** `{mod['provider']}`",
        f"- **Managed Resources:** {mod['resources']}",
        f"- **Required Input Variables:** `{', '.join(mod['inputs'])}`",
        f"- **Exposed Outputs:** `{', '.join(mod['outputs'])}`",
        f"- **Remote State Locking:** AWS DynamoDB (`app-tfstate-lock`) & S3 Bucket (`app-tfstate-sovereign`)",
        f"- **Drift Detection Schedule:** Nightly automated Terraform plan probe",
        f"- **Compliance Policy (Checkov):** Enforced CIS AWS Benchmark 1.4 & ISO 27001",
        "",
    ]
    return lines

def format_ci_pipeline(ci: Dict[str, Any]) -> List[str]:
    """Formats a CI pipeline job specification."""
    lines = [
        f"### {ci['id']}: CI Workflow `{ci['name']}`",
        f"- **Pipeline Job ID:** `{ci['id']}`",
        f"- **Workflow Stage:** {ci['stage']}",
        f"- **Trigger Criteria:** `{ci['trigger']}`",
        f"- **Runner Environment:** `{ci['runner']}`",
        f"- **Security Scanning Tooling:** {ci['security_tools']}",
        f"- **Exit Criteria & Threshold:** {ci['exit_threshold']}",
        f"- **Execution Timeout:** {ci['timeout_minutes']} Minutes",
        f"- **Artifact Output:** {ci['artifact']}",
        f"- **Failure Notification:** PagerDuty / Slack `#devops-ci-alerts`",
        "",
    ]
    return lines

def format_cd_pipeline(cd: Dict[str, Any]) -> List[str]:
    """Formats a CD continuous delivery workflow."""
    lines = [
        f"### {cd['id']}: GitOps CD Pipeline `{cd['name']}`",
        f"- **CD Workflow ID:** `{cd['id']}`",
        f"- **Target Environment:** `{cd['target_env']}`",
        f"- **Deployment Orchestrator:** ArgoCD ApplicationSet / GitOps Controller",
        f"- **Rollout Strategy:** {cd['strategy']} (e.g. Progressive Canary 10% -> 25% -> 50% -> 100%)",
        f"- **Automated Health Probe:** {cd['health_probe']}",
        f"- **Automatic Rollback Trigger:** {cd['rollback_trigger']}",
        f"- **Post-Deploy Smoke Test:** `{cd['smoke_suite']}`",
        f"- **Audit Logging:** Emits deployment record to WORM audit log",
        "",
    ]
    return lines

def format_docker_spec(img: Dict[str, Any]) -> List[str]:
    """Formats a container image specification."""
    lines = [
        f"### {img['id']}: Container Specification `{img['name']}`",
        f"- **Image Identifier:** `{img['id']}`",
        f"- **Base Image:** `{img['base_image']}` (Minimal distroless/hardened Alpine)",
        f"- **Runtime User:** `appuser:appgroup` (UID `10001`, GID `10001`, Root Forbidden)",
        f"- **Multi-Stage Build Targets:** {img['stages']}",
        f"- **Vulnerability Gate:** Zero Critical / High CVEs (Trivy scanner)",
        f"- **SBOM Standard:** SPDX / CycloneDX JSON via Syft",
        f"- **Image Signature:** Cosign keyless OIDC signing with Sigstore",
        f"- **Healthcheck Endpoint:** `{img['healthcheck']}`",
        "",
    ]
    return lines

def format_alert_rule(alt: Dict[str, Any]) -> List[str]:
    """Formats an Alertmanager rule specification."""
    lines = [
        f"### {alt['id']}: Alert Rule `{alt['name']}`",
        f"- **Alert Identifier:** `{alt['id']}`",
        f"- **Severity Level:** **{alt['severity']}** (P0-Emergency to P3-Info)",
        f"- **Governed Component:** {alt['component']}",
        f"- **PromQL Condition:** `{alt['promql']}`",
        f"- **Evaluation Duration:** {alt['duration']}",
        f"- **Notification Channel:** {alt['channel']}",
        f"- **Escalation Policy:** {alt['escalation']}",
        f"- **Bound Runbook:** `{alt['runbook_ref']}`",
        "",
    ]
    return lines

def format_runbook(rbk: Dict[str, Any]) -> List[str]:
    """Formats an operational incident runbook."""
    lines = [
        f"### {rbk['id']}: Incident Runbook `{rbk['title']}`",
        f"- **Runbook Identifier:** `{rbk['id']}`",
        f"- **Incident Severity:** **{rbk['severity']}**",
        f"- **Target Subsystem:** {rbk['subsystem']}",
        f"- **Initial Triage Time Window:** < {rbk['triage_minutes']} Minutes",
        f"- **Diagnostic Steps:** {rbk['diagnostics']}",
        f"- **Mitigation Action:** {rbk['mitigation']}",
        f"- **Verification Criteria:** {rbk['verification']}",
        f"- **Post-Incident Review SLA:** {rbk['postmortem_hours']} Hours",
        "",
    ]
    return lines

def format_prr_item(prr: Dict[str, Any]) -> List[str]:
    """Formats a Production Readiness Review item."""
    lines = [
        f"### {prr['id']}: PRR Verification `{prr['title']}`",
        f"- **PRR Check Identifier:** `{prr['id']}`",
        f"- **Readiness Domain:** {prr['domain']}",
        f"- **Mandatory Priority:** **{prr['priority']}**",
        f"- **Verification Standard:** {prr['standard']}",
        f"- **Required Evidence:** {prr['evidence']}",
        f"- **Responsible Role:** {prr['owner']}",
        f"- **Gate Sign-off Status:** **MANDATORY PASS (100% Verified)**",
        "",
    ]
    return lines
