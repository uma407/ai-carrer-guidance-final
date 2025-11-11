from crewai import CrewAI  # our lightweight crewai.py
from agent_impl import AcademicAdvisorAgent, CareerCounselorAgent, ResourceAgent

class AgenticAdvisor:
    """High-level orchestrator that uses CrewAI to coordinate multiple agents.

    Methods:
      - respond(query): runs agents and aggregates a combined reply
    """
    def __init__(self):
        self.crew = CrewAI()
        # register agents (callables)
        self.crew.register_agent('academic_advisor', AcademicAdvisorAgent())
        self.crew.register_agent('career_counselor', CareerCounselorAgent())
        self.crew.register_agent('resource_agent', ResourceAgent())

    def respond(self, query: str) -> dict:
        # Dispatch to all agents and combine results
        results = self.crew.dispatch(query)
        # Basic aggregation strategy: concatenate `text` fields and collect resources
        combined_texts = []
        combined_resources = []
        for name, res in results.items():
            if isinstance(res, dict) and 'text' in res:
                combined_texts.append(f"[{name}] {res.get('text')}")
            elif isinstance(res, dict) and 'response' in res:
                combined_texts.append(f"[{name}] {res.get('response')}")
            if isinstance(res, dict) and 'resources' in res and res['resources']:
                combined_resources.extend(res['resources'])

        aggregated = {
            'combined_text': '\n\n'.join(combined_texts),
            'resources': list(dict.fromkeys(combined_resources))[:20],
            'agent_results': results
        }
        return aggregated
