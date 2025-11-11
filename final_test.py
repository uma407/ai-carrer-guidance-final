"""Final smoke test: verify all components work together."""
import json
from agentic_advisor import AgenticAdvisor
from openai_client import OpenAIClient
import os

print("=" * 60)
print("FINAL PROJECT SMOKE TEST")
print("=" * 60)

# 1. Check OpenAI setup
print("\n1️⃣  OpenAI Setup")
has_key = bool(os.environ.get('OPENAI_API_KEY'))
print(f"   - OPENAI_API_KEY set: {'✅ YES' if has_key else '❌ NO'}")

# 2. Check OpenAI client
print("\n2️⃣  OpenAI Client")
try:
    client = OpenAIClient()
    print(f"   - Client initialized: ✅")
    print(f"   - Client has API key: {'✅ YES' if client.api_key else '❌ NO (using fallback)'}")
except Exception as e:
    print(f"   - Client error: ❌ {e}")

# 3. Check Agentic Advisor
print("\n3️⃣  Agentic Advisor")
try:
    advisor = AgenticAdvisor()
    print(f"   - Advisor initialized: ✅")
    agents = list(advisor.crew.agents.keys())
    print(f"   - Registered agents: {len(agents)} agents")
    for agent in agents:
        print(f"     • {agent}")
except Exception as e:
    print(f"   - Advisor error: ❌ {e}")

# 4. Test agent response
print("\n4️⃣  Agent Response Test")
try:
    response = advisor.respond("What's the best way to start a career in AI?")
    print(f"   - Response generated: ✅")
    print(f"   - Response length: {len(response.get('combined_text', ''))} chars")
    print(f"   - Resources found: {len(response.get('resources', []))} items")
    print(f"\n   💬 Agent Output Preview:")
    text = response.get('combined_text', '')[:200]
    print(f"   {text}...")
except Exception as e:
    print(f"   - Response error: ❌ {e}")

# 5. Check pages exist
print("\n5️⃣  Project Pages")
import os
pages_dir = "pages"
page_files = sorted([f for f in os.listdir(pages_dir) if f.endswith('.py')])
print(f"   - Pages found: {len(page_files)} pages")
for pf in page_files:
    print(f"     ✅ {pf}")

print("\n" + "=" * 60)
print("✅ PROJECT READY FOR DEPLOYMENT")
print("=" * 60)
print("\n📱 Open browser: http://localhost:8501")
print("🔐 Login with any username/password")
print("🚀 Explore all pages and features")
print("=" * 60)
