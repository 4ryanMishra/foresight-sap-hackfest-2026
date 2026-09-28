import os
import sys
import json
import urllib.request
import urllib.error

def check_cap_runtime():
    try:
        req = urllib.request.Request("http://localhost:4004/odata/v4/foresight/$metadata")
        with urllib.request.urlopen(req, timeout=2) as response:
            if response.status == 200:
                return "RUNNING"
    except urllib.error.URLError:
        pass
    return "STOPPED"

def check_database_provider():
    # Inspect package.json
    try:
        with open("sap-cap-backend/package.json", "r") as f:
            pkg = json.load(f)
            requires = pkg.get("cds", {}).get("requires", {})
            db_kind = requires.get("db", {}).get("kind", "unknown")
            if db_kind == "sqlite":
                return "SQLite (Local Fallback)"
            elif db_kind == "hana":
                return "SAP HANA Cloud"
            return db_kind
    except Exception:
        return "UNKNOWN"

def check_hana_config():
    # Check if mta.yaml has HANA HDI container
    try:
        with open("sap-cap-backend/mta.yaml", "r") as f:
            content = f.read()
            if "com.sap.xs.hdi-container" in content:
                return "PRESENT (HDI Container configured in mta.yaml)"
    except Exception:
        pass
    return "NOT PRESENT"

def check_sap_genai():
    if os.environ.get("USE_SAP_AI_HUB") == "true":
        deployment = os.environ.get("AICORE_DEPLOYMENT_ID")
        if deployment:
            return f"CONFIGURED (Deployment: {deployment}, Orchestration: FORESIGHT_Recovery_Orchestration_v1)"
        return "PARTIALLY CONFIGURED (USE_SAP_AI_HUB=true but AICORE_DEPLOYMENT_ID missing)"
    return "NOT CONFIGURED (Using Local MockLLMProvider)"

def check_s4_adapter():
    if os.environ.get("USE_LIVE_S4") == "true":
        dest = os.environ.get("S4_DESTINATION_NAME")
        if dest:
            return f"CONFIGURED (Using LiveS4Adapter with Destination: {dest})"
        return "PARTIALLY CONFIGURED (USE_LIVE_S4=true but S4_DESTINATION_NAME missing)"
    return "NOT CONFIGURED (Using MockS4Adapter)"

def check_work_zone():
    # Check if approuter or build work zone descriptor exists
    if os.path.exists("sap-cap-backend/xs-app.json") or os.path.exists("sap-ui5-frontend/xs-app.json"):
        return "READY (AppRouter/xs-app.json found)"
    return "NOT READY (Missing AppRouter config)"

def run_diagnostics():
    print("==================================================")
    print(" FORESIGHT SAP ENVIRONMENT DIAGNOSTICS")
    print("==================================================")
    print(f"CAP Runtime Status      : {check_cap_runtime()}")
    print(f"Database Provider       : {check_database_provider()}")
    print(f"HANA Config             : {check_hana_config()}")
    print(f"SAP GenAI Provider      : {check_sap_genai()}")
    print(f"S/4 Adapter             : {check_s4_adapter()}")
    print(f"Work Zone Readiness     : {check_work_zone()}")
    print("==================================================")

if __name__ == "__main__":
    run_diagnostics()
