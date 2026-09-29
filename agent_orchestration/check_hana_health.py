import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_orchestration.hana_adapter import HanaPersistenceAdapter

def run_hana_health_check():
    print("==================================================")
    print(" SAP HANA CLOUD - HEALTH CHECK (Hackfest-DB)")
    print("==================================================")
    
    adapter = HanaPersistenceAdapter()
    status = adapter.health_check()

    # Credential variable presence check (without leaking secrets)
    required_vars = ["HANA_HOST", "HANA_USER", "HANA_PASSWORD"]
    print("--- Environment Configuration ---")
    for var in required_vars:
        if os.environ.get(var):
            print(f"[CONFIGURED] {var}")
        else:
            print(f"[NOT CONFIGURED] {var}")

    print(f"HANA Port                      : {adapter.port}")
    print(f"HANA Schema                    : {adapter.schema}")

    print("\n--- Connectivity & Health Status ---")
    print(f"Adapter Configured             : {'YES' if status['configured'] else 'NO'}")
    print(f"HANA Host Reachable            : {'YES' if status['reachable'] else 'NO'}")
    print(f"SELECT 1 FROM DUMMY Test       : {'PASSED' if status['test_query_passed'] else 'FAILED'}")
    
    if status['error']:
        print(f"Diagnostic Output / Message    : {status['error']}")

    print("==================================================")
    if status['reachable'] and status['test_query_passed']:
        print("STATUS: CONFIGURED & CONNECTED - Hackfest-DB live connection active.")
        print("==================================================")
        return 0
    else:
        print("STATUS: NOT CONFIGURED / UNREACHABLE - Defaulting to local SQLite / CAP fallback.")
        print("==================================================")
        return 1

if __name__ == "__main__":
    sys.exit(run_hana_health_check())
