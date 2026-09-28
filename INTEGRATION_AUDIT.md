# FORESIGHT Integration Audit (Phase 2.5)

**Date:** 2026-09-29
**Scope:** CAP ↔ Agent Orchestration ↔ Optimization ↔ Policy/Commitment ↔ Mock S/4 Adapter ↔ Frontend

## 1. Schema & Lifecycle Consistency Verification
- **Disruption Lifecycle:** `DETECTED` → `ANALYZING` → `PLAN_PROPOSED` → `RESOLVED`. Handled correctly in CAP `triggerDisruption`. Error states map to `FAILED`.
- **RecoveryPlan Lifecycle:** `DRAFT` → `PENDING_APPROVAL` → `APPROVED` → `EXECUTED`. The Python orchestrator sets the approval requirement (via PolicyService), which CAP honors when creating the plan.
- **Result:** Pass, with one mismatch identified in the rejection flow (see Mismatches).

## 2. Agent Output & Orchestrator Consumption
- **Agents:** Return lists of strongly-typed `AgentRecommendation` objects (defined in `models.py`).
- **Orchestrator/Optimizer:** `CpSatOptimizer` directly loops over these `AgentRecommendation` arrays.
- **Policy Engine:** `PolicyService` operates on the final `RecoveryPlan` dictionary produced by the Optimizer, shielding it from raw LLM output.
- **Result:** Pass.

## 3. Transaction Isolation & SAGA Compliance
- **Direct Execution Shielding:** Verified. The Python `BaseAgent` implementations and specific agents (`ProcurementAgent`, `InventoryAgent`) only compute properties and return recommendations. No external I/O occurs within agents.
- **S/4HANA Invocation Boundary:** Verified. The Mock S/4 REST POST is *only* called inside `sap-cap-backend/srv/service.js` inside the `approvePlan` event handler. 
- **Audit Trails:** Verified. CAP correctly emits `foresight.AuditEvent` for `DISRUPTION_TRIGGERED`, `PLAN_APPROVED`, `EXECUTION_SUCCESS`, and `EXECUTION_FAILED`.
- **Result:** Pass.

## 4. Contract Mismatches (To be resolved in Phase 3)

The following inconsistencies between the frozen UI (Commit `1eec925`) and the backend contracts must be addressed when wiring the UI:

1. **Telemetry Trace Persistence:**
   - *Frontend:* Uses a dedicated `telemetry` list mapping to individual agent execution steps (e.g., "CpSatOptimizer solved mixed-integer program...").
   - *Backend:* The Python orchestrator logs these to STDOUT, but does not return them to CAP, nor does CAP have a schema to store them.
   - *Resolution Required:* Either CAP needs an `AgentTelemetry` entity, or the frontend must rely on `AgentAction` instead.

2. **Rejection & Compensation Lifecycle:**
   - *Frontend:* The `.onReject()` handler displays a warning about initiating "SAGA Compensation & Re-plan" and releasing temporary holds.
   - *Backend:* CAP only implements `approvePlan(planId, approverId, comments)`. It lacks a `rejectPlan` endpoint to reverse the `PENDING_APPROVAL` state, release holds, and trigger replanning.
   - *Resolution Required:* Add `rejectPlan` action to CAP and `service.js`.

3. **Audit Event Mappings:**
   - *Frontend:* Expects `actor`, `type`, `evidence`, and `target`.
   - *Backend:* Uses `entityName`, `entityId`, `eventType`, and `details`.
   - *Resolution Required:* The OData UI5 model mapping needs to align `details` -> `evidence` and `entityName`/`entityId` -> `target`.

4. **Action Payload Mismatch:**
   - *Frontend / Prompt:* Refers to `RecoveryAction`.
   - *Backend:* Implements this as `foresight.AgentAction`.
   - *Resolution Required:* UI5 binding must query `AgentActions`.

## Summary
The backend vertical slice is fundamentally sound, fully decoupled, and rigorously isolates AI decision-making from S/4 execution. The discrepancies are strictly between the static UI mock data model and the final CAP OData metadata schema, which is typical for Phase 2 completion and will be wired smoothly in Phase 3.
