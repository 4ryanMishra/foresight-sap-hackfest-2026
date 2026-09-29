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
| **Orchestration Config** | ✅ VERIFIED | `FORESIGHT_Recovery_Orchestration_v1` (ID: `884ae7da-8003-4b37-a312-af0da9125ffc`) verified. |
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
| **SAP Generative AI Hub** | VERIFIED (Config) | Python SDK (`sap-ai-sdk-gen>=2.0.0` Orchestration V2) | MVP |
| **S/4HANA: Read Material/Stock** | UNVERIFIED | OData via BTP Destination / LiveS4Adapter | MVP |
| **S/4HANA: Read Supplier** | UNVERIFIED | OData via BTP Destination / LiveS4Adapter | MVP |
| **S/4HANA: Create PO/STO** | UNVERIFIED | OData via BTP Destination / LiveS4Adapter | MVP |
| **SAP Event Mesh** | UNVERIFIED | AMQP / Webhook | Extension |
| **SAP Build Work Zone** | VERIFIED | Launchpad Site Deployment | Extension |

## 4. SAP Generative AI Hub Integration Specification (Orchestration V2 API)

*   **Target SDK**: `sap-ai-sdk-gen>=2.0.0`
*   **Orchestration API Version**: **V2** (`gen_ai_hub.orchestration_v2`)
*   **Exact Imports / Classes Used**:
    ```python
    from gen_ai_hub.orchestration_v2.service import OrchestrationService
    ```
*   **Target Model**: `GPT-5.6 Luna`
*   **Orchestration Config ID**: `884ae7da-8003-4b37-a312-af0da9125ffc`
*   **Resource Group**: `default`
*   **Orchestration Input Parameter**: `disruption_context`

### Required Environment Variables
*   `USE_SAP_AI_HUB=true`
*   `AICORE_CLIENT_ID` (OAuth client ID)
*   `AICORE_CLIENT_SECRET` (OAuth client secret)
*   `AICORE_AUTH_URL` (OAuth token endpoint)
*   `AICORE_API_BASE_URL` (AI Core REST API root)
*   `AICORE_RESOURCE_GROUP` (Optional, default: `default`)
*   `AICORE_ORCHESTRATION_CONFIG_ID` (Optional, default: `884ae7da-8003-4b37-a312-af0da9125ffc`)

### Live Authentication Status
*   **Live Call Tested**: **NOT RUN** (Missing runtime environment credentials `AICORE_CLIENT_ID` and `AICORE_CLIENT_SECRET`).
*   **Fallback Mode**: Automatically active (`MockLLMProvider`).
