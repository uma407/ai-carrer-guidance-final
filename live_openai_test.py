"""
Live OpenAI integration test.

This script demonstrates the OpenAI integration in action:
1. Creates an AgenticAdvisor
2. Runs a query through it (will use OpenAI if key is present, fallback otherwise)
3. Prints the combined response and per-agent breakdown
4. Saves the response to a file

Note: If OPENAI_API_KEY is not set, this will return deterministic fallback responses.
To test with live OpenAI, set the environment variable before running:
  $env:OPENAI_API_KEY = "sk-..."
  python live_openai_test.py
"""
import os
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
RESULTS_DIR = ROOT / 'data' / 'debug_logs'
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("Live OpenAI Integration Test")
print("=" * 80)

# Check environment
api_key_set = bool(os.environ.get('OPENAI_API_KEY'))
print(f"\n[INFO] OPENAI_API_KEY in environment: {'✓ YES' if api_key_set else '✗ NO (will use fallback)'}\n")

# Import and run
from agentic_advisor import AgenticAdvisor
from career_chatbot import CareerChatbot

# Test 1: Chatbot direct query
print("TEST 1: Career Chatbot Query")
print("-" * 80)
bot = CareerChatbot()
chatbot_query = "How do I become a Data Scientist? What skills should I learn?"
chatbot_resp = bot.get_response(chatbot_query)
print(f"Query: {chatbot_query}")
print(f"Response:\n{chatbot_resp}\n")

# Test 2: Full AgenticAdvisor aggregation
print("TEST 2: AgenticAdvisor Full Aggregation")
print("-" * 80)
advisor = AgenticAdvisor()
main_query = "How do I become a Data Scientist?"
print(f"Query: {main_query}")

agg_result = advisor.respond(main_query)

print("\nCombined Aggregated Response:")
print(agg_result.get('combined_text'))

print("\nPer-Agent Breakdown:")
for agent_name, agent_result in agg_result.get('agent_results', {}).items():
    if isinstance(agent_result, dict):
        print(f"\n  [{agent_name}]")
        print(f"    Text: {agent_result.get('text', 'N/A')[:100]}...")
        print(f"    Resources: {agent_result.get('resources', [])}")

print("\nResources Recommended:")
for i, res in enumerate(agg_result.get('resources', []), 1):
    print(f"  {i}. {res}")

# Save full result for reference
ts = int(datetime.now().timestamp())
result_file = RESULTS_DIR / f'live_openai_test_{ts}.json'
with result_file.open('w', encoding='utf-8') as f:
    json.dump({
        'timestamp': ts,
        'openai_available': api_key_set,
        'query': main_query,
        'chatbot_response': chatbot_resp,
        'aggregated_response': agg_result
    }, f, ensure_ascii=False, indent=2)

print(f"\n[SUCCESS] Full test results saved to: {result_file}")
print("=" * 80)
print("\nNOTE: If you want to test with LIVE OpenAI:")
print("  1. Set your API key: $env:OPENAI_API_KEY = 'sk-...'")
print("  2. Run this script again: python live_openai_test.py")
print("  3. You should see non-fallback responses from OpenAI")
print("=" * 80)
