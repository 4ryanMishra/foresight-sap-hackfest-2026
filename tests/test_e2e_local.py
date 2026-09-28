import sys
import os
import asyncio
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_orchestration.models import SupplyChainContext
from agent_orchestration.orchestrator import OrchestratorAgent
from agent_orchestration.interfaces import LLMProvider
from optimization.optimizer import CpSatOptimizer
from optimization.policy import PolicyService

class MockLLMProvider(LLMProvider):
    pass

async def test_disruption_to_recovery_plan():
    print("--- STARTING E2E TEST: Disruption to Recovery Plan ---")
    llm = MockLLMProvider()
    opt = CpSatOptimizer()
    pol = PolicyService(budget_threshold=1000000.0, max_commitment_risk=50000.0)

    orchestrator = OrchestratorAgent(llm_provider=llm, opt_service=opt, policy_service=pol)

    raw_event = {
        "id": "DISRUPT-101",
        "type": "SupplierFailure"
    }

    context = SupplyChainContext(
        disruption_id="DISRUPT-101",
        impacted_material_id="UNKNOWN", 
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

    result = await orchestrator.execute_flow(raw_event, context)

    assert result["status"] == "FEASIBLE"
    assert "actions" in result
    assert result["total_cost"] > 0
    assert result["validation"]["policy_passed"] == True
    
    # Assert that InventoryAgent's transfer was used
    stock_transfer = next((a for a in result["actions"] if a["action_type"] == "STOCK_TRANSFER"), None)
    assert stock_transfer is not None
    assert stock_transfer["quantity"] > 0

    print("--- E2E TEST PASSED ---")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(test_disruption_to_recovery_plan())
