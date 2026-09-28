using { foresight } from '../db/schema';

service ForesightService {

    entity Disruptions as projection on foresight.Disruption;
    entity Suppliers as projection on foresight.Supplier;
    entity Materials as projection on foresight.Material;
    entity Plants as projection on foresight.Plant;
    entity Inventories as projection on foresight.Inventory;
    
    @odata.draft.enabled
    entity RecoveryPlans as projection on foresight.RecoveryPlan;
    
    entity AgentActions as projection on foresight.AgentAction;
    entity Approvals as projection on foresight.Approval;
    entity Commitments as projection on foresight.Commitment;
    entity AuditEvents as projection on foresight.AuditEvent;

    // Action to simulate disruption trigger
    action triggerDisruption(supplierId: String, materialId: String) returns Disruptions;
    
    // Action to approve plan
    action approvePlan(planId: String, approverId: String, comments: String) returns RecoveryPlans;

    // Action to reject plan and initiate SAGA compensation / replan
    action rejectPlan(planId: String, approverId: String, comments: String) returns RecoveryPlans;

    // Action to simulate execution failure and automated SAGA compensation
    action failExecution(planId: String, reason: String) returns RecoveryPlans;

}
