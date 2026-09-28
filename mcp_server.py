import sys, json
from client import TokenBucketGossipNode

node = TokenBucketGossipNode()

def handle_jsonrpc(line):
    global node
    try:
        req = json.loads(line)
        req_id = req.get("id")
        method = req.get("method")
        if method == "initialize":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "genpark-multi-agent-token-bucket-gossip-protocol-skill", "version": "1.0.0"}, "capabilities": {"tools": {}}}}
        elif method == "tools/list":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [
                {"name": "gossip_broadcast", "description": "Disseminate state subject to rate limit.", "inputSchema": {"type": "object", "properties": {"key": {"type": "string"}, "value": {"type": "object"}}, "required": ["key", "value"]}},
                {"name": "benchmark_gossip_dissemination", "description": "Run gossip benchmark.", "inputSchema": {"type": "object", "properties": {}}}
            ]}}
        elif method == "tools/call":
            params = req.get("params", {})
            tool = params.get("name")
            args = params.get("arguments", {})
            if tool == "gossip_broadcast":
                res = node.broadcast(args.get("key"), args.get("value"))
            elif tool == "benchmark_gossip_dissemination":
                res = node.benchmark_gossip_dissemination()
            else:
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    except Exception as e:
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}

def main():
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_jsonrpc(line.strip())), flush=True)

if __name__ == "__main__":
    main()
