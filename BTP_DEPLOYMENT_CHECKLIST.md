# SAP BTP DEPLOYMENT CHECKLIST

This document outlines the structural steps required to transition the FORESIGHT CAP application and Python Orchestrator from local development to the SAP Business Technology Platform (BTP).

## 1. SAP CAP Backend Readiness

The CAP backend (`sap-cap-backend`) is currently built with SQLite and mock endpoints. It requires the following updates for BTP deployment:

- [ ] **MTA Configuration**: Generate the `mta.yaml` descriptor file using `cds add mta`. This file orchestrates the deployment of the CAP service, HANA DB, and UI5 app module.
- [ ] **SAP HANA Cloud Integration**: 
    - Run `cds add hana` to configure the `@cap-js/hana` database adapter.
    - Update `package.json` `cds.requires.db` to switch from SQLite to HANA in the production profile.
- [ ] **Authentication & Authorization**:
    - Run `cds add xsuaa` to provision an XSUAA instance.
    - Bind the XSUAA instance in `mta.yaml`.
    - Apply `@requires: 'authenticated-user'` (or specific scopes like `SC_Ops_Executive`) in `srv/service.cds` to restrict OData operations.
- [ ] **Destination Service**:
    - Add `cds.requires.S4HANA_DEST` in `package.json`.
    - Bind the Destination service instance in `mta.yaml` so CAP can route API calls to the target S/4HANA system securely.
- [ ] **UI Deployment Module**:
    - Add an Approuter module or standard SAP Build Work Zone / HTML5 Application Repository configurations to serve the `sap-ui5-frontend` from BTP natively instead of `express.static`.

## 2. Python Orchestrator Readiness

The Python orchestration layer runs FastAPI and contains the agent swarm.

- [ ] **Dockerization**: Create a `Dockerfile` for `agent_orchestration`.
- [ ] **Cloud Foundry Deployment**: Define the Python app in `mta.yaml` as a separate module, or deploy as an independent CF app/Kyma workload.
- [ ] **Internal Routing**: Ensure CAP can securely call the Python service. If both are on BTP Cloud Foundry, use internal routes or BTP Destination Service to bridge CAP and Python.
- [ ] **SAP Generative AI Hub Integration**: 
    - Implement the SAP AI Core SDK within the `LLMProvider` interface.
    - Bind the SAP AI Core service credentials via BTP environment variables (`VCAP_SERVICES`) to the Python module.

## 3. SAP Event Mesh Readiness

- [ ] **Service Provisioning**: Provision an instance of SAP Event Mesh in the BTP subaccount.
- [ ] **Event Topics**: Define and document standard S/4HANA event topics (e.g., `sap/s4/beh/businesspartner/v1/BusinessPartner/Changed/v1`).
- [ ] **CAP Subscription**: Update CAP `package.json` to include `@sap/xb-msg-amqp-v100` and configure `cds.requires.messaging`.
- [ ] **Event Handlers**: Bind incoming Event Mesh topics to the existing `/triggerDisruption` CAP logic.

## 4. CI/CD & Migration Commands

*   Build the deployment archive: `mbt build`
*   Deploy to BTP Cloud Foundry: `cf deploy mta_archives/foresight_1.0.0.mtar`
