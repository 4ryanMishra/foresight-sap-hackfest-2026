import asyncio
import sys
import os

# Add parent directory to path so we can import optimization
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import SupplyChainContext
from orchestrator import OrchestratorAgent
from interfaces import LLMProvider
from optimization.optimizer import CpSatOptimizer
from optimization.policy import PolicyService

class MockLLMProvider(LLMProvider):
    pass # Currently using deterministic logic in agents

async def run_local_slice():
    llm = MockLLMProvider()
    opt = CpSatOptimizer()
    pol = PolicyService()

    orchestrator = OrchestratorAgent(llm_provider=llm, opt_service=opt, policy_service=pol)

    # 0. The Raw Event
    raw_event = {
        "id": "DISRUPT-101",
        "type": "SupplierFailure"
    }

    # Pre-fetched context (mocking CAP/S4 Data Provider)
    context = SupplyChainContext(
        disruption_id="DISRUPT-101",
        impacted_material_id="UNKNOWN", # Will be mapped by DisruptionAgent
        impacted_supplier_id="UNKNOWN",
        required_quantity=0,
        deadline="UNKNOWN",
        available_suppliers=[
            {'Supplier': 'SUP-001', 'RiskClass': 'Low', 'Capacity': 10000},
            {'Supplier': 'SUP-002', 'RiskClass': 'Low', 'Capacity': 5000},
            {'Supplier': 'SUP-003', 'RiskClass': 'High', 'Capacity': 20000}
        ],
        available_inventory=[
            {'Material': 'MAT-100', 'Plant': 'PLANT-A', 'UnrestrictedStock': 500},
            {'Material': 'MAT-100', 'Plant': 'PLANT-B', 'UnrestrictedStock': 1200}
        ]
    )

    final_plan = await orchestrator.execute_flow(raw_event, context)
    
    import json
    print("\n--- FINAL RECOVERY PLAN ---")
    print(json.dumps(final_plan, indent=2))

if __name__ == "__main__":
    asyncio.run(run_local_slice())
