# FORESIGHT - Implementation Plan

## 1. Exact MVP Scope
For the SAP Hackfest 2026, the MVP will demonstrate a critical supply chain disruption scenario.

**Scenario**: A key supplier for "Material X" (e.g., a specialized electronic component) experiences a sudden failure (e.g., natural disaster, cyberattack).
**End-to-End Flow**:
1.  **Disruption Sensing**: An external trigger (simulated via API call) notifies the system of the supplier failure.
2.  **Impact Analysis**: The system queries S/4HANA (via CAP) to identify affected Purchase Orders, current inventory levels across plants, and dependent Production Orders.
3.  **Parallel Agent Execution**:
    *   *Procurement Agent*: Identifies alternative suppliers in S/4HANA (`API_SUPPLIER`), evaluates lead times and historical reliability.
    *   *Inventory Agent*: Checks stock at other plants (`API_MATERIAL_STOCK_SRV`) for potential internal transfers.
    *   *Logistics Agent*: Calculates expedited shipping options and costs.
    *   *Risk Agent*: Validates that alternative suppliers meet enterprise compliance and risk thresholds.
4.  **Optimization**: An Orchestrator Agent synthesizes the findings and formulates the optimal mitigation plan (e.g., transfer 20% from Plant B, expedite PO for 80% from Supplier Y).
5.  **Business Policy & Commitment Validation**: The system ensures the plan adheres to business rules (e.g., budget limits, SLA commitments).
6.  **Human Approval**: The proposed plan is surfaced in a SAPUI5/Fiori Inbox. The Supply Chain Manager reviews the plan, explains the AI's reasoning, and clicks "Approve".
7.  **SAP Transaction (S/4HANA)**: The CAP backend securely executes the approved transactions in S/4HANA (e.g., creating a new PO and an internal Stock Transport Order).
8.  **Audit Trail**: The entire decision-making process, including agent reasoning and human approval, is persisted in SAP HANA Cloud for auditability.

## 2. Phased Implementation Strategy

### Phase 1: Foundation (Local Environment)
*   **Initialize CAP Project**: Scaffold the Node.js CAP backend (`cds init sap-cap-backend`).
*   **Data Modeling**: Define core CDS entities (`schema.cds`) for the `MitigationPlan`, `AgentAction`, and `AuditLog`.
*   **Local Persistence**: Configure SQLite for local testing (`cds watch`).
*   **UI Foundation**: Generate a Fiori Elements App linked to the `MitigationPlan` OData V4 service.
*   **Agent Foundation**: Setup a Python virtual environment, install agent frameworks (e.g., LangChain/Google Antigravity SDK), and define the basic Orchestrator and Specialist Agent classes.

### Phase 2: Integration & API Definition
*   **S/4HANA API Contracts**: Import S/4HANA EDMX metadata for the necessary standard APIs (`API_PURCHASEORDER_PROCESS_SRV`, `API_MATERIAL_STOCK_SRV`, etc.).
*   **Mock S/4HANA**: Implement mock service handlers in CAP (`srv/external-mock.js`) to return realistic SAP data during local development.
*   **Agent ↔ CAP Integration**: Define custom actions in CAP (e.g., `action proposePlan(payload: String)`) and build the Python tools necessary for the Agents to read from and write to these CAP endpoints.

### Phase 3: Agent Reasoning Layer (Python)
*   **Implement Tools**: Build Python functions that call the CAP backend to fetch inventory, supplier, and order data.
*   **Agent Logic**: 
    *   Implement the parallel execution logic for Procurement, Inventory, Logistics, and Risk agents.
    *   Implement the synthesis and optimization logic in the Orchestrator Agent.
*   **SAP Generative AI Hub Setup**: Configure the Python application to authenticate and route LLM requests through the SAP AI Core / Generative AI Hub endpoints.

### Phase 4: User Experience (SAPUI5/Fiori)
*   **Fiori Elements Configuration**: Use annotations (`annotations.cds`) to design a robust review UI (List Report + Object Page).
*   **Explainable AI UI**: Implement custom UI5 fragments/controls on the Object Page to visualize the agents' parallel reasoning process and the rationale behind the proposed plan.
*   **Approval Choreography**: Implement CAP Draft choreography to transition the plan from "Draft/Proposed" to "Approved" and trigger the backend execution logic.

### Phase 5: SAP Transaction & Audit
*   **S/4HANA Execution**: Implement the CAP logic to translate an "Approved" plan into concrete S/4HANA OData POST requests via the SAP Cloud SDK.
*   **Audit Logging**: Ensure all steps (sensing, agent reasoning, human approval) are committed to the SAP HANA Cloud database.

### Phase 6: BTP Deployment & Verification
*   **MTA Assembly**: Configure `mta.yaml` to bundle the CAP backend, UI5 frontend, HANA HDI container, AppRouter, and XSUAA.
*   **Deploy**: Build (`mbt build`) and deploy (`cf deploy`) to the SAP BTP space.
*   **Destinations**: Configure the BTP Destination service to point to the practice S/4HANA system and the SAP AI Launchpad.

## 3. Testing Strategy
*   **Unit Testing**: 
    *   *CAP*: Use Jest to test custom service handlers, formatting, and draft choreography logic locally.
    *   *Agent Layer*: Use PyTest to test individual tools and agent prompts using mocked LLM responses.
*   **Integration Testing**: 
    *   Use `.http` files or Postman collections to verify the OData V4 APIs exposed by CAP.
    *   Test the end-to-end local flow: Trigger event via API -> Agent generates plan via API -> CAP processes plan.
*   **E2E UI Testing**: (Optional for MVP) Use wdi5 to simulate a user logging into the Fiori Launchpad, navigating to the Inbox, and approving a plan.
*   **Agent Evaluation**: Run specific test cases against the agent layer to ensure it respects business constraints (e.g., "Do not select Supplier X if their risk score is > 80").

## 4. Deployment Strategy
*   **Local Development**: 
    *   CAP & UI5: `cds watch` (uses embedded SQLite and mock external services).
    *   Agent Layer: Local Python execution.
*   **BTP Staging / Demonstration**: 
    *   SAP Components (CAP, UI5, HANA, AppRouter): Packaged as an MTA (`.mtar`) and deployed to SAP BTP Cloud Foundry.
    *   Agent Layer (Python): Deployed to SAP BTP Cloud Foundry as a Python buildpack app, or hosted externally (e.g., Google Cloud Run) securely accessing BTP via OAuth client credentials.
    *   AI Hub: All LLM requests routed through SAP Generative AI Hub for enterprise compliance.
