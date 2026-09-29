import os
import unittest
import asyncio
from agent_orchestration.sap_ai_provider import SapGenAiHubProvider

class TestSapGenAiHubProvider(unittest.IsolatedAsyncioTestCase):
    
    @unittest.skipUnless(os.environ.get("AICORE_CLIENT_ID"), "Skipping live SAP AI Core test because AICORE_CLIENT_ID is not set.")
    async def test_live_orchestration_service(self):
        """
        Optional integration test that runs ONLY when SAP credentials are present.
        """
        provider = SapGenAiHubProvider()
        
        # We ensure it initialized successfully
        self.assertTrue(provider.is_configured)
        self.assertIsNotNone(provider.client)
        
        # Test basic invocation
        test_context = "TEST_DISRUPTION: Simulated connectivity test."
        try:
            response = await provider.generate_structured_response(test_context, schema={})
            self.assertIsInstance(response, dict, "Expected the orchestration service to return a structured JSON response (parsed as dict).")
            print("Successfully received structured response from SAP GenAI Hub.")
        except Exception as e:
            self.fail(f"Live orchestration call failed: {e}")

if __name__ == '__main__':
    unittest.main()
