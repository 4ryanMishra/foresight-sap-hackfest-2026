from typing import List, Dict, Any
from agent_orchestration.models import SupplyChainContext, AgentRecommendation

class LLMProvider:
    async def generate_structured_response(self, prompt: str, schema: Any) -> Any:
        raise NotImplementedError

class SupplyChainDataProvider:
    async def fetch_context(self, disruption_id: str) -> SupplyChainContext:
        raise NotImplementedError

class OptimizationService:
    async def generate_feasible_plan(self, context: SupplyChainContext, recommendations: List[AgentRecommendation]) -> Dict:
        raise NotImplementedError

class PolicyService:
    async def evaluate_plan(self, plan: Dict) -> Dict:
        raise NotImplementedError
