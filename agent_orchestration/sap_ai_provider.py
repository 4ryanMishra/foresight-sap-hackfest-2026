import os
import json
from agent_orchestration.interfaces import LLMProvider

# Standard imports for SAP Cloud SDK for AI (sap-ai-sdk-gen) Orchestration Service V2 API
try:
    from gen_ai_hub.orchestration_v2.service import OrchestrationService
except ImportError:
    try:
        from sap_ai_sdk_gen.orchestration_v2 import OrchestrationService
    except ImportError:
        OrchestrationService = None

class SapGenAiHubProvider(LLMProvider):
    """
    SAP Generative AI Hub Provider using sap-ai-sdk-gen Orchestration Service (V2 API).
    
    Reads credentials and configuration strictly from environment variables or secure BTP service bindings.
    Does NOT hardcode credentials.
    """
    def __init__(self):
        self.config_id = os.environ.get('AICORE_ORCHESTRATION_CONFIG_ID', '884ae7da-8003-4b37-a312-af0da9125ffc')
        self.resource_group = os.environ.get('AICORE_RESOURCE_GROUP', 'default')
        
        # Connection requires standard AICORE environment variables
        self.is_configured = bool(
            os.environ.get("AICORE_CLIENT_ID") and
            os.environ.get("AICORE_CLIENT_SECRET") and
            os.environ.get("AICORE_AUTH_URL") and
            os.environ.get("AICORE_API_BASE_URL")
        )
        
        if self.is_configured and OrchestrationService is not None:
            self.service = OrchestrationService(
                resource_group=self.resource_group
            )
        else:
            self.service = None

    async def generate_structured_response(self, prompt: str, schema: any) -> any:
        if not self.is_configured or self.service is None:
            raise RuntimeError(
                "SAP AI Core runtime credentials are NOT CONFIGURED or sap-ai-sdk-gen is not installed. "
                "Cannot execute live call."
            )
            
        print(f"[SapGenAiHubProvider] Executing Orchestration V2 Config {self.config_id} on RG {self.resource_group}")
        
        try:
            # Using Orchestration V2 API
            response = self.service.run(
                config_id=self.config_id,
                input_params={
                    "disruption_context": prompt
                }
            )
            
            # Extract content from Orchestration V2 response object/dict
            if hasattr(response, 'content'):
                result_text = response.content
            elif isinstance(response, dict):
                result_text = response.get('orchestration_result', {}).get('content', json.dumps(response))
            else:
                result_text = str(response)

            return json.loads(result_text)
            
        except Exception as e:
            print(f"[SapGenAiHubProvider] Error calling Orchestration V2 Service: {e}")
            raise
