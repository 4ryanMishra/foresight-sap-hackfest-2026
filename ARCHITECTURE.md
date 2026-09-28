# FORESIGHT - Resilient Supply Chain Architecture

## 1. Product Vision & Core Problem
Modern enterprises deploy autonomous AI agents across procurement, inventory, logistics, and planning. However, these agents often make individually reasonable decisions that become collectively infeasible or harmful because they lack a coordinated view of supply-chain dependencies, business constraints, and existing commitments.

**FORESIGHT is a Decision and Commitment Control Plane for Autonomous Supply Chains.** It does not replace SAP, S/4HANA, Joule, or enterprise agents. Instead, it coordinates autonomous decisions and governs the transition from AI recommendation to real enterprise commitment.

### 1.1 The Core Mental Model
The FORESIGHT execution loop is:
**SEE → UNDERSTAND → COLLABORATE → SIMULATE → COMMIT → RECOVER**

### 1.2 Business Objective & Commitment Risk
FORESIGHT does not optimize solely for the lowest cost. The conceptual decision objective accounts for:
`Cost + Service Impact + Operational Risk + Working Capital + Commitment Risk`

**Commitment Risk** is a proposed FORESIGHT concept defined as: 
*Probability of failure × cost of irreversibility*.

## 2. Five Major Intelligence Capabilities

1. **Zero-Trust Reality Engine (SEE/UNDERSTAND)**: Determines if a disruption is real before triggering expensive actions using multi-source evidence fusion and anomaly detection. 
2. **Supply Chain Knowledge Graph + Industrial Dark Pool (UNDERSTAND)**: Represents suppliers, materials, plants, and dependencies as a connected graph. The Industrial Dark Pool is a privacy-aware mechanism for discovering compatible idle capacity before creating new external supply.
3. **Multi-Agent Swarm + Dynamic BOM (COLLABORATE)**: Specialized, structured tool-calling agents (Procurement, Inventory, Logistics, Production, Risk) operate on shared state. Production Agents can evaluate approved alternative BOMs under engineering constraints.
4. **Simulation + Collective Intelligence (SIMULATE)**: Candidate recovery plans are tested against uncertainty using Monte Carlo simulation, constraint solving, and agent-based game-theoretic reasoning to evaluate second-order effects.
5. **Safe Execution / Commitment Control (COMMIT/RECOVER)**: Evaluates business policies, financial constraints, and commitment exposure before execution. Uses Policy-as-Code, human approval for high-risk decisions, and Saga-style compensating actions for recovery.

### 2.1 The Commitment Graph
In addition to the physical Supply Chain Knowledge Graph, FORESIGHT introduces a **Commitment Graph** to reason about business commitments:
`Purchase Requisition → Purchase Order → Reservation → Freight/Transportation → Production Order → Delivery → Customer Commitment`
FORESIGHT asks: *"What business commitments will this decision create?"*

## 3. Latency Architecture
FORESIGHT is an event-driven, asynchronous, parallel architecture. Independent agents execute concurrently. Knowledge-graph state is reusable. Simulations are selective. 
**Core Principle**: *"We do not add five waiting rooms. We add five parallel intelligence layers and one controlled commitment gate."* Only dependency-critical validation blocks final commitment.

## 4. SAP-First Architecture
SAP is the enterprise execution environment, not a logo on a Python application. SAP-native technologies are used for SAP-native concerns.

*   **SAP S/4HANA**: Business data and actual ERP transaction execution (where verified).
*   **SAP BTP / CAP**: The SAP-facing application and service layer. Exposes FORESIGHT entities and choreographs drafts/approvals.
*   **SAP HANA Cloud**: FORESIGHT-specific persistence (Disruption, RecoveryPlan, AuditEvent).
*   **SAPUI5 / Fiori**: Enterprise decision console for human-in-the-loop approval.
*   **SAP Build Work Zone**: Enterprise application entry point (where available).
*   **SAP AI Launchpad / Generative AI Hub**: Governed LLM access (where verified).
*   **SAP Integration Suite / Event Mesh**: Event-driven integration (where verified).
*   **Python Runtime**: Dedicated exclusively to agent orchestration, graph analysis, mathematical optimization, and simulation. The Antigravity SDK is a development tool only and is **not** a runtime dependency.

## 5. Repository Architecture

```text
foresight-sap-hackfest-2026/
├── sap-cap-backend/         # SAP CAP Model (Node.js/Java) & SAP HANA Cloud
│   ├── app/                 # Fiori / SAPUI5 configurations (Decision Console)
│   ├── db/                  # CDS Data Models (Source of truth for FORESIGHT entities)
│   ├── srv/                 # Service Definitions & S/4HANA Adapter routing
│   └── mock-s4hana/         # Realistic mock service for unverified/unavailable S/4 APIs
├── sap-ui5-frontend/        # SAPUI5 App (Enterprise UI / Inbox)
│   └── webapp/              # UI5 source code
├── agent-runtime/           # Python Agent Reasoning Layer
│   ├── agents/              # Swarm: Procurement, Logistics, Risk, Inventory, Production
│   ├── intelligence/        # Zero-Trust Reality, Graph traversal, Simulation math
│   └── core/                # Clean LLM orchestration (routing to SAP Gen AI Hub)
├── mta.yaml                 # BTP Deployment configuration
└── docs/                    # Architecture and integration documentation
```

## 6. MVP vs. Advanced Extensions Boundary
The mandatory working vertical slice MVP focuses strictly on one thin thread through the five pillars:
*Supplier failure → disruption sensing → impact analysis → parallel swarm (procurement/inventory/logistics/risk) → feasible recovery plan → business-policy/commitment validation → human approval → SAP/mock-SAP transaction → audit trail.*

Advanced features (Zero-Trust Reality Engine, Dark Pool, Dynamic BOM, Game-Theoretic Simulation, full Saga recovery) are explicit extensions layered progressively and must never block the MVP.

## 7. No-Hallucination SAP Rules
1. **Never Invent APIs**: Every SAP capability, API, business object, service, and permission is treated as **UNKNOWN** until explicitly verified in the actual SAP practice environment.
2. **Never Claim Untested Integrations**: If an integration has not been tested against a live system, it must be documented as simulated or mocked.
3. **S/4HANA is an Adapter**: S/4HANA is treated as an integration adapter. The architecture supports switching between verified live S/4HANA APIs and a realistic mock S/4 service with the exact same contract.
