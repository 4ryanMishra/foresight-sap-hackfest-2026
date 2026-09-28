# FORESIGHT SAP Migration Checklist

This document details the exact readiness state for migrating the FORESIGHT Decision Console from its current local mocked environment to a live SAP practice landscape (S/4HANA, BTP, SAP Generative AI Hub).

## 1. Current State Assessment

### 🟢 LIVE NOW (Local & Isolated)
- **SAP CAP Backend (OData V4)**: Fully functional, serving the UI statically, handling complex SAGA transactions (Reject/Compensate), tracking `AgentAction` and `AuditEvent` telemetry.
- **Python Agent Orchestrator**: Executes parallel LLM/optimization logic via FastAPI. 
- **SAPUI5 Frontend**: Fully wired Decision Console built with Fiori design principles.
- **SQLite Persistence**: Local lightweight database for rapid development.
- **Deterministic AI Fallbacks**: `MockLLMProvider` currently ensures reproducible testing while prompt engineering stabilizes.

### 🟡 MOCKED NOW (Requires Migration)
- **S/4HANA Adapter**: Currently hitting `mock-s4hana/index.js` which simulates APIs (e.g., `API_PURCHASEORDER_PROCESS_SRV`).
- **Authentication**: Currently open (no XSUAA/JWT required) to facilitate local testing.
- **Eventing/Triggering**: Currently triggered manually via `/triggerDisruption` endpoint.

### 🔴 REQUIRES SAP VERIFICATION (The "Unknowns")
- **Live S/4HANA APIs**: Wait for confirmation that standard OData APIs (e.g., `API_BUSINESS_PARTNER`) are available and reachable.
- **SAP Event Mesh**: Wait for confirmation on the topic structure for S/4HANA Supplier/Material events.
- **SAP Generative AI Hub**: Wait for API Keys and deployment IDs for `gpt-4o` or similar models.
- **BTP Destination Service**: Wait for credentials to securely connect CAP to the on-premise/cloud S/4 instance.

---

## 2. Migration Checklist

### A. S/4HANA Integration
- [ ] **Verify APIs**: Test standard SAP APIs on the target S/4 system via Postman or SAP API Business Hub.
- [ ] **Configure SAP Destination**: Set up the S/4HANA destination in SAP BTP.
- [ ] **Update CAP**: Replace `axios` direct calls in `service.js` with SAP Cloud SDK `cds.connect.to('S4HANA_DESTINATION')`.

### B. AI & Orchestration Integration
- [ ] **Implement SAP AI Core Provider**: Create `SapGenAiHubProvider(LLMProvider)` in `agent_orchestration/interfaces.py` using the SAP Generative AI Hub SDK.
- [ ] **Update Credentials**: Inject Generative AI Hub credentials via BTP service bindings.
- [ ] **Verify Throughput**: Test concurrent swarm execution against rate limits of the Generative AI Hub.

### C. Eventing Integration (Optional for MVP, Highly Recommended)
- [ ] **Provision SAP Event Mesh**: Create service instance and queues.
- [ ] **Subscribe in CAP**: Add `cds.requires.messaging` to `package.json` and consume Supplier Failure events natively in `service.js`.

### D. Production Deployment (BTP & HANA)
- [ ] **Generate MTA Descriptor**: Run `cds add mta` to create the `mta.yaml`.
- [ ] **Add HANA Support**: Run `cds add hana` to switch from SQLite to SAP HANA Cloud.
- [ ] **Add Authentication**: Run `cds add xsuaa` to secure endpoints.
- [ ] **Deploy**: `mbt build` and `cf deploy`.
