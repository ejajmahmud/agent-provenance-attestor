"""Core Agent Provenance Attestor implementation."""
import json
import hmac
import hashlib
import time
from typing import Dict, Any, List


class AttestationReceipt:
    def __init__(self, agent_id: str, model_id: str, action: str, data_hash: str, prev_hash: str, signature: str, timestamp: float):
        self.agent_id = agent_id
        self.model_id = model_id
        self.action = action
        self.data_hash = data_hash
        self.prev_hash = prev_hash
        self.signature = signature
        self.timestamp = timestamp

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "model_id": self.model_id,
            "action": self.action,
            "data_hash": self.data_hash,
            "prev_hash": self.prev_hash,
            "signature": self.signature,
            "timestamp": self.timestamp
        }


class AgentProvenanceAttestor:
    def __init__(self, signing_key: str):
        self.signing_key = signing_key
        self._chain: List[AttestationReceipt] = []

    def _hash_data(self, data: Any) -> str:
        s = json.dumps(data, sort_keys=True)
        return hashlib.sha256(s.encode("utf-8")).hexdigest()

    def attest_action(self, agent_id: str, model_id: str, action: str, payload: Any) -> AttestationReceipt:
        data_hash = self._hash_data(payload)
        prev_hash = self._chain[-1].signature if self._chain else "GENESIS_ROOT"
        now = time.time()

        content = f"{agent_id}:{model_id}:{action}:{data_hash}:{prev_hash}:{now}"
        sig = hmac.new(self.signing_key.encode("utf-8"), content.encode("utf-8"), hashlib.sha256).hexdigest()

        receipt = AttestationReceipt(agent_id, model_id, action, data_hash, prev_hash, sig, now)
        self._chain.append(receipt)
        return receipt

    def verify_chain(self) -> bool:
        prev = "GENESIS_ROOT"
        for r in self._chain:
            if r.prev_hash != prev:
                return False
            content = f"{r.agent_id}:{r.model_id}:{r.action}:{r.data_hash}:{r.prev_hash}:{r.timestamp}"
            expected = hmac.new(self.signing_key.encode("utf-8"), content.encode("utf-8"), hashlib.sha256).hexdigest()
            if not hmac.compare_digest(r.signature, expected):
                return False
            prev = r.signature
        return True
