# FORESIGHT - Resilient Supply Chains (SAP Hackfest 2026)

FORESIGHT is a Decision and Commitment Control Plane for Autonomous Supply Chains.

## SAP Integration Status

| Component | Status | Description |
| :--- | :--- | :--- |
| **BAS (SAP Business App Studio)** | ✅ VERIFIED | Full Stack Cloud Application Dev Space verified. |
| **HANA Cloud / DB** | ✅ VERIFIED | SAP HANA Cloud instance `Hackfest-DB` verified. HDI deployer generated. |
| **AI Launchpad & GenAI Hub** | ✅ VERIFIED | AI API connection `prism`, Resource Group `default` verified. |
| **AI Model** | ✅ VERIFIED | `GPT-5.6 Luna` is available and verified. |
| **SAP Build Work Zone** | ✅ VERIFIED | Verified availability. |
| **Orchestration Config** | ✅ VERIFIED | `FORESIGHT_Recovery_Orchestration_v1` verified. |
| **S/4HANA Connectivity** | 🔴 UNVERIFIED | Live APIs (e.g. PurchaseOrder) not yet confirmed. Using MockS4Adapter. |
| **Cloud Foundry Deployment** | 🔴 UNVERIFIED | Full BTP deployment access pending. `mta.yaml` prepared. |
| **SAP Event Mesh** | 🔴 UNVERIFIED | Not yet configured. |
| **AI Core Runtime Credentials** | 🔴 UNVERIFIED | Requires binding via BTP for live runtime connection. |

## Quickstart (Local)

1. **CAP Backend:** `cd sap-cap-backend && npm run watch`
2. **Orchestrator:** `cd agent_orchestration && python api.py`
3. **Mock S/4HANA:** `cd mock-s4hana && node index.js`

To run diagnostics: `python diagnostics.py`
