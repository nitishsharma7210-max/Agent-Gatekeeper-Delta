import unittest
from gatekeeper import decide_request, ACTIONS, SPENDING_LIMIT

class GatekeeperTests(unittest.TestCase):
    def setUp(self):
        self.agents = {
            "AGENT-001": {
                "name": "TravelBuddy Demo",
                "customer": "Demo Customer",
                "active": True,
                "revoked_at": "",
                "permissions": ACTIONS,
            },
            "AGENT-REVOKED": {
                "name": "Old Agent",
                "customer": "Demo Customer",
                "active": False,
                "revoked_at": "2026-11-22T10:00:00+05:30",
                "permissions": ACTIONS,
            },
        }

    def test_known_agent_read_only_fares(self):
        self.assertEqual(
            decide_request(self.agents, "AGENT-001", "View fares", 0)[0],
            "ALLOW"
        )

    def test_unknown_agent_blocked(self):
        self.assertEqual(
            decide_request(self.agents, "UNKNOWN", "View fares", 0)[0],
            "BLOCK"
        )

    def test_payment_above_limit_asks(self):
        self.assertEqual(
            decide_request(self.agents, "AGENT-001", "Book flight / make payment", SPENDING_LIMIT + 1)[0],
            "ASK CUSTOMER"
        )

    def test_payment_below_limit_allowed(self):
        self.assertEqual(
            decide_request(self.agents, "AGENT-001", "Book flight / make payment", SPENDING_LIMIT - 1)[0],
            "ALLOW"
        )

    def test_revoked_agent_blocked(self):
        self.assertEqual(
            decide_request(self.agents, "AGENT-REVOKED", "View fares", 0)[0],
            "BLOCK"
        )

    def test_refund_requires_confirmation(self):
        self.assertEqual(
            decide_request(self.agents, "AGENT-001", "Request refund", 0)[0],
            "ASK CUSTOMER"
        )

if __name__ == "__main__":
    unittest.main(verbosity=2)
