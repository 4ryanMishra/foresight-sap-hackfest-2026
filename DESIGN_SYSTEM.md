# FORESIGHT Enterprise Design System

## 1. Design Philosophy
FORESIGHT is an enterprise-grade Decision and Commitment Control Plane for Autonomous Supply Chains. The design language is strictly **Light Mode**, engineered for operational precision, high information density, calm authority, and zero startup fluff.

It feels native to an SAP enterprise landscape (compatible with SAP Fiori Horizon conventions) while offering the bespoke precision of an advanced industrial control console.

---

## 2. Core Foundations

### 2.1 Surfaces & Canvas (Light Mode Only)
- **Canvas / App Background:** `#f8fafc` (Warm neutral off-white / slate-50)
- **Primary Surface (Cards, Panels, Tables):** `#ffffff` (Pure white)
- **Secondary Surface (Sidebars, Nested Panels, Headers):** `#f1f5f9` (Slate-100)
- **Tertiary Surface (Table headers, Inactive chips, Hover states):** `#e2e8f0` (Slate-200)
- **Borders & Dividers:** `1px solid #e2e8f0` (Subtle, non-distracting)
- **Selected / Focused Borders:** `1px solid #0284c7` (Sky-600) or `1px solid #0f766e` (Teal-700)
- **Shadows:** Minimal elevation only.
  - Card/Panel: `0 1px 3px 0 rgba(15, 23, 42, 0.05), 0 1px 2px -1px rgba(15, 23, 42, 0.05)`
  - Floating Popover/Modal: `0 4px 6px -1px rgba(15, 23, 42, 0.08), 0 2px 4px -2px rgba(15, 23, 42, 0.05)`

### 2.2 Typography
- **Font Family:** `72`, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif
- **Scale & Weights:**
  - **App Title / Page Heading:** 18px (1.125rem), Weight 600, Color `#0f172a`
  - **Section Title / Panel Header:** 14px (0.875rem), Weight 600, Color `#1e293b`
  - **Primary Data Value / KPI Metric:** 20px - 24px, Weight 600, Tabular Numbers
  - **Body / Primary Text:** 13px (0.8125rem), Weight 400, Color `#334155`
  - **Labels / Metadata / Table Headers:** 11px - 12px, Weight 600, Uppercase tracking +0.03em, Color `#64748b`
  - **Code / Monospace / Transaction IDs:** 12px, `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`, Color `#0f172a`

### 2.3 Semantic Palette
Every color communicates concrete operational state—never decorative noise:
| Semantic State | Color Code | Background Tint | Border Tint | Usage |
| :--- | :--- | :--- | :--- | :--- |
| **Disrupted / Critical** | `#dc2626` (Red-600) | `#fef2f2` (Red-50) | `#fecaca` (Red-200) | Outages, stockout alerts, infeasible plans |
| **Warning / Attention** | `#d97706` (Amber-600) | `#fffbeb` (Amber-50) | `#fde68a` (Amber-200) | Human approval required, medium risk, SLA near limit |
| **Healthy / Feasible / Approved** | `#0f766e` (Teal-700) | `#f0fdfa` (Teal-50) | `#99f6e4` (Teal-200) | Optimal plans, verified suppliers, passed policies |
| **Active / Informational / SAP** | `#1d4ed8` (Blue-700) | `#eff6ff` (Blue-50) | `#bfdbfe` (Blue-200) | Active routes, current selections, ERP link |
| **Neutral / Muted** | `#64748b` (Slate-500) | `#f8fafc` (Slate-50) | `#e2e8f0` (Slate-200) | Completed historical steps, inactive options |

---

## 3. Shape & Density System

- **Corner Radii:**
  - Panels & Cards: `6px` (Strictly restrained, no bubbly 16px/24px pill cards)
  - Badges & Status Tags: `4px`
  - Input Fields & Buttons: `4px`
- **Spacing Scale:**
  - 4px, 8px, 12px, 16px, 20px, 24px
- **Layout Architecture:**
  - 100% viewport fit with internal scroll containers for high-density monitoring.
  - Multi-column grid: 
    - Shell Nav: Top compact header + sub-navigation tabstrip
    - System KPI Strip: 48px height compact metrics
    - Main split workspace: 60% operational graph & flow / 40% decision & commitment console
    - Lower drawer: Real-time parallel agent activity log & Saga compensation trace

---

## 4. Component Standards

### 4.1 Shell Navigation
- Single line top-header with system identifier, practice environment badge (`SAP BTP / S/4HANA Adapter: LOCAL_MOCK`), and user persona (`Supply Chain Operations Executive`).
- 8 Primary tabs:
  1. `Overview` (Decision Console)
  2. `Disruptions` (Active Incidents)
  3. `Network` (Topology & Dark Pool)
  4. `Agents` (Swarm Execution Telemetry)
  5. `Recovery Plans` (Comparative Optimizer)
  6. `Simulation` (Monte Carlo & Stress Test)
  7. `Execution` (Saga Process Timeline)
  8. `Audit` (Governance Log)

### 4.2 Network Topology Visualization
- Clean enterprise SVG/Canvas rendering.
- Visual node hierarchy:
  - Suppliers (`[SUP-001]`, `[SUP-002]`, `[SUP-003: OUTAGE]`)
  - Materials (`[MAT-100: Microcontroller X]`)
  - Plants (`[PLANT-A: Primary]`, `[PLANT-B: Depot]`)
  - Logistics Corridors (Normal Overland, Disrupted Sea Freight, Expedited Air)
  - Commitments (`[PRD-1001: Assembly]`, `[CUST-882: Tier 1 Customer Order]`)
- Distinct state indicators on nodes: Healthy (green rim), Disrupted (red pulse rim, hatch pattern), Alternative (blue dashed).

### 4.3 Decision & Commitment Gate
- Structured recovery comparison cards (Plan A - Recommended Balanced, Plan B - Fast Air Expedite, Plan C - Internal Transfer Only).
- Commitment Risk gauge: `Cost + Service Impact + Operational Risk + Commitment Risk`.
- Policy-as-Code checklist with clear audit verification badges.
- Enterprise action controls: Primary "Approve Recovery Plan" (Teal/Navy solid), Secondary "Simulate Alternatives", Danger "Reject & Trigger Replan".

### 4.4 Operational Agent Telemetry (No Chat Bubbles!)
- High-density parallel event stream with millisecond timestamps, agent badge, action verb, and quantitative findings.
- Color-coded agent glyphs:
  - `[PROC]` Procurement Agent (Teal)
  - `[INVT]` Inventory Agent (Blue)
  - `[LOGI]` Logistics Agent (Indigo)
  - `[PROD]` Production Agent (Purple)
  - `[RISK]` Risk & Compliance Agent (Amber)
  - `[OPTM]` CP-SAT Solver (Slate)

### 4.5 Saga Process Tracker
- Visual step progression:
  `[Intent] → [Temporary Hold] → [Policy Validation] → [Human Approval] → [SAP Commit] → [Active Monitor]`
- Compensation branches clearly visualized for recovery paths.
