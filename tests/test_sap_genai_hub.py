import os
import unittest
from agent_orchestration.sap_ai_provider import SapGenAiHubProvider

class TestSapGenAiHubProvider(unittest.IsolatedAsyncioTestCase):
    
    def test_provider_import_and_initialization(self):
        """
        Verify that SapGenAiHubProvider imports cleanly and initializes in mock fallback mode.
        """
        provider = SapGenAiHubProvider()
        self.assertEqual(provider.config_id, os.environ.get('AICORE_ORCHESTRATION_CONFIG_ID', '884ae7da-8003-4b37-a312-af0da9125ffc'))
        self.assertEqual(provider.resource_group, os.environ.get('AICORE_RESOURCE_GROUP', 'default'))
        # Should be unconfigured when credentials are not present in environment
        if not os.environ.get("AICORE_CLIENT_ID"):
            self.assertFalse(provider.is_configured)
            self.assertIsNone(provider.service)

    @unittest.skipUnless(
        os.environ.get("AICORE_CLIENT_ID") and os.environ.get("AICORE_CLIENT_SECRET"), 
        "Skipping live SAP AI Core test because AICORE_CLIENT_ID / AICORE_CLIENT_SECRET are not set."
    )
    async def test_live_orchestration_service(self):
        """
        Optional integration test that runs ONLY when SAP credentials are present.
        """
        provider = SapGenAiHubProvider()
        
        # We ensure it initialized successfully
        self.assertTrue(provider.is_configured)
        self.assertIsNotNone(provider.service)
        
        # Test basic invocation
        test_context = "TEST_DISRUPTION: Simulated connectivity test."
        try:
            response = await provider.generate_structured_response(test_context, schema={})
            self.assertIsInstance(response, dict, "Expected Orchestration V2 service to return structured response.")
            print("Successfully received structured response from SAP GenAI Hub (V2 API).")
        except Exception as e:
            self.fail(f"Live orchestration call failed: {e}")

if __name__ == '__main__':
    unittest.main()
