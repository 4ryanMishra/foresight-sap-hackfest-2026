import os
import unittest
import uuid
from agent_orchestration.hana_adapter import HanaPersistenceAdapter

class TestHanaPersistenceAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = HanaPersistenceAdapter()

    def test_adapter_initialization(self):
        """Verify that HanaPersistenceAdapter initializes properly and safely handles unconfigured state."""
        self.assertEqual(self.adapter.schema, os.environ.get("HANA_SCHEMA", "HACKEFEST0115"))
        if not os.environ.get("HANA_HOST"):
            self.assertFalse(self.adapter.is_configured)

    @unittest.skipUnless(
        os.environ.get("HANA_HOST") and os.environ.get("HANA_USER") and os.environ.get("HANA_PASSWORD"),
        "Skipping live HANA Cloud tests because HANA_HOST / HANA_USER / HANA_PASSWORD are not set in environment."
    )
    def test_live_hana_connection_and_dummy(self):
        """1. Test live HANA Cloud connection and SELECT 1 FROM DUMMY."""
        status = self.adapter.health_check()
        self.assertTrue(status["configured"])
        self.assertTrue(status["reachable"])
        self.assertTrue(status["test_query_passed"])

    @unittest.skipUnless(
        os.environ.get("HANA_HOST") and os.environ.get("HANA_USER") and os.environ.get("HANA_PASSWORD"),
        "Skipping live HANA Cloud tests."
    )
    def test_live_schema_init_and_rx1042_lifecycle(self):
        """
        Tests 2 through 7:
        - Schema Initialization
        - RecoveryCase CRUD
        - AgentDecision persistence
        - RecoveryPlan persistence
        - Commitment persistence
        - CompensationEvent persistence
        - RX-1042 full lifecycle persistence
        """
        # Ensure tables are created
        self.adapter.init_schema()

        case_id = f"RX-1042-TEST-{uuid.uuid4().hex[:6]}"
        disruption_id = f"DISRUPT-{uuid.uuid4().hex[:6]}"
        plan_id = f"RP-07-{uuid.uuid4().hex[:6]}"

        # 2. RecoveryCase CRUD
        created_case = self.adapter.create_recovery_case(
            case_id=case_id,
            disruption_id=disruption_id,
            supplier_id="SUP-100",
            material_id="MAT-100",
            shortage_qty=5000,
            status="PROPOSED"
        )
        self.assertIsNotNone(created_case)
        self.assertEqual(created_case["case_id"], case_id)
        self.assertEqual(created_case["status"], "PROPOSED")

        # Update case status
        self.adapter.update_recovery_case_status(case_id, "APPROVED")
        updated_case = self.adapter.get_recovery_case(case_id)
        self.assertEqual(updated_case["status"], "APPROVED")

        # 3. AgentDecision Persistence
        self.adapter.save_agent_decision(
            decision_id=f"DEC-{uuid.uuid4().hex[:6]}",
            case_id=case_id,
            agent_name="ProcurementAgent",
            action_type="CREATE_PO",
            target_id="SUP-200",
            quantity=3300,
            estimated_cost=148500.0,
            confidence=0.95,
            rationale="SUP-200 low risk with immediate capacity."
        )
        decisions = self.adapter.get_agent_decisions(case_id)
        self.assertGreaterEqual(len(decisions), 1)
        self.assertEqual(decisions[0]["agent_name"], "ProcurementAgent")

        # 4. RecoveryPlan Persistence
        self.adapter.save_recovery_plan(
            plan_id=plan_id,
            case_id=case_id,
            status="FEASIBLE",
            total_cost=157000.0,
            commitment_risk=23550.0,
            sla_impact="0 Days Delay"
        )
        plan = self.adapter.get_recovery_plan(plan_id)
        self.assertIsNotNone(plan)
        self.assertEqual(plan["status"], "FEASIBLE")

        # Update plan status
        self.adapter.update_recovery_plan_status(plan_id, "EXECUTED")
        updated_plan = self.adapter.get_recovery_plan(plan_id)
        self.assertEqual(updated_plan["status"], "EXECUTED")

        # 5. Commitment Persistence
        self.adapter.create_commitment(
            commitment_id=f"COMM-{uuid.uuid4().hex[:6]}",
            case_id=case_id,
            plan_id=plan_id,
            commitment_type="CustomerOrder",
            reference_id="CUST-882",
            status="MITIGATED"
        )
        commitments = self.adapter.get_commitments(case_id)
        self.assertGreaterEqual(len(commitments), 1)
        self.assertEqual(commitments[0]["reference_id"], "CUST-882")

        # 6. CompensationEvent Persistence & Replan Lifecycle
        self.adapter.record_compensation_event(
            compensation_id=f"COMP-{uuid.uuid4().hex[:6]}",
            case_id=case_id,
            previous_plan_id=plan_id,
            reason="Secondary disruption: SUP-200 failure to confirm.",
            actions_released="Released 1,200 PC hold at Plant B."
        )
        comps = self.adapter.get_compensation_events(case_id)
        self.assertGreaterEqual(len(comps), 1)
        self.assertEqual(comps[0]["previous_plan_id"], plan_id)

        # Final RX-1042 status update to REPLANNED
        self.adapter.update_recovery_case_status(case_id, "REPLANNED")
        final_case = self.adapter.get_recovery_case(case_id)
        self.assertEqual(final_case["status"], "REPLANNED")

if __name__ == "__main__":
    unittest.main()
