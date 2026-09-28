import asyncio
from typing import List
from agent_orchestration.models import SupplyChainContext, AgentRecommendation
from agent_orchestration.agents import DisruptionAgent, ProcurementAgent, InventoryAgent, LogisticsAgent, ProductionAgent, RiskAgent
from agent_orchestration.interfaces import LLMProvider, OptimizationService, PolicyService

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
        context.required_quantity = impact['required_quantity']

        # 2. COLLABORATE
        print("\n[2/5] COLLABORATE: Parallel Agent Swarm...")
        recommendations = await self.run_swarm(context)

        # 3. SIMULATE
        print("\n[3/5] SIMULATE: Optimization & Simulation...")
        recovery_plan = await self.opt_service.generate_feasible_plan(context, recommendations)

        # 4. COMMIT
        print("\n[4/5] COMMIT: Policy & Commitment Control...")
        validation_result = await self.policy_service.evaluate_plan(recovery_plan)
        recovery_plan['validation'] = validation_result

        print("\n=== FLOW COMPLETE ===")
        return recovery_plan
