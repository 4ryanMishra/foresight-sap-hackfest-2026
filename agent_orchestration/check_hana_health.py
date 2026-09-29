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

    print("--- Environment Configuration ---")
    print(f"HANA Host                      : {adapter.host}")
    print(f"HANA Port                      : {adapter.port}")
    print(f"HANA User                      : {adapter.user}")
    print(f"HANA Schema                    : {adapter.schema}")
    print(f"HANA Password (Env)            : {'[CONFIGURED]' if os.environ.get('HANA_PASSWORD') else '[NOT CONFIGURED]'}")

    print("\n--- Connectivity & Health Status ---")
    print(f"Adapter Configured             : {'YES' if status['configured'] else 'NO'}")
    print(f"HANA Host Reachable            : {'YES' if status['reachable'] else 'NO'}")
    print(f"Current DB User                : {status.get('current_user') or 'N/A'}")
    print(f"Current DB Schema              : {status.get('current_schema') or 'N/A'}")
    print(f"SELECT CURRENT_USER Test       : {'PASSED' if status['test_query_passed'] else 'FAILED'}")
    
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
