import os
import sys

def run_health_check():
    print("==================================================")
    print(" SAP GENERATIVE AI HUB - HEALTH CHECK")
    print("==================================================")
    
    # Check for the SDK
    try:
        from sap_ai_sdk_gen.orchestration import OrchestrationClient
        print("[OK] sap-ai-sdk-gen package is available in the environment.")
    except ImportError:
        print("[WARN] sap-ai-sdk-gen package is NOT installed.")
    
    # Check for basic AI Core environment variables
    # Only verify presence, never print the values
    required_vars = [
        "AICORE_CLIENT_ID",
        "AICORE_CLIENT_SECRET",
        "AICORE_AUTH_URL",
        "AICORE_API_BASE_URL"
    ]
    
    all_present = True
    for var in required_vars:
        if os.environ.get(var):
            print(f"[OK] {var} is configured.")
        else:
            print(f"[MISSING] {var} is NOT configured.")
            all_present = False
            
    # Check Orchestration config details
    config_id = os.environ.get('AICORE_ORCHESTRATION_CONFIG_ID', '884ae7da-8003-4b37-a312-af0da9125ffc')
    rg = os.environ.get('AICORE_RESOURCE_GROUP', 'default')
    
    print(f"\n[INFO] Orchestration Config ID : {config_id}")
    print(f"[INFO] Resource Group          : {rg}")
    
    if all_present:
        print("\n[SUCCESS] Environment is fully configured for SAP Generative AI Hub.")
        sys.exit(0)
    else:
        print("\n[WARNING] SAP Generative AI Hub credentials are INCOMPLETE. The system will fall back to MockLLMProvider.")
        sys.exit(1)

if __name__ == "__main__":
    run_health_check()
