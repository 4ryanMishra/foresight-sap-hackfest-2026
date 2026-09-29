import os
import json
from agent_orchestration.interfaces import LLMProvider

try:
    from sap_ai_sdk_gen.orchestration import OrchestrationClient
except ImportError:
    OrchestrationClient = None

class SapGenAiHubProvider(LLMProvider):
    """
    SAP Generative AI Hub Provider using sap-ai-sdk-gen Orchestration Service.
    
    Reads credentials and URLs from environment variables or secure BTP service bindings.
    Does NOT hardcode credentials.
    """
    def __init__(self):
        # We assume the environment has been populated by BTP VCAP_SERVICES or local .env
        self.config_id = os.environ.get('AICORE_ORCHESTRATION_CONFIG_ID', '884ae7da-8003-4b37-a312-af0da9125ffc')
        self.resource_group = os.environ.get('AICORE_RESOURCE_GROUP', 'default')
        
        # Connection requires standard AICORE environment variables (AICORE_CLIENT_ID, AICORE_CLIENT_SECRET, etc.)
        self.is_configured = bool(os.environ.get("AICORE_CLIENT_ID"))
        
        if self.is_configured and OrchestrationClient is not None:
            self.client = OrchestrationClient(resource_group=self.resource_group)
        else:
            self.client = None

    async def generate_structured_response(self, prompt: str, schema: any) -> any:
        if not self.is_configured or self.client is None:
            raise RuntimeError("SAP AI Core runtime credentials are UNVERIFIED or sap-ai-sdk-gen is not installed. Cannot execute live call.")
            
        print(f"[SapGenAiHubProvider] Calling Orchestration Config {self.config_id} on RG {self.resource_group}")
        
        # The prompt represents the disruption context or agent context
        # We pass it as the orchestration input under the 'disruption_context' key
        try:
            # Using the official SDK approach for orchestration
            response = self.client.run_orchestration(
                configuration_id=self.config_id,
                input_params={
                    "disruption_context": prompt
                }
            )
            
            # The orchestration service will return the JSON string from the LLM based on the config.
            # We parse the response content and return the dict.
            result_text = response.get('orchestration_result', {}).get('content', '{}')
            return json.loads(result_text)
            
        except Exception as e:
            print(f"[SapGenAiHubProvider] Error calling Orchestration Service: {e}")
            raise
