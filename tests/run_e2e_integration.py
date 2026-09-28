import subprocess
import time
import requests
import sys
import os

def run_integration():
    print("Starting integration test for FORESIGHT Phase 2...")
    
    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cap_dir = os.path.join(base_dir, "sap-cap-backend")
    mock_s4_dir = os.path.join(base_dir, "mock-s4hana")
    agent_dir = os.path.join(base_dir, "agent_orchestration")

    # Start Mock S4
    print("Starting Mock S/4HANA on 8080...")
    mock_s4_proc = subprocess.Popen(
        ["node.exe", "index.js"],
        cwd=mock_s4_dir,
        shell=True
    )

    # Start Orchestrator
    print("Starting Python Orchestrator on 8000...")
    orchestrator_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api:app", "--port", "8000"],
        cwd=agent_dir,
        shell=True
    )

    # Start CAP Backend
    print("Starting SAP CAP on 4004...")
    cap_proc = subprocess.Popen(
        ["npx.cmd", "cds", "run"],
        cwd=cap_dir,
        shell=True
    )

    try:
        # Wait for services to be up
        print("Waiting 20 seconds for services to initialize...")
        time.sleep(20)

        print("\n--- TEST 1: Trigger Disruption ---")
        trigger_url = "http://localhost:4004/odata/v4/foresight/triggerDisruption"
        trigger_payload = {
            "supplierId": "SUP-001",
            "materialId": "MAT-100"
        }
        print(f"POST {trigger_url}")
        res = requests.post(trigger_url, json=trigger_payload)
        
        if res.status_code not in (200, 201):
            print(f"Failed to trigger disruption. Status: {res.status_code}")
            print(res.text)
            sys.exit(1)
            
        disruption = res.json()
        print("Disruption triggered successfully:")
        print(disruption)

        disruption_id = disruption.get("ID")
        if not disruption_id:
            disruption_id = disruption.get('value', {}).get("ID")
        
        time.sleep(10)

        print("\n--- TEST 2: Fetch Recovery Plan ---")
        plans_url = "http://localhost:4004/odata/v4/foresight/RecoveryPlans?$expand=actions"
        res = requests.get(plans_url)
        plans = res.json().get('value', [])
        
        if not plans:
            print("No recovery plans found!")
            sys.exit(1)
            
        latest_plan = plans[-1]
        plan_id = latest_plan["ID"]
        print(f"Found Plan ID: {plan_id}")
        print(f"Status: {latest_plan['status']}")
        print(f"Total Cost: {latest_plan['totalCost']}")
        print(f"Commitment Risk: {latest_plan['commitmentRisk']}")
        print(f"Actions generated: {len(latest_plan['actions'])}")
        
        for action in latest_plan['actions']:
            print(f"  -> [{action['agentName']}] {action['actionType']} {action['quantity']} units from {action['targetSupplier_ID'] or action['targetPlant_ID']}")

        print("\n--- TEST 3: Approve Plan ---")
        approve_url = "http://localhost:4004/odata/v4/foresight/approvePlan"
        approve_payload = {
            "planId": plan_id,
            "approverId": "SUPPLY_CHAIN_MGR",
            "comments": "Looks good, execute immediately."
        }
        res = requests.post(approve_url, json=approve_payload)
        
        if res.status_code not in (200, 201):
            print(f"Failed to approve plan. Status: {res.status_code}")
            print(res.text)
            sys.exit(1)
            
        print("Plan approved successfully.")

        print("\n--- TEST 4: Verify Execution (Audit Events) ---")
        audit_url = f"http://localhost:4004/odata/v4/foresight/AuditEvents?$filter=entityId eq '{plan_id}'"
        res = requests.get(audit_url)
        audits = res.json().get('value', [])
        
        for event in audits:
            print(f"Audit [{event['eventType']}]: {event['details']}")

        print("\n--- ALL TESTS PASSED! ---")

    finally:
        print("\nCleaning up processes...")
        # with shell=True, need to kill the process group or use taskkill
        subprocess.call(["taskkill", "/F", "/T", "/PID", str(mock_s4_proc.pid)])
        subprocess.call(["taskkill", "/F", "/T", "/PID", str(orchestrator_proc.pid)])
        subprocess.call(["taskkill", "/F", "/T", "/PID", str(cap_proc.pid)])

if __name__ == "__main__":
    run_integration()
