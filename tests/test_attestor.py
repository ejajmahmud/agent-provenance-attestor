"""Tests for agent-provenance-attestor."""
import unittest
from agent_provenance_attestor.attestor import AgentProvenanceAttestor


class TestProvenanceAttestor(unittest.TestCase):
    def setUp(self):
        self.attestor = AgentProvenanceAttestor("secret_key_99")

    def test_chain_integrity(self):
        self.attestor.attest_action("a1", "m1", "action1", {"k": 1})
        self.attestor.attest_action("a2", "m2", "action2", {"k": 2})
        self.assertTrue(self.attestor.verify_chain())

    def test_detects_tampering(self):
        self.attestor.attest_action("a1", "m1", "action1", {"k": 1})
        # Alter signature
        self.attestor._chain[0].signature = "tampered_sig"
        self.assertFalse(self.attestor.verify_chain())
