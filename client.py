import time
from typing import List, Dict, Any

class TokenBucketGossipNode:
    def __init__(self, node_id: str = "swarm-node-01", capacity: int = 10, refill_rate: float = 2.0):
        self.node_id = node_id
        self.capacity = capacity
        self.tokens = float(capacity)
        self.refill_rate = refill_rate
        self.last_refill = time.time()
        self.state_store: Dict[str, Any] = {}

    def _refill(self):
        now = time.time()
        self.tokens = min(self.capacity, self.tokens + (now - self.last_refill) * self.refill_rate)
        self.last_refill = now

    def broadcast(self, key: str, value: Any) -> Dict[str, Any]:
        self._refill()
        if self.tokens < 1.0:
            return {"status": "RATE_LIMITED", "tokens_available": round(self.tokens, 2)}
        self.tokens -= 1.0
        self.state_store[key] = {"value": value, "origin": self.node_id, "timestamp": time.time()}
        return {"status": "DISSEMINATED", "key": key, "tokens_remaining": round(self.tokens, 2)}

    def benchmark_gossip_dissemination(self) -> Dict[str, Any]:
        b1 = self.broadcast("heartbeat", "OK")
        b2 = self.broadcast("leader_status", "ACTIVE")
        return {"b1": b1, "b2": b2, "keys": list(self.state_store.keys())}
