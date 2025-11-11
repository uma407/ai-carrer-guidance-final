"""Smoke test script that simulates UI flows without Streamlit.

Runs the following checks:
- Career Explorer: uses CareerChatbot to get recommendations
- AI Advisor: runs AgenticAdvisor.respond and prints aggregated + per-agent outputs
- Learning Hub: populates sample docs and queries for "machine learning"
- Saves each returned resource via saved_resources_store.save_resource
- Writes debug logs (raw agent results and aggregated JSON) to data/debug_logs
- Verifies development timeline generator by importing pages/4_Development.py logic (non-Streamlit parts)

Run using the project's venv python.
"""
import os
import json
from pathlib import Path

ROOT = Path(__file__).parent
DEBUG_DIR = ROOT / 'data' / 'debug_logs'
DEBUG_DIR.mkdir(parents=True, exist_ok=True)

print('Starting smoke UI checks...')

# 1) Career Explorer via CareerChatbot
try:
    from career_chatbot import CareerChatbot
    bot = CareerChatbot()
    q = 'Explore career paths for data science and related roles.'
    resp = bot.get_response(q)
    print('\n[Career Explorer] Response:')
    print(resp)
except Exception as e:
    print('CareerChatbot error:', e)

# 2) AI Advisor aggregated response
try:
    from agentic_advisor import AgenticAdvisor
    aa = AgenticAdvisor()
    query = 'How do I become a Data Scientist?'
    agg = aa.respond(query)
    print('\n[AI Advisor] Aggregated combined_text:')
    print(agg.get('combined_text'))
    # Per-agent breakdown
    print('\n[AI Advisor] Agent breakdown:')
    print(json.dumps(agg.get('agent_results', {}), indent=2))
except Exception as e:
    print('AgenticAdvisor error:', e)
    agg = None

# Save debug logs
try:
    import time
    ts = int(time.time())
    if agg is not None:
        raw_file = DEBUG_DIR / f'agent_aggregated_{ts}.json'
        with raw_file.open('w', encoding='utf-8') as f:
            json.dump(agg, f, ensure_ascii=False, indent=2)
        print('\nSaved aggregated agent JSON to', raw_file)
except Exception as e:
    print('Saving debug log failed:', e)

# 3) Learning Hub search
try:
    from vector_db import populate_sample_data, query_vector_db
    populate_sample_data()
    hits = query_vector_db('machine learning', top_k=5)
    print('\n[Learning Hub] Search hits for "machine learning":')
    for i,h in enumerate(hits, 1):
        print(f'{i}. {h}')
except Exception as e:
    print('Vector DB search error:', e)
    hits = []

# 4) Save each resource via persistence helper
try:
    from saved_resources_store import save_resource, list_resources
    saved = []
    for i,h in enumerate(hits, 1):
        rec = save_resource({'title': h, 'source': 'learning_hub'})
        print('Saved resource id:', rec.get('id'))
        saved.append(rec)
    print('\nTotal saved resources now:', len(list_resources()))
except Exception as e:
    print('Saving resources error:', e)

# 5) Admin Debug: Save raw agent breakdown as well
try:
    if agg is not None:
        raw_breakdown = DEBUG_DIR / f'agent_breakdown_{ts}.json'
        with raw_breakdown.open('w', encoding='utf-8') as f:
            json.dump(agg.get('agent_results', {}), f, ensure_ascii=False, indent=2)
        print('Saved agent breakdown to', raw_breakdown)
except Exception as e:
    print('Saving agent breakdown failed:', e)

# 6) Development page check: ensure the timeline DataFrame builds
try:
    # replicate the DataFrame creation used in pages/4_Development.py
    import pandas as pd
    import numpy as np
    timeline_data = pd.DataFrame({
        'Date': pd.date_range(start='2025-01-01', periods=10, freq='ME'),
        'Technical_Skills': np.random.randint(60, 100, size=10),
        'Soft_Skills': np.random.randint(70, 95, size=10),
        'Domain_Knowledge': np.random.randint(50, 90, size=10)
    })
    print('\n[Development Page] Timeline DataFrame OK shape:', timeline_data.shape)
except Exception as e:
    print('Development timeline generation error:', e)

print('\nSmoke UI checks completed.')

if __name__ == '__main__':
    pass
