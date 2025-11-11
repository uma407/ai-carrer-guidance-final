"""
CrewAI-like lightweight orchestrator for agent collaboration.
This is a local, simple implementation that mimics multi-agent orchestration:
- register agents (callable objects)
- dispatch a request to a set of agents
- aggregate and return their responses

This is intentionally simple and deterministic so the frontend can run without a network.
"""
from typing import List, Dict, Callable

class CrewAI:
    def __init__(self, agents: Dict[str, Callable] = None):
        # agents is a dict name->callable(request)->dict
        self.agents = agents or {}

    def register_agent(self, name: str, handler: Callable):
        self.agents[name] = handler

    def dispatch(self, request: str, agent_names: List[str] = None) -> Dict[str, dict]:
        """Dispatch request to all agents or a subset. Returns mapping agent_name->response dict."""
        results = {}
        names = agent_names or list(self.agents.keys())
        for name in names:
            handler = self.agents.get(name)
            if handler is None:
                results[name] = {"error": "agent_not_found"}
                continue
            try:
                res = handler(request)
                results[name] = res if isinstance(res, dict) else {"response": res}
            except Exception as e:
                results[name] = {"error": str(e)}
        return results
