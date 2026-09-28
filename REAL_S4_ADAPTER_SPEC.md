# REAL S/4HANA ADAPTER SPECIFICATION

This document outlines the exact interface required for a live S/4HANA implementation for the FORESIGHT Decision Console.

**STATUS:** 🔴 `UNVERIFIED` - All endpoints and data structures must be confirmed in the target SAP practice environment.

## 1. Architectural Guardrails

*   **CAP is the ONLY Gateway**: The Python Agent layer MUST NOT directly query or execute transactions in S/4HANA. All communication with S/4HANA routes through the SAP CAP backend via the SAP Cloud SDK or BTP Destination Service.
*   **Abstraction Layer**: The CAP backend interacts with S/4HANA via external services (e.g., `cds.connect.to()`). If an S/4 API changes, only the CAP abstraction logic changes, not the Python agents or the frontend.
*   **Authentication**: Managed natively by BTP (Destination Service + Cloud Connector / XSUAA). No hardcoded basic auth or tokens.

## 2. Required S/4HANA Context APIs (UNVERIFIED)

These APIs are required to hydrate the `SupplyChainContext` passed to the Python orchestrator.

### 2.1 Supplier Master Data
*   **Expected API**: `API_BUSINESS_PARTNER` or `API_SUPPLIER` (OData V2/V4)
*   **Required Fields**: `Supplier`, `SupplierName`, `Country`, risk metadata if available as custom fields.
*   **Usage**: Fetch impacted supplier details and alternative capable suppliers.

### 2.2 Material Master Data
*   **Expected API**: `API_PRODUCT_SRV` (OData V2) or `API_PRODUCT`
*   **Required Fields**: `Product`, `ProductName`, `BaseUnit`
*   **Usage**: Validate the impacted material.

### 2.3 Inventory Data
*   **Expected API**: `API_MATERIAL_STOCK_SRV` or `API_INVENTORY_MANAGEMENT`
*   **Required Fields**: `Material`, `Plant`, `UnrestrictedStock`, `InTransitStock`
*   **Usage**: Discover available inventory across alternative plants to satisfy shortages.

### 2.4 Purchasing & Production Context
*   **Expected API**: `API_PURCHASEORDER_PROCESS_SRV` (PO) & `API_PRODUCTION_ORDER_SRV` (PRD)
*   **Required Fields**: `PurchaseOrder`, `OrderQuantity`, `DeliveryDate`, `Supplier`, `Material` (and PRD equivalents).
*   **Usage**: Map open orders that might be delayed or used for expediting.

## 3. Required S/4HANA Execution APIs (UNVERIFIED)

These APIs are called *only* upon human approval of a `RecoveryPlan` in the FORESIGHT UI.

### 3.1 Purchase Order Creation
*   **Expected API**: `POST /sap/opu/odata/sap/API_PURCHASEORDER_PROCESS_SRV/A_PurchaseOrder`
*   **Payload structure needed**:
    ```json
    {
      "Supplier": "<Verified-Supplier-ID>",
      "PurchaseOrderType": "NB",
      "PurchasingOrganization": "<Org>",
      "PurchasingGroup": "<Grp>",
      "CompanyCode": "<Code>",
      "to_PurchaseOrderItem": [
        {
          "Material": "<Material-ID>",
          "Plant": "<Plant-ID>",
          "OrderQuantity": "<Qty>"
        }
      ]
    }
    ```
*   **Usage**: Execute `CREATE_PO` Agent actions.

### 3.2 Stock Transfer / Inventory Move
*   **Expected API**: Material Document Creation (`API_MATERIAL_DOCUMENT_SRV`)
*   **Usage**: Execute `STOCK_TRANSFER` Agent actions (e.g., Mvt Type 301/311).

## 4. Error Handling and Resilience

*   **Timeout & Retries**: CAP must wrap S/4HANA calls in resilience patterns (circuit breakers/retries).
*   **Compensating Transactions (SAGA)**: If a `CREATE_PO` succeeds but the subsequent `STOCK_TRANSFER` fails, CAP must possess logic to either rollback the PO or flag the `RecoveryPlan` as `EXECUTION_FAILED` requiring human intervention. Currently handled via `failExecution` CAP action.
