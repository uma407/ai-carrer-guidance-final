import json
from agentic_advisor import AgenticAdvisor

if __name__ == '__main__':
    a = AgenticAdvisor()
    res = a.respond('How do I become a Data Scientist?')
    print(json.dumps(res, indent=2, ensure_ascii=False))
