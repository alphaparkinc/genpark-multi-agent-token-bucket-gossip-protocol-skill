from client import TokenBucketGossipNode

def run_example():
    print("=== GenPark Token-Bucket Gossip Example ===")
    node = TokenBucketGossipNode("agent-x", capacity=5)
    print("Broadcast:", node.broadcast("cluster_metric", {"load": 0.22}))

if __name__ == "__main__":
    run_example()
