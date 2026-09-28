# FORESIGHT - Local Foundation Build Plan

This plan outlines the steps to build the parallel, local, SAP-independent foundation for FORESIGHT, ensuring we don't block on live SAP environment verification while perfectly preserving the architecture.

## Milestone 1: Repository Structure & CAP Foundation
*   Scaffold the repository directories: `sap-cap-backend`, `sap-ui5-frontend`, `agent-orchestration`, `optimization`, `mock-s4hana`, `tests`.
*   Initialize the SAP CAP project in `sap-cap-backend` with SQLite.
*   Define core CDS entities (`Disruption`, `Supplier`, `Material`, `Plant`, `Inventory`, `RecoveryPlan`, `AgentAction`, `Approval`, `Commitment`, `AuditEvent`).
*   Expose clean OData V4 services and action endpoints.
*   Seed realistic deterministic demo data for the supplier failure scenario (CSV files).
*   *Git Commit & Push*

## Milestone 2: Mock S/4 Adapter
*   Create a standalone `mock-s4hana` Node.js express app (or integrated CAP service) implementing the rigid S/4HANA interface.
*   Implement endpoints for material, supplier, inventory, and order lookups.
*   Implement transaction simulation endpoints (PO/STO creation).
*   *Git Commit & Push*

## Milestone 3: Agent Orchestration (Python)
*   Set up a Python environment in `agent-orchestration` with Pydantic for strict typing.
*   Implement provider interfaces (LLMProvider, S4Adapter, etc.) with mock/deterministic implementations.
*   Develop the agents: `DisruptionAgent`, `ProcurementAgent`, `InventoryAgent`, `LogisticsAgent`, `ProductionAgent`, `RiskAgent`, and `OrchestratorAgent`.
*   Implement the parallel execution engine (`asyncio`) ensuring all specialized agents run concurrently against a shared state context.
*   *Git Commit & Push*

## Milestone 4: Optimization & Policy Control (Python)
*   Implement the `optimization` module using OR-Tools (CP-SAT) to evaluate feasible recovery plans against hard constraints (capacity, budget, deadlines).
*   Implement a deterministic Monte Carlo simulator for uncertainty modeling.
*   Implement local Policy and Commitment Control logic (budget thresholds, risk bounds).
*   Implement Saga-style recovery logic (Intent -> Hold -> Validate -> Commit -> Monitor, plus compensation).
*   *Git Commit & Push*

## Milestone 5: Frontend Foundation
*   Initialize the UI5 project in `sap-ui5-frontend`.
*   Build the initial Decision Console view displaying the disruption context, parallel agent recommendations, optimization metrics, policy statuses, and the Approval action.
*   Connect the UI to the local CAP OData service.
*   *Git Commit & Push*

## Milestone 6: Testing & E2E Verification
*   Implement unit and integration tests across Python and Node.js layers.
*   Execute the full simulated scenario locally: Event -> Agents -> Optimization -> Policy -> Approval -> Mock S/4 Transaction -> Audit.
*   Generate a Verification Report artifact.
*   *Git Commit & Push*
