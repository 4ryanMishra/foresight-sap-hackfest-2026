import os
import sys

def run_health_check():
    print("==================================================")
    print(" SAP GENERATIVE AI HUB - HEALTH CHECK (V2 API)")
    print("==================================================")
    
    # Check for the SDK and Orchestration V2 API
    sdk_available = False
    sdk_version = "NOT INSTALLED"
    try:
        import sap_ai_sdk_gen
        sdk_version = getattr(sap_ai_sdk_gen, "__version__", ">=2.0.0 (Unspecified)")
    except ImportError:
        try:
            import gen_ai_hub
            sdk_version = getattr(gen_ai_hub, "__version__", ">=2.0.0 (gen_ai_hub)")
        except ImportError:
            pass

    try:
        from gen_ai_hub.orchestration_v2.service import OrchestrationService
        print(f"[OK] sap-ai-sdk-gen / gen_ai_hub package is available (Version: {sdk_version}).")
        print("[OK] Orchestration V2 Service API imported successfully (gen_ai_hub.orchestration_v2.service.OrchestrationService).")
        sdk_available = True
    except ImportError:
        try:
            from sap_ai_sdk_gen.orchestration_v2 import OrchestrationService
            print(f"[OK] sap-ai-sdk-gen package is available (Version: {sdk_version}).")
            print("[OK] Orchestration V2 Service API imported successfully (sap_ai_sdk_gen.orchestration_v2.OrchestrationService).")
            sdk_available = True
        except ImportError:
            print(f"[WARN] sap-ai-sdk-gen / gen_ai_hub package is NOT INSTALLED or Orchestration V2 is unavailable.")

    # Check for basic AI Core environment variables per official SAP Cloud SDK for AI documentation
    required_vars = [
        "AICORE_CLIENT_ID",
        "AICORE_CLIENT_SECRET",
        "AICORE_AUTH_URL",
        "AICORE_BASE_URL"
    ]
    
    all_vars_present = True
    print("\n--- Credential Status ---")
    for var in required_vars:
        if os.environ.get(var):
            print(f"[CONFIGURED] {var}")
        else:
            print(f"[NOT CONFIGURED] {var}")
            all_vars_present = False
            
    # Check Orchestration V2 config details
    config_id = os.environ.get('AICORE_ORCHESTRATION_CONFIG_ID', '884ae7da-8003-4b37-a312-af0da9125ffc')
    rg = os.environ.get('AICORE_RESOURCE_GROUP', 'default')
    
    print("\n--- Orchestration V2 Settings ---")
    print(f"API Version                    : V2")
    print(f"Orchestration Config ID        : {config_id}")
    print(f"Resource Group (Env)           : {rg}")
    
    print("\n==================================================")
    if all_vars_present and sdk_available:
        print("STATUS: CONFIGURED - Ready for live SAP Generative AI Hub calls.")
        print("==================================================")
        return 0
    else:
        print("STATUS: NOT CONFIGURED - Missing environment variables or SDK package.")
        print("Fallback Mode: Deterministic MockLLMProvider active.")
        print("==================================================")
        return 1

if __name__ == "__main__":
    sys.exit(run_health_check())
