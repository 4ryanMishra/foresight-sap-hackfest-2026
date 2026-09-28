namespace foresight;

using { cuid, managed } from '@sap/cds/common';

entity Disruption : cuid, managed {
    type              : String; // e.g. 'SupplierFailure'
    description       : String;
    status            : String default 'DETECTED'; // DETECTED, ANALYZING, PLAN_PROPOSED, RESOLVED
    confidenceScore   : Decimal(5,2);
    impactedSupplier  : Association to Supplier;
    impactedMaterial  : Association to Material;
    recoveryPlan      : Association to RecoveryPlan;
}

entity Supplier : managed {
    key ID            : String; // e.g. 'SUP-001'
    name              : String;
    location          : String;
    riskScore         : Decimal(5,2);
    isQualified       : Boolean;
    capacity          : Integer;
}

entity Material : managed {
    key ID            : String; // e.g. 'MAT-100'
    name              : String;
    description       : String;
    unitPrice         : Decimal(10,2);
    currency          : String default 'USD';
}

entity Plant : managed {
    key ID            : String; // e.g. 'PLANT-A'
    name              : String;
    location          : String;
}

entity Inventory : cuid {
    material          : Association to Material;
    plant             : Association to Plant;
    quantityAvailable : Integer;
    reorderLevel      : Integer;
}

entity RecoveryPlan : cuid, managed {
    disruption        : Association to Disruption;
    status            : String default 'DRAFT'; // DRAFT, PENDING_APPROVAL, APPROVED, REJECTED, EXECUTED
    totalCost         : Decimal(15,2);
    serviceImpact     : String;
    commitmentRisk    : Decimal(5,2);
    rationale         : LargeString;
    actions           : Composition of many AgentAction on actions.recoveryPlan = $self;
    approvals         : Composition of many Approval on approvals.recoveryPlan = $self;
    commitments       : Composition of many Commitment on commitments.recoveryPlan = $self;
}

entity AgentAction : cuid {
    recoveryPlan      : Association to RecoveryPlan;
    agentName         : String; // e.g. 'ProcurementAgent'
    actionType        : String; // e.g. 'CREATE_PO', 'STOCK_TRANSFER'
    targetSupplier    : Association to Supplier;
    targetPlant       : Association to Plant;
    quantity          : Integer;
    estimatedCost     : Decimal(10,2);
    description       : String;
}

entity Approval : cuid, managed {
    recoveryPlan      : Association to RecoveryPlan;
    approverId        : String;
    decision          : String; // APPROVED, REJECTED
    comments          : String;
}

entity Commitment : cuid, managed {
    recoveryPlan      : Association to RecoveryPlan;
    commitmentType    : String; // e.g. 'CustomerOrder', 'ProductionOrder'
    referenceId       : String; // external ID
    status            : String; // AT_RISK, MITIGATED, FAILED
}

entity AuditEvent : cuid, managed {
    entityName        : String;
    entityId          : String;
    eventType         : String;
    details           : LargeString;
}
