import asyncio
from typing import List
from agent_orchestration.models import SupplyChainContext, AgentRecommendation
from agent_orchestration.interfaces import LLMProvider

class BaseAgent:
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider

class DisruptionAgent(BaseAgent):
    async def analyze(self, disruption_event: dict) -> dict:
        # Mock Impact Analysis
        print(f"[DisruptionAgent] Analyzing event: {disruption_event['id']}")
        await asyncio.sleep(0.5)
        return {
            "disruption_id": disruption_event["id"],
            "impacted_material_id": "MAT-100",
            "impacted_supplier_id": "SUP-003",
            "required_quantity": 5000,
            "deadline": "2026-10-15"
        }

class ProcurementAgent(BaseAgent):
    async def evaluate(self, context: SupplyChainContext) -> List[AgentRecommendation]:
        print("[ProcurementAgent] Evaluating alternative suppliers...")
        await asyncio.sleep(1) # Simulate LLM/Search latency
        recommendations = []
        for sup in context.available_suppliers:
            if sup['Supplier'] != context.impacted_supplier_id and sup['RiskClass'] == 'Low':
                recommendations.append(
                    AgentRecommendation(
                        agent_name="ProcurementAgent",
                        action_type="CREATE_PO",
                        target_id=sup['Supplier'],
                        proposed_quantity=min(sup['Capacity'], context.required_quantity),
                        estimated_cost=45.00 * min(sup['Capacity'], context.required_quantity),
                        confidence=0.9,
                        rationale=f"Supplier {sup['Supplier']} is low risk and has available capacity.",
                        lead_time_days=5
                    )
                )
        return recommendations

class InventoryAgent(BaseAgent):
    async def evaluate(self, context: SupplyChainContext) -> List[AgentRecommendation]:
        print("[InventoryAgent] Checking internal plant inventory...")
        await asyncio.sleep(0.8)
        recommendations = []
        for inv in context.available_inventory:
            if inv['Material'] == context.impacted_material_id and inv['UnrestrictedStock'] > 0:
                recommendations.append(
                    AgentRecommendation(
                        agent_name="InventoryAgent",
                        action_type="STOCK_TRANSFER",
                        target_id=inv['Plant'],
                        proposed_quantity=inv['UnrestrictedStock'],
                        estimated_cost=5.00 * inv['UnrestrictedStock'], # internal transfer cost
                        confidence=0.95,
                        rationale=f"Internal stock available at {inv['Plant']}.",
                        lead_time_days=2
                    )
                )
        return recommendations

class LogisticsAgent(BaseAgent):
    async def evaluate(self, context: SupplyChainContext) -> List[AgentRecommendation]:
        print("[LogisticsAgent] Evaluating freight options...")
        await asyncio.sleep(0.9)
        # Mocking logistics route for a generic expedited freight
        return [
            AgentRecommendation(
                agent_name="LogisticsAgent",
                action_type="EXPEDITE_FREIGHT",
                target_id="AIR-FREIGHT-01",
                proposed_quantity=context.required_quantity,
                estimated_cost=2.00 * context.required_quantity,
                confidence=0.85,
                rationale="Expedited air freight available to meet deadline.",
                lead_time_days=1
            )
        ]

class ProductionAgent(BaseAgent):
    async def evaluate(self, context: SupplyChainContext) -> List[AgentRecommendation]:
        print("[ProductionAgent] Checking dynamic BOM alternatives...")
        await asyncio.sleep(0.7)
        return [] # No alternative BOM for this MVP slice

class RiskAgent(BaseAgent):
    async def evaluate(self, context: SupplyChainContext) -> List[AgentRecommendation]:
        print("[RiskAgent] Assessing macro risk and compliance...")
        await asyncio.sleep(1.2)
        # In this slice, Risk Agent doesn't propose primary capacity, 
        # it might provide risk flags. For now, returns empty or generic risk mitigation.
        return []
