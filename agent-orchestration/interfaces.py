from typing import List, Dict, Any
from models import SupplyChainContext, AgentRecommendation

class LLMProvider:
    async def generate_structured_response(self, prompt: str, schema: Any) -> Any:
        raise NotImplementedError

class S4Adapter:
    async def get_suppliers(self) -> List[Dict]:
        raise NotImplementedError
    async def get_inventory(self, material_id: str) -> List[Dict]:
        raise NotImplementedError
    async def get_purchase_orders(self) -> List[Dict]:
        raise NotImplementedError
    async def execute_mock_transaction(self, action: AgentRecommendation) -> Dict:
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
