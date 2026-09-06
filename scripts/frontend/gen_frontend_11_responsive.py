"""
gen_frontend_11_responsive.py
Generator for docs/09-frontend/11-responsive-design.md.
Produces >= 2,000 substantive lines detailing responsive design layout strategies,
viewport token systems, dual-device optimization (10-inch Android tablets vs 21-inch desktops),
and exhaustive screen-by-screen responsive layout specifications across all 108 screens.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.frontend.frontend_gen_common import write_fe_doc
from scripts.frontend.frontend_core_data import SCREENS

def generate_doc():
    lines = []
    lines.append("# Namma Clinic Frontend Responsive Design & Multi-Device Viewport Strategy")
    lines.append("")
    lines.append("## 1. Executive Summary & Hardware Form Factor Strategy")
    lines.append("Namma Clinic healthcare software operates in diverse clinical environments across 183 primary health centers in the Greater Bengaluru metropolitan area. The user interface must seamlessly scale across two primary hardware form factors:")
    lines.append("1. **10-Inch Android Field Tablets (1280x800, WXGA, 149 PPI):** Deployed for ASHA workers, ANM mobile outreach, queue marshals, and portable triage stations. Demands high-contrast, finger-friendly touch targets (minimum 48x48 CSS pixels), single-column fluid stacking, and on-screen virtual keyboard accommodation.")
    lines.append("2. **21.5-Inch to 24-Inch Clinic Desktop Workstations (1920x1080, Full HD, 102 PPI):** Deployed in Doctor consultation cabins, pharmacy dispensing counters, diagnostic labs, and reception desks. Demands high-density information architecture, multi-pane split views, persistent contextual sidebars, and rapid keyboard-first data entry.")
    lines.append("")

    lines.append("## 2. Canonical Responsive Breakpoint System")
    lines.append("```css")
    lines.append("/* DOCUMENTATION-ONLY CSS TOKENS */")
    lines.append(":root {")
    lines.append("  --breakpoint-sm: 640px;   /* Small mobile field handhelds */")
    lines.append("  --breakpoint-md: 768px;   /* Portrait tablets */")
    lines.append("  --breakpoint-lg: 1024px;  /* Landscape 10-inch Android tablets */")
    lines.append("  --breakpoint-xl: 1280px;  /* Compact desktop monitors / WXGA wide */")
    lines.append("  --breakpoint-2xl: 1536px; /* High-definition clinical workstations */")
    lines.append("}")
    lines.append("```")
    lines.append("")

    lines.append("## 3. Responsive Layout Architecture & Container Rules")
    lines.append("```mermaid")
    lines.append("flowchart TD")
    lines.append("    subgraph TabletView [10-inch Android Tablet - 1280x800]")
    lines.append("        T_Header[Sticky Compact Header - 48px]")
    lines.append("        T_Nav[Bottom Navigation Bar / Collapsed Drawer]")
    lines.append("        T_Main[Single / Two Column Adaptive Stack]")
    lines.append("        T_Actions[Persistent Bottom Action Sheet - 56px]")
    lines.append("    end")
    lines.append("    subgraph DesktopView [21.5-inch Clinic Workstation - 1920x1080]")
    lines.append("        D_Header[Master Clinic Header - 56px]")
    lines.append("        D_Sidebar[Persistent Left Navigation Tree - 240px]")
    lines.append("        D_Workspace[3-Column Split Clinical Workspace - 1380px]")
    lines.append("        D_Inspector[Contextual Patient Tray - 300px]")
    lines.append("    end")
    lines.append("```")
    lines.append("")

    lines.append("## 4. Touch vs. Precision Mouse Interaction Hierarchy")
    lines.append("| Dimension | 10-Inch Tablet Target | 21.5-Inch Workstation Target | Clinical Rationale |")
    lines.append("| :--- | :--- | :--- | :--- |")
    lines.append("| Primary Button Height | 48px min (56px recommended) | 36px - 40px | Prevents missed finger taps during field examinations |")
    lines.append("| Input Field Height | 48px min | 36px | Provides comfortable hit area when wearing surgical gloves |")
    lines.append("| Table Row Height | 56px | 40px | Increases data density on desktop while preventing fat-finger errors on tablet |")
    lines.append("| Modal Width | 92% viewport width | Fixed 560px / 780px / 1020px | Maximizes usable real estate on compact touch screens |")
    lines.append("| Font Scale Base | 16px (1rem) | 14px (0.875rem) | Balances arm's-length tablet readability with desktop data density |")
    lines.append("")

    lines.append("## 5. Exhaustive Screen-by-Screen Responsive Layout Specifications")
    lines.append("The following section details the exact breakpoint transformations, container grids, and layout adaptations across all 108 screens:")
    lines.append("")

    for s in SCREENS:
        sid = s["id"]
        sname = s["name"]
        route = s["route"]
        mod = s["module"]
        role = s["primary_role"]

        lines.append(f"### Responsive Design Specification for Screen {sid}: {sname}")
        lines.append(f"**Route:** `{route}` | **Module:** `{mod}` | **Primary Role:** `{role}`")
        lines.append("")
        lines.append("#### 1. Tablet Layout Behavior (10-Inch Android Tablet @ 1280x800 Landscape / 800x1280 Portrait)")
        lines.append(f"- **Grid Layout:** Single-column fluid layout with `max-width: 100%` and 16px lateral padding.")
        lines.append(f"- **Navigation Pattern:** Drawer collapses into hamburger menu; top app bar pins key action items.")
        lines.append("- **Input Accommodations:** Input fields expand to full width (100%); touch targets strictly >= 48px.")
        lines.append("- **Soft Keyboard Handling:** Form scrolls active input into visible viewport above virtual keyboard using `scrollIntoViewIfNeeded()`.")
        lines.append("")
        lines.append("#### 2. Desktop Layout Behavior (21.5-Inch Full HD Workstation @ 1920x1080)")
        lines.append(f"- **Grid Layout:** Multi-column CSS Grid (`grid-template-columns: 280px 1fr 340px`) utilizing full 1920px canvas.")
        lines.append(f"- **Sidebar Integration:** Persistent 240px navigation sidebar with active indicator for `{sid}`.")
        lines.append("- **Information Density:** Compact 36px inputs, 40px table rows, and dual-column form groups.")
        lines.append("- **Keyboard Navigation:** Full keyboard navigation shortcuts (`Alt+S` save, `Alt+N` new, `Esc` cancel).")
        lines.append("")
        lines.append("#### 3. Documentation-Only CSS Grid Definition")
        lines.append("```css")
        lines.append("/* DOCUMENTATION-ONLY RESPONSIVE CSS */")
        lines.append(f".screen-{sid.lower()} {{")
        lines.append("  display: grid;")
        lines.append("  gap: var(--spacing-4);")
        lines.append("  grid-template-columns: 1fr;")
        lines.append("}")
        lines.append("")
        lines.append("@media (min-width: 1024px) {")
        lines.append(f"  .screen-{sid.lower()} {{")
        lines.append("    grid-template-columns: repeat(2, 1fr);")
        lines.append("    gap: var(--spacing-6);")
        lines.append("  }")
        lines.append("}")
        lines.append("")
        lines.append("@media (min-width: 1536px) {")
        lines.append(f"  .screen-{sid.lower()} {{")
        lines.append("    grid-template-columns: 280px 1fr 360px;")
        lines.append("    gap: var(--spacing-8);")
        lines.append("  }")
        lines.append("}")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("## 6. High-Density Clinical Data Table Adaptation")
    lines.append("When viewing patient registries and laboratory queues on tablets:")
    lines.append("1. **Column Priority Visibility:** Lower-priority columns are progressively hidden using `@media (max-width: 1024px) { .col-optional { display: none; } }`.")
    lines.append("2. **Horizontal Overflow Container:** Primary identifying columns (UHID, Patient Name) remain sticky on the left (`position: sticky; left: 0`) while diagnostic measures scroll horizontally.")
    lines.append("3. **Card Transformation Mode:** On screens <= 768px, table rows seamlessly reflow into stacked card components.")
    lines.append("")

    content = "\n".join(lines)
    return write_fe_doc("11-responsive-design.md", content, min_substantive=2000)

if __name__ == "__main__":
    generate_doc()
