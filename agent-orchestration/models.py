from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class SupplyChainContext(BaseModel):
    disruption_id: str
    impacted_material_id: str
    impacted_supplier_id: str
    required_quantity: int
    deadline: str
    # Pre-fetched subgraph data to avoid N+1 queries during parallel agent execution
    available_suppliers: List[Dict[str, Any]] = []
    available_inventory: List[Dict[str, Any]] = []
    open_orders: List[Dict[str, Any]] = []

class AgentRecommendation(BaseModel):
    agent_name: str
    action_type: str
    target_id: str # e.g., Supplier ID or Plant ID
    proposed_quantity: int
    estimated_cost: float
    confidence: float
    rationale: str
    lead_time_days: int = 0
