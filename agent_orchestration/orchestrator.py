import asyncio
import uuid
from typing import List
from agent_orchestration.models import SupplyChainContext, AgentRecommendation
from agent_orchestration.agents import DisruptionAgent, ProcurementAgent, InventoryAgent, LogisticsAgent, ProductionAgent, RiskAgent
from agent_orchestration.interfaces import LLMProvider, OptimizationService, PolicyService
from agent_orchestration.hana_adapter import HanaPersistenceAdapter

class OrchestratorAgent:
    def __init__(self, llm_provider: LLMProvider, opt_service: OptimizationService, policy_service: PolicyService):
        self.disruption_agent = DisruptionAgent(llm_provider)
        self.specialists = [
            ProcurementAgent(llm_provider),
            InventoryAgent(llm_provider),
            LogisticsAgent(llm_provider),
            ProductionAgent(llm_provider),
            RiskAgent(llm_provider)
        ]
        self.opt_service = opt_service
        self.policy_service = policy_service
        self.hana = HanaPersistenceAdapter()
        if self.hana.is_configured:
            try:
                self.hana.init_schema()
            except Exception as e:
                print(f"[Orchestrator] Note: HANA schema initialization deferred: {e}")

    async def run_swarm(self, context: SupplyChainContext) -> List[AgentRecommendation]:
        print("[Orchestrator] Launching parallel agent swarm...")
        
        # Run all specialist agents concurrently!
        tasks = [agent.evaluate(context) for agent in self.specialists]
        results = await asyncio.gather(*tasks)
        
        # Flatten the list of lists
        all_recommendations = [rec for sublist in results for rec in sublist]
        print(f"[Orchestrator] Swarm returned {len(all_recommendations)} recommendations.")
        return all_recommendations

    async def execute_flow(self, raw_event: dict, context: SupplyChainContext) -> dict:
        print("\n=== FORESIGHT EXECUTION LOOP ===")
        # 1. SEE / UNDERSTAND
        print("[1/5] SEE & UNDERSTAND: Disruption Agent analyzing event...")
        impact = await self.disruption_agent.analyze(raw_event)
        
        # Overwrite context with actual impact
        context.impacted_material_id = impact['impacted_material_id']
        context.impacted_supplier_id = impact['impacted_supplier_id']
        context.required_quantity = impact['required_quantity']

        case_id = raw_event.get("case_id", f"RX-1042-{raw_event['id'][:8]}")
        if self.hana.is_configured:
            try:
                self.hana.create_recovery_case(
                    case_id=case_id,
                    disruption_id=raw_event['id'],
                    supplier_id=context.impacted_supplier_id,
                    material_id=context.impacted_material_id,
                    shortage_qty=context.required_quantity,
                    status="PROPOSED"
                )
                self.hana.create_disruption_event(
                    event_id=f"EVT-{raw_event['id'][:8]}",
                    case_id=case_id,
                    event_type=raw_event.get("type", "SupplierFailure"),
                    supplier_id=context.impacted_supplier_id,
                    material_id=context.impacted_material_id,
                    confidence=0.95,
                    details=f"Disruption analyzed: {context.required_quantity} PC shortage."
                )
            except Exception as e:
                print(f"[Orchestrator] Note: HANA event logging deferred: {e}")

        # 2. COLLABORATE
        print("\n[2/5] COLLABORATE: Parallel Agent Swarm...")
        recommendations = await self.run_swarm(context)

        if self.hana.is_configured:
            try:
                for rec in recommendations:
                    self.hana.save_agent_decision(
                        decision_id=f"DEC-{uuid.uuid4().hex[:6]}",
                        case_id=case_id,
                        agent_name=rec.agent_name,
                        action_type=rec.action_type,
                        target_id=rec.target_id,
                        quantity=rec.proposed_quantity,
                        estimated_cost=rec.estimated_cost,
                        confidence=rec.confidence,
                        rationale=rec.rationale
                    )
            except Exception as e:
                print(f"[Orchestrator] Note: HANA agent decision logging deferred: {e}")

        # 3. SIMULATE
        print("\n[3/5] SIMULATE: Optimization & Simulation...")
        recovery_plan = await self.opt_service.generate_feasible_plan(context, recommendations)

        # 4. COMMIT
        print("\n[4/5] COMMIT: Policy & Commitment Control...")
        validation_result = await self.policy_service.evaluate_plan(recovery_plan)
        recovery_plan['validation'] = validation_result

        if self.hana.is_configured:
            try:
                plan_id = recovery_plan.get("id", f"RP-07-{uuid.uuid4().hex[:6]}")
                self.hana.save_recovery_plan(
                    plan_id=plan_id,
                    case_id=case_id,
                    status=recovery_plan.get("status", "FEASIBLE"),
                    total_cost=float(recovery_plan.get("totalCost", 157000.0)),
                    commitment_risk=float(recovery_plan.get("commitmentRisk", 23550.0)),
                    sla_impact=recovery_plan.get("serviceImpact", "0 Days Delay")
                )
                self.hana.create_commitment(
                    commitment_id=f"COMM-{uuid.uuid4().hex[:6]}",
                    case_id=case_id,
                    plan_id=plan_id,
                    commitment_type="CustomerOrder",
                    reference_id="CUST-882",
                    status="MITIGATED"
                )
            except Exception as e:
                print(f"[Orchestrator] Note: HANA plan logging deferred: {e}")

        print("\n=== FLOW COMPLETE ===")
        return recovery_plan
