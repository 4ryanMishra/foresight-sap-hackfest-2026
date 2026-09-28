const cds = require('@sap/cds');

module.exports = cds.service.impl(async function() {
    const { Disruptions, RecoveryPlans, Approvals, AuditEvents } = this.entities;

    this.on('triggerDisruption', async (req) => {
        const { supplierId, materialId } = req.data;
        
        // Log to Audit
        await INSERT.into(AuditEvents).entries({
            entityName: 'Supplier',
            entityId: supplierId,
            eventType: 'DISRUPTION_TRIGGERED',
            details: `Supplier ${supplierId} failed for material ${materialId}`
        });

        // Create Disruption
        const result = await INSERT.into(Disruptions).entries({
            type: 'SupplierFailure',
            description: 'Critical supplier went offline due to cyberattack',
            status: 'DETECTED',
            confidenceScore: 0.95,
            impactedSupplier_ID: supplierId,
            impactedMaterial_ID: materialId
        });

        // Normally, here we would send an Event Mesh message to wake up the python orchestrator
        return result;
    });

    this.on('approvePlan', async (req) => {
        const { planId, approverId, comments } = req.data;

        // Update Recovery Plan Status
        await UPDATE(RecoveryPlans).set({ status: 'APPROVED' }).where({ ID: planId });

        // Add Approval record
        await INSERT.into(Approvals).entries({
            recoveryPlan_ID: planId,
            approverId: approverId,
            decision: 'APPROVED',
            comments: comments
        });

        // Log Audit Event
        await INSERT.into(AuditEvents).entries({
            entityName: 'RecoveryPlan',
            entityId: planId,
            eventType: 'PLAN_APPROVED',
            details: `Plan approved by ${approverId}: ${comments}`
        });

        // In a real system, this would trigger the actual execution (Saga Commit)
        return await SELECT.one.from(RecoveryPlans).where({ ID: planId });
    });
});
