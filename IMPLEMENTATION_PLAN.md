# FORESIGHT - Implementation Plan

## 1. The Core MVP: Mandatory Working Vertical Slice
Do NOT attempt to fully implement every advanced research capability. The project must first demonstrate a single, genuinely working vertical slice that proves the core architecture (AI proposes → Knowledge grounds → Optimization checks → Policy enforces → Human approves → SAP executes).

**The Slice:**
1.  **Disruption Sensing**: An HTTP POST triggers a supplier failure event in the CAP backend.
2.  **Impact Analysis**: The Python agent runtime queries the basic Supply Chain Graph (via CAP/mock-S4) to identify impacted orders and materials.
3.  **Parallel Agent Swarm**: Procurement, Inventory, Logistics, and Risk agents run concurrently to evaluate alternatives (find new suppliers, check stock, evaluate freight, verify compliance).
4.  **Feasible Recovery Plan**: A central optimization script (Python) evaluates the swarm's findings and generates a plan balancing Cost, Service Impact, and Commitment Risk.
5.  **Policy/Commitment Validation**: The plan is checked against the Commitment Graph (e.g., ensuring we don't violate a top-tier customer delivery).
6.  **Human Approval**: The `RecoveryPlan` is persisted as a draft in HANA. A human logs into the UI5 app to review the plan and clicks "Approve".
7.  **SAP/Mock-SAP Transaction**: The CAP action handler routes the approved transaction to the verified S/4HANA APIs (or the rigid mock adapter).
8.  **Audit Trail**: An `AuditEvent` is written to HANA Cloud.

## 2. Advanced Extensions (Non-Blockers)
These features represent the full product vision but are explicitly excluded from blocking the MVP. They will be layered progressively:
*   **Zero-Trust Reality Engine**: Multi-source Bayesian anomaly detection to verify the disruption before acting.
*   **Industrial Dark Pool**: Cross-enterprise privacy-aware idle inventory matching.
*   **Dynamic BOM Reconfiguration**: The Production agent evaluating engineering-approved component substitutions.
*   **Game-Theoretic Simulation**: Simulating collective behavior (e.g., what happens if all companies rush to the same alternative port).
*   **Saga-Style Recovery**: Automated compensating transactions if reality changes post-commitment.
*   **SAP Event Mesh**: Native pub/sub event consumption.

## 3. Phase 1 Build Plan (Foundation & SAP Source of Truth)
Phase 1 focuses entirely on establishing the SAP CAP/HANA layer as the strict source of truth for the Decision Control Plane.

*   **Step 1.1**: Initialize the SAP CAP project (`sap-cap-backend`).
*   **Step 1.2**: Define the CDS Data Models representing the Control Plane state: `Disruption`, `RecoveryPlan`, `AgentAction`, `Approval`, `Commitment`, and `AuditEvent`.
*   **Step 1.3**: Implement the OData V4 services exposing these entities, specifically configuring Draft choreography for the `RecoveryPlan` to support the Human Approval gate.
*   **Step 1.4**: Scaffold the SAPUI5/Fiori Elements application on top of the CAP OData service to serve as the Decision Console.
*   **Step 1.5**: Deploy to local SQLite and verify the manual creation, drafting, and approval of a `RecoveryPlan` without any AI involvement yet.

## 4. Phase 2 Build Plan (S/4HANA Adapter & Mocking)
*   **Step 2.1**: Define the rigid integration contracts expected from S/4HANA (e.g., fetching a material, reading stock, creating a PO).
*   **Step 2.2**: Build the `mock-s4hana` service locally that perfectly implements this contract.
*   **Step 2.3**: Implement the CAP routing logic to direct S/4 queries to either the destination service or the local mock.

## 5. Phase 3 Build Plan (Python Agent Runtime & Parallel Latency)
*   **Step 3.1**: Establish the clean Python runtime environment (No Antigravity SDK).
*   **Step 3.2**: Implement the parallel execution framework ensuring agents do not run as sequential waiting rooms.
*   **Step 3.3**: Implement the basic Supply Chain Knowledge Graph state management.
*   **Step 3.4**: Build the Procurement, Inventory, Logistics, and Risk structured tool-calling agents.
*   **Step 3.5**: Integrate with SAP Generative AI Hub API via standard REST clients.

## 6. Phase 4 Build Plan (Integration & Live SAP Environment Verification)
*   **Step 4.1**: Connect the Python runtime to the local CAP instance and run the end-to-end simulated trigger.
*   **Step 4.2**: Execute manual environment checks in the SAP practice system (see Manual Verification list).
*   **Step 4.3**: Switch S/4HANA adapters from mock to verified live APIs via BTP Destinations.
*   **Step 4.4**: Deploy CAP/UI5 to SAP BTP.
