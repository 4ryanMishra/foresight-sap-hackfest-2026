# FORESIGHT - Resilient Supply Chain Architecture

## 1. Overview
FORESIGHT is an SAP-first, agentic AI prototype designed for the SAP Hackfest 2026. The application addresses critical supply chain disruptions (e.g., supplier failure, material shortage) through an autonomous, multi-agent reasoning layer integrated natively into the SAP ecosystem. 

The core end-to-end flow is:
**Disruption Event → Sensing → Impact Analysis → Parallel Agent Reasoning (Procurement, Inventory, Logistics, Production, Risk) → Optimization → Business Policy & Commitment Validation → Human Approval → SAP Transaction (S/4HANA) → Audit Trail → Compensation/Replan.**

## 2. Repository Architecture
The repository will be structured to support both local development and SAP BTP deployment:

```text
foresight-sap-hackfest-2026/
├── sap-cap-backend/         # SAP Cloud Application Programming (CAP) Model
│   ├── app/                 # Fiori Elements / SAPUI5 app configurations
│   ├── db/                  # CDS Data Models (schema.cds) & SAP HANA Cloud artifacts
│   ├── srv/                 # Service Definitions & Business Logic (service.cds, .js)
│   └── package.json         # Node.js dependencies
├── sap-ui5-frontend/        # Custom SAPUI5 Freestyle / Fiori Elements App (Enterprise UI)
│   ├── webapp/              # UI5 source code, views, controllers
│   └── ui5.yaml             # UI5 tooling configuration
├── agent-orchestration/     # Multi-Agent Reasoning Layer (Python)
│   ├── agents/              # Procurement, Logistics, Risk, Inventory Agents
│   ├── tools/               # Tools for querying CAP APIs & S/4HANA APIs
│   ├── core/                # LLM orchestration and workflow logic
│   └── requirements.txt     # Python dependencies
├── mock-s4hana/             # (Optional) Local mock server for S/4HANA OData APIs
├── mta.yaml                 # Multi-Target Application descriptor for BTP Deployment
└── docs/                    # Architecture and implementation documentation
```

## 3. SAP Capability Requirements
To implement FORESIGHT authentically within the SAP ecosystem, the following SAP BTP capabilities and services are required:

*   **SAP Business Application Studio (BAS)**: Primary IDE for CAP, UI5, and HANA development.
*   **SAP Cloud Application Programming Model (CAP)**: Core application layer (Node.js/Java) for defining OData V4 services, handling business logic, and choreographing actions.
*   **SAP HANA Cloud**: High-performance persistence layer for audit trails, caching, and custom app data via HDI Containers.
*   **SAPUI5 / SAP Fiori Elements**: Enterprise-grade UI framework for the human-in-the-loop approval inbox.
*   **SAP Build Work Zone / Launchpad Service**: Portal for accessing the Fiori application.
*   **SAP Destination & Connectivity Service**: Securely routing requests from the BTP environment to the S/4HANA system (Cloud or On-Premise).
*   **SAP S/4HANA**: The core digital core providing standard APIs (e.g., `API_PURCHASEORDER_PROCESS_SRV`, `API_MATERIAL_STOCK_SRV`, `API_SUPPLIER`).
*   **SAP AI Core / Generative AI Hub**: Centralized proxy and orchestration layer for interacting with LLMs securely, adhering to enterprise AI guardrails.

## 4. Components Implemented Locally
During rapid prototyping and early development, the following can be executed locally without requiring continuous BTP access:
*   **CAP Backend**: Running with an embedded **SQLite** database (`cds watch`) instead of SAP HANA Cloud.
*   **Agent Orchestration**: Running as a local Python process, interacting with local LLMs or direct API keys (before migrating to SAP Generative AI Hub).
*   **SAPUI5 Frontend**: Served locally using UI5 Tooling (`ui5 serve`), consuming the local CAP OData services.
*   **S/4HANA Integration**: Mocked locally within the CAP application or using a dedicated mock server to simulate S/4HANA OData V2/V4 responses.

## 5. Components Running in SAP BAS / BTP
The following components mandate deployment to SAP BTP for staging, integration testing, and the final Hackfest demonstration:
*   **SAP HANA Cloud HDI Containers**: Required for advanced HANA features and persistent storage.
*   **S/4HANA Connectivity**: Actual integration with the practice S/4HANA system using the BTP Destination service (which cannot easily be fully emulated locally without VPNs/Cloud Connectors).
*   **SAP Generative AI Hub Integration**: Routing the Agent Orchestration LLM calls through SAP's AI endpoints for compliance and auditing.
*   **BTP AppRouter & XSUAA**: For secure enterprise authentication and routing between the UI, CAP backend, and Agent layer.

## 6. Integration Contracts
The system relies on clear API boundaries between its primary tiers:

*   **UI5 Frontend ↔ CAP Backend**: Standard **OData V4**. CAP provides Draft choreography out-of-the-box for human-in-the-loop approvals (e.g., "Draft Plan" -> "Approved Plan").
*   **Agent Orchestration ↔ CAP Backend**: **REST / HTTP**. The agent layer queries the CAP backend to fetch current context (Sensing/Impact Analysis). The agent layer POSTs back optimization plans and proposed resolutions as JSON payloads to CAP custom action endpoints.
*   **Agent Orchestration ↔ SAP Generative AI Hub**: **REST (OpenAI API compatible)**. Agent framework communicates with SAP AI Core deployment endpoints.
*   **CAP Backend ↔ SAP S/4HANA**: Standard **OData V2/V4**. CAP uses destination-based routing (via `@sap-cloud-sdk/http-client` or CAP's remote service consumption) to execute the final transaction (e.g., creating a PO) once human approval is granted.
