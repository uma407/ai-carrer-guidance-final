"""Test sentence-transformers embeddings and FAISS vector search."""
import json
from vector_db import query_vector_db, populate_sample_data

# Ensure sample data is loaded
print("📚 Populating sample vector DB...")
try:
    populate_sample_data()
    print("✅ Sample data loaded")
except Exception as e:
    print(f"⚠️  Sample data population: {e}")

# Test vector search
print("\n🔍 Testing vector search with embeddings...")
queries = [
    "How do I start learning machine learning?",
    "Best programming languages for data science",
    "Career path for a software engineer"
]

for q in queries:
    try:
        results = query_vector_db(q, top_k=3)
        print(f"\n   Query: {q}")
        print(f"   Results ({len(results)} found):")
        for i, r in enumerate(results, 1):
            print(f"     {i}. {r[:70]}...")
    except Exception as e:
        print(f"   ❌ Query failed: {e}")

print("\n✅ Embedding test complete!")
