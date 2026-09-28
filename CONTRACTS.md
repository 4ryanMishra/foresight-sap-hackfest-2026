# FORESIGHT Canonical Contracts

This document defines the definitive schema and field mappings across the SAP CAP backend, Python Orchestrator, and S/4HANA mock adapter for the canonical supplier-failure scenario.

## 1. Disruption
**Source of Truth:** SAP CAP (`foresight.Disruption`)
- `ID`: String (UUID)
- `type`: String (e.g., `"SupplierFailure"`)
- `description`: String
- `status`: String (`"DETECTED" | "ANALYZING" | "PLAN_PROPOSED" | "RESOLVED" | "FAILED"`)
- `confidenceScore`: Decimal
- `impactedSupplier_ID`: String (Foreign Key to Supplier)
- `impactedMaterial_ID`: String (Foreign Key to Material)
- `recoveryPlan_ID`: String (Foreign Key to RecoveryPlan)

## 2. SupplyChainContext
**Source of Truth:** Python Orchestrator (`agent_orchestration/models.py`)
Passed from CAP to Python via POST `/orchestrate`.
- `disruption_id`: String
- `impacted_material_id`: String
- `impacted_supplier_id`: String
- `required_quantity`: Integer
- `deadline`: String (ISO 8601 Date)
- `available_suppliers`: Array of Objects (Mock S/4 format)
- `available_inventory`: Array of Objects (Mock S/4 format)
- `open_orders`: Array of Objects (Mock S/4 format)

## 3. AgentRecommendation
**Source of Truth:** Python Orchestrator (`agent_orchestration/models.py`)
Internal contract between Swarm Agents and Optimizer.
- `agent_name`: String (e.g., `"ProcurementAgent"`)
- `action_type`: String (e.g., `"CREATE_PO"`, `"STOCK_TRANSFER"`)
- `target_id`: String
- `proposed_quantity`: Integer
- `estimated_cost`: Float
- `confidence`: Float
- `rationale`: String
- `lead_time_days`: Integer

## 4. RecoveryPlan
**Source of Truth:** SAP CAP (`foresight.RecoveryPlan`)
- `ID`: String (UUID)
- `disruption_ID`: String
- `status`: String (`"DRAFT" | "PENDING_APPROVAL" | "APPROVED" | "REJECTED" | "EXECUTED" | "EXECUTION_FAILED"`)
- `totalCost`: Decimal
- `serviceImpact`: String
- `commitmentRisk`: Decimal
- `rationale`: String

## 5. RecoveryAction (AgentAction)
**Source of Truth:** SAP CAP (`foresight.AgentAction`)
- `ID`: String (UUID)
- `recoveryPlan_ID`: String
- `agentName`: String
- `actionType`: String (`"CREATE_PO" | "STOCK_TRANSFER"`)
- `targetSupplier_ID`: String (Nullable)
- `targetPlant_ID`: String (Nullable)
- `quantity`: Integer
- `estimatedCost`: Decimal
- `description`: String

## 6. Commitment
**Source of Truth:** SAP CAP (`foresight.Commitment`)
- `ID`: String (UUID)
- `recoveryPlan_ID`: String
- `commitmentType`: String
- `referenceId`: String
- `status`: String (`"AT_RISK" | "MITIGATED" | "FAILED"`)

## 7. Approval
**Source of Truth:** SAP CAP (`foresight.Approval`)
- `ID`: String (UUID)
- `recoveryPlan_ID`: String
- `approverId`: String
- `decision`: String (`"APPROVED" | "REJECTED"`)
- `comments`: String

## 8. AuditEvent
**Source of Truth:** SAP CAP (`foresight.AuditEvent`)
- `ID`: String (UUID)
- `entityName`: String (e.g., `"RecoveryPlan"`, `"Supplier"`)
- `entityId`: String
- `eventType`: String (e.g., `"PLAN_APPROVED"`, `"EXECUTION_SUCCESS"`)
- `details`: String

## 9. S4Adapter Contract (Mock S/4HANA)
**Source of Truth:** Express API (`mock-s4hana/index.js`)
### Context Fetch
- **Endpoint**: `GET /sap/opu/odata/sap/API_SUPPLIER/A_Supplier`
- **Response**: `{ "d": { "results": [{ "Supplier": "...", "SupplierName": "...", "Country": "...", "RiskClass": "...", "Capacity": ... }] } }`
### Execution (PO Creation)
- **Endpoint**: `POST /sap/opu/odata/sap/API_PURCHASEORDER_PROCESS_SRV/A_PurchaseOrder`
- **Request Payload**: `{ "Supplier": "SUP-002", "Material": "MAT-100", "OrderQuantity": 3300 }`
- **Response Payload**: `{ "d": { "PurchaseOrder": "PO-SIM-9482", "Supplier": "SUP-002", "Status": "Created Locally" } }`
