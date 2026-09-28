import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Add parent directory to path so we can import optimization and agent_orchestration
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_orchestration.models import SupplyChainContext
from agent_orchestration.orchestrator import OrchestratorAgent
from agent_orchestration.interfaces import LLMProvider
from optimization.optimizer import CpSatOptimizer
from optimization.policy import PolicyService

app = FastAPI(title="FORESIGHT Agent Orchestrator")

class MockLLMProvider(LLMProvider):
    pass # Currently using deterministic logic in agents

# Global instances
llm = MockLLMProvider()
opt = CpSatOptimizer()
pol = PolicyService()
orchestrator = OrchestratorAgent(llm_provider=llm, opt_service=opt, policy_service=pol)

class OrchestrationRequest(BaseModel):
    raw_event: dict
    context: SupplyChainContext

@app.post("/orchestrate")
async def orchestrate(req: OrchestrationRequest):
    try:
        final_plan = await orchestrator.execute_flow(req.raw_event, req.context)
        return final_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
