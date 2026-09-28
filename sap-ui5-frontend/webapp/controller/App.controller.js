sap.ui.define([
    "sap/ui/core/mvc/Controller",
    "sap/ui/model/json/JSONModel",
    "sap/m/MessageBox",
    "sap/m/MessageToast"
], function (Controller, JSONModel, MessageBox, MessageToast) {
    "use strict";

    return Controller.extend("foresight.ui.controller.App", {
        onInit: function () {
            var oData = {
                telemetry: [
                    { time: "08:11:02", agent: "DisruptionAgent", tool: "Sensing / Bayesian", findings: "Supplier SUP-003 telemetry drop. Bayesian verification confirms 95% outage for MAT-100 (5,000 PC shortage).", confidence: "95.0%", state: "Error" },
                    { time: "08:11:05", agent: "ProcurementAgent", tool: "Query API_SUPPLIER", findings: "Scanned alternative vendor roster. Identified SUP-002 (Germany, Low Risk, 5K Capacity) and SUP-001 (Taiwan, 10K Capacity).", confidence: "90.0%", state: "Success" },
                    { time: "08:11:05", agent: "InventoryAgent", tool: "Query API_STOCK", findings: "Located 1,200 PC excess at Plant B (Monterrey) and 500 PC reserve at Plant A (Austin). Formulated internal stock transfer.", confidence: "95.0%", state: "Success" },
                    { time: "08:11:06", agent: "LogisticsAgent", tool: "Route Evaluation", findings: "Evaluated expedited air freight (DE->US, 1 day, $2/unit) and overland transfer (MX->US, 2 days, $5/unit). Both within SLA.", confidence: "85.0%", state: "Information" },
                    { time: "08:11:06", agent: "ProductionAgent", tool: "Dynamic BOM Check", findings: "Component MAT-100-revB verified compatible with engineering drawings ES-2026 for Production Order PRD-1001.", confidence: "99.0%", state: "Success" },
                    { time: "08:11:07", agent: "RiskAgent", tool: "Sanctions & ESG Scan", findings: "SUP-002 cleared. Tier 1 low geopolitical risk. ESG score 88/100. Trade corridor green.", confidence: "92.0%", state: "Success" },
                    { time: "08:11:08", agent: "CpSatOptimizer", tool: "Constraint Solver", findings: "Solved mixed-integer program in 42ms. Selected 1,700 transfer + 3,300 buy from SUP-002. Total cost $157,000.", confidence: "100%", state: "Success" },
                    { time: "08:11:09", agent: "PolicyControl", tool: "Commitment Gate", findings: "Policy-as-Code checks passed. Human approval required as total commitment exceeds $100K threshold.", confidence: "100%", state: "Warning" }
                ],
                audit: [
                    { time: "2026-09-29 08:11:02", actor: "DisruptionAgent", type: "DISRUPTION_DETECTED", state: "Error", evidence: "Sensor telemetry drop. Outage at SUP-003. 5,000 PC impact.", target: "Supplier:SUP-003" },
                    { time: "2026-09-29 08:11:08", actor: "CpSatOptimizer", type: "PLAN_FORMULATED", state: "Success", evidence: "Optimal mix: 1,700 stock transfer + 3,300 PO from SUP-002 ($157K).", target: "RecoveryPlan:PLAN-A" },
                    { time: "2026-09-29 08:11:09", actor: "PolicyEngine", type: "GATE_EVALUATED", state: "Warning", evidence: "Value exceeds $100K threshold; required executive approval flag raised.", target: "Policy:GATE-01" }
                ]
            };

            var oModel = new JSONModel(oData);
            this.getView().setModel(oModel);
        },

        onApprove: function () {
            var that = this;
            MessageBox.confirm(
                "Approve Recovery Plan A ($157,000)?\n\nThis will execute the SAGA dual-phase commit:\n• Generate S/4HANA PO-SIM-9482 (3,300 PC)\n• Execute Stock Transport Order STO-SIM-1204 (1,200 PC)\n• Lock immutable audit record in SAP HANA Cloud",
                {
                    title: "Executive Commitment Gate",
                    actions: [MessageBox.Action.YES, MessageBox.Action.NO],
                    emphasizedAction: MessageBox.Action.YES,
                    onClose: function (oAction) {
                        if (oAction === MessageBox.Action.YES) {
                            MessageToast.show("Recovery Plan Committed to S/4HANA!");
                            
                            // Append to audit model
                            var oModel = that.getView().getModel();
                            var aAudit = oModel.getProperty("/audit");
                            var now = new Date().toISOString().replace("T", " ").substring(0, 19);
                            aAudit.unshift({
                                time: now,
                                actor: "SC_Ops_Executive",
                                type: "PLAN_COMMITTED",
                                state: "Success",
                                evidence: "Executive approved Plan A. Dispatched PO-SIM-9482 and STO-SIM-1204.",
                                target: "RecoveryPlan:PLAN-A"
                            });
                            oModel.setProperty("/audit", aAudit);
                        }
                    }
                }
            );
        },

        onReject: function () {
            MessageBox.warning("Initiate SAGA Compensation & Re-plan?\n\nThis releases all temporary holds at Plant B and triggers the agent swarm for secondary alternatives.");
        },

        onSimulate: function () {
            MessageBox.information("Monte Carlo Simulation Results (500 Stochastic Runs):\n\n• Mean Lead Time: 5.95 Days\n• P95 Lead Time: 6.74 Days\n• SLA Breach Probability: 2.1% (Within policy limits)\n• Commitment Risk: $23,550");
        }
    });
});
