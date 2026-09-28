# FORESIGHT - SAP Integration Matrix

## 1. No-Hallucination SAP Integration Rules
1. **Never Invent APIs**: Every SAP capability, API, business object, service, tenant capability, and permission is treated as **UNKNOWN** until explicitly verified in the actual SAP practice environment.
2. **Never Claim Untested Integrations**: If an integration has not been tested against a live system, it must be documented as simulated or mocked.
3. **S/4HANA is an Adapter**: S/4HANA is treated as an integration adapter. The architecture must support seamless switching between verified live S/4HANA APIs and a realistic mock S/4 service implementing the exact same contract.

## 2. SAP Capability Matrix

| Capability / API | Status | Evidence | Integration Method | Scope |
| :--- | :--- | :--- | :--- | :--- |
| **SAP CAP (Cloud Application Programming)** | [ ] UNKNOWN | Pending check in BAS | Node.js / CDS Deployment to BTP | MVP |
| **SAP HANA Cloud** | [ ] UNKNOWN | Pending HDI container creation | CAP `cds deploy` to HDI container | MVP |
| **SAP Fiori / SAPUI5** | [ ] UNKNOWN | Pending Fiori Elements generation | Served via AppRouter / BTP | MVP |
| **SAP Generative AI Hub** | [ ] UNKNOWN | Pending API key / destination check | REST API / Python SDK | MVP |
| **S/4HANA: Read Material/Stock** | [ ] UNKNOWN | Pending Postman/curl to practice S/4 | OData via BTP Destination / Mock Adapter | MVP |
| **S/4HANA: Read Supplier** | [ ] UNKNOWN | Pending Postman/curl to practice S/4 | OData via BTP Destination / Mock Adapter | MVP |
| **S/4HANA: Create PO/STO** | [ ] UNKNOWN | Pending Postman/curl to practice S/4 | OData via BTP Destination / Mock Adapter | MVP |
| **SAP Event Mesh** | [ ] UNKNOWN | Pending BTP Entitlements check | AMQP / Webhook | Extension |
| **SAP Build Work Zone** | [ ] UNKNOWN | Pending BTP Entitlements check | Launchpad Site Deployment | Extension |

## 3. S/4HANA Adapter Interface & Transaction Execution
The core philosophy is that SAP executes the actual ERP transactions. The CAP layer defines a strict `srv/external-s4.cds` interface. 
*   **Live Mode**: CAP routes requests through the BTP Destination service to the verified practice S/4HANA system.
*   **Mock Mode**: CAP routes requests to a local `mock-s4hana` service that responds with pre-seeded realistic supply chain data. 

The Python agent runtime will **only** ever communicate with the CAP layer, remaining completely agnostic to whether the underlying S/4HANA data is live or mocked.
