from ortools.sat.python import cp_model
import numpy as np
import asyncio

class DeterministicMonteCarlo:
    def simulate(self, plan_lead_time_days: int) -> dict:
        # A simple deterministic MC simulator for local MVP
        # Usually this would use stochastic distributions (e.g. np.random.normal)
        # We use a fixed seed to keep it deterministic for MVP tests
        np.random.seed(42)
        simulated_delays = np.random.normal(loc=1.0, scale=0.5, size=100)
        mean_delay = float(np.mean(simulated_delays))
        p95_delay = float(np.percentile(simulated_delays, 95))
        
        return {
            "mean_expected_lead_time": plan_lead_time_days + mean_delay,
            "p95_lead_time": plan_lead_time_days + p95_delay,
            "confidence": 0.85
        }

class CpSatOptimizer:
    async def generate_feasible_plan(self, context, recommendations) -> dict:
        print("[CpSatOptimizer] Formulating CP-SAT model...")
        await asyncio.sleep(0.5)
        
        model = cp_model.CpModel()
        
        # Variables: how much quantity to take from each recommendation
        req_vars = {}
        material_source_vars = []
        for idx, rec in enumerate(recommendations):
            # var: quantity assigned to this recommendation
            req_vars[idx] = model.NewIntVar(0, int(rec.proposed_quantity), f"rec_{idx}")
            if rec.action_type in ["CREATE_PO", "STOCK_TRANSFER"]:
                material_source_vars.append(req_vars[idx])
            
        # Constraint 1: Meet required quantity using only material sources
        model.Add(sum(material_source_vars) == int(context.required_quantity))
        
        # Objective: Minimize total cost
        # cost = sum(qty * cost_per_unit)
        # we approximate cost per unit = estimated_cost / proposed_quantity
        objective_terms = []
        for idx, rec in enumerate(recommendations):
            unit_cost = int(rec.estimated_cost / rec.proposed_quantity) if rec.proposed_quantity > 0 else 0
            objective_terms.append(req_vars[idx] * unit_cost)
            
        model.Minimize(sum(objective_terms))
        
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            print("[CpSatOptimizer] Feasible plan found!")
            actions = []
            total_cost = 0.0
            max_lead_time = 0
            for idx, rec in enumerate(recommendations):
                assigned_qty = solver.Value(req_vars[idx])
                if assigned_qty > 0:
                    actions.append({
                        "agent_name": rec.agent_name,
                        "action_type": rec.action_type,
                        "target_id": rec.target_id,
                        "quantity": assigned_qty,
                        "cost": assigned_qty * (rec.estimated_cost / rec.proposed_quantity)
                    })
                    total_cost += assigned_qty * (rec.estimated_cost / rec.proposed_quantity)
                    if rec.lead_time_days > max_lead_time:
                        max_lead_time = rec.lead_time_days
            
            # Run simulation
            mc = DeterministicMonteCarlo()
            sim_results = mc.simulate(max_lead_time)
            
            # Calculate Commitment Risk = Probability of failure * cost of irreversibility
            prob_failure = 1.0 - sim_results["confidence"]
            commitment_risk = prob_failure * total_cost

            return {
                "status": "FEASIBLE",
                "actions": actions,
                "total_cost": total_cost,
                "simulation": sim_results,
                "commitment_risk": commitment_risk
            }
        else:
            print("[CpSatOptimizer] NO FEASIBLE PLAN.")
            return {"status": "INFEASIBLE", "actions": []}
