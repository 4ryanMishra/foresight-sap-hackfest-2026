import asyncio

class PolicyService:
    def __init__(self, budget_threshold: float = 1000000.0, max_commitment_risk: float = 50000.0):
        self.budget_threshold = budget_threshold
        self.max_commitment_risk = max_commitment_risk

    async def evaluate_plan(self, plan: dict) -> dict:
        print("[PolicyService] Evaluating plan against enterprise policies...")
        await asyncio.sleep(0.3)
        
        if plan["status"] == "INFEASIBLE":
            return {"policy_passed": False, "reason": "Plan is infeasible"}

        total_cost = plan.get("total_cost", 0.0)
        risk = plan.get("commitment_risk", 0.0)

        passed = True
        violations = []

        if total_cost > self.budget_threshold:
            passed = False
            violations.append(f"Budget Exceeded: {total_cost} > {self.budget_threshold}")
            
        if risk > self.max_commitment_risk:
            passed = False
            violations.append(f"Commitment Risk Too High: {risk} > {self.max_commitment_risk}")

        # Human Approval Threshold
        requires_human_approval = total_cost > (self.budget_threshold * 0.1) or not passed

        return {
            "policy_passed": passed,
            "violations": violations,
            "requires_human_approval": requires_human_approval
        }

class SagaRecovery:
    def execute_compensation(self, failed_action_id: str):
        # A simple local compensation logic
        print(f"[SagaRecovery] Executing compensation for action {failed_action_id}")
        print(f"[SagaRecovery] Releasing mock reservations... Done.")
        print(f"[SagaRecovery] Flagging for Replan... Done.")
