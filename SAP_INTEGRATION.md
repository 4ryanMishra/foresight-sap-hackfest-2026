# FORESIGHT - SAP Integration Matrix

## 1. No-Hallucination SAP Integration Rules
1. **Never Invent APIs**: Every SAP capability, API, business object, service, tenant capability, and permission is treated as **UNKNOWN** until explicitly verified in the actual SAP practice environment.
2. **Never Claim Untested Integrations**: If an integration has not been tested against a live system, it must be documented as simulated or mocked.
3. **S/4HANA is an Adapter**: S/4HANA is treated as an integration adapter. The architecture must support seamless switching between verified live S/4HANA APIs and a realistic mock S/4 service implementing the exact same contract.

## 2. SAP Integration Status (Phase 4 Updates)

| Component | Status | Description |
| :--- | :--- | :--- |
| **BAS (SAP Business App Studio)** | ✅ VERIFIED | Full Stack Cloud Application Dev Space verified. |
| **HANA Cloud / DB** | ✅ VERIFIED | SAP HANA Cloud instance `Hackfest-DB` verified. HDI deployer generated. |
| **AI Launchpad & GenAI Hub** | ✅ VERIFIED | AI API connection `prism`, Resource Group `default` verified. |
| **AI Model** | ✅ VERIFIED | `GPT-5.6 Luna` is available and verified. |
| **SAP Build Work Zone** | ✅ VERIFIED | Verified availability. |
| **Orchestration Config** | ✅ VERIFIED | `FORESIGHT_Recovery_Orchestration_v1` (ID: 884ae7da-8003-4b37-a312-af0da9125ffc) verified. |
| **S/4HANA Connectivity** | 🔴 UNVERIFIED | Live APIs (e.g. PurchaseOrder) not yet confirmed. Using MockS4Adapter. |
| **Cloud Foundry Deployment** | 🔴 UNVERIFIED | Full BTP deployment access pending. `mta.yaml` prepared. |
| **SAP Event Mesh** | 🔴 UNVERIFIED | Not yet configured. |
| **AI Core Runtime Credentials** | 🔴 UNVERIFIED | Requires binding via BTP for live runtime connection. |

## 3. SAP Capability Matrix

| Capability / API | Status | Integration Method | Scope |
| :--- | :--- | :--- | :--- |
| **SAP CAP** | VERIFIED | Node.js / CDS Deployment to BTP | MVP |
| **SAP HANA Cloud** | VERIFIED | CAP `cds add hana` | MVP |
| **SAPUI5** | VERIFIED | Served via CAP statically currently | MVP |
| **SAP Generative AI Hub** | VERIFIED (Config) | Python SDK (`sap-ai-sdk-gen` Orchestration) | MVP |
| **S/4HANA: Read Material/Stock** | UNVERIFIED | OData via BTP Destination / LiveS4Adapter | MVP |
| **S/4HANA: Read Supplier** | UNVERIFIED | OData via BTP Destination / LiveS4Adapter | MVP |
| **S/4HANA: Create PO/STO** | UNVERIFIED | OData via BTP Destination / LiveS4Adapter | MVP |
| **SAP Event Mesh** | UNVERIFIED | AMQP / Webhook | Extension |
| **SAP Build Work Zone** | VERIFIED | Launchpad Site Deployment | Extension |

## 4. SAP Generative AI Hub Environment Variables

To activate the real SAP Generative AI Hub integration in the Python orchestrator, the following environment variables must be provided via `.env` or BTP Service Bindings (`VCAP_SERVICES`):

*   `USE_SAP_AI_HUB=true` (Required to activate the `SapGenAiHubProvider`)
*   `AICORE_CLIENT_ID` (Required)
*   `AICORE_CLIENT_SECRET` (Required)
*   `AICORE_AUTH_URL` (Required)
*   `AICORE_API_BASE_URL` (Required)
*   `AICORE_RESOURCE_GROUP` (Optional, defaults to `default`)
*   `AICORE_ORCHESTRATION_CONFIG_ID` (Optional, defaults to `884ae7da-8003-4b37-a312-af0da9125ffc`)
