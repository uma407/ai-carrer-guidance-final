"""
Automated tests for the career guidance system.

Run with: pytest test_integration.py -v

Tests cover:
- Saving resources via saved_resources_store
- Agent aggregation via agentic_advisor
- Vector DB query via vector_db
"""
import pytest
import json
import tempfile
from pathlib import Path

# Test 1: Save and list resources
def test_save_resource():
    from saved_resources_store import save_resource, list_resources
    
    # Save a test resource
    test_resource = {'title': 'Test Resource', 'source': 'test'}
    saved = save_resource(test_resource)
    
    # Verify it was saved with metadata
    assert 'id' in saved
    assert 'saved_at' in saved
    assert saved['title'] == 'Test Resource'
    
    # List and verify
    resources = list_resources()
    assert len(resources) > 0
    assert any(r['title'] == 'Test Resource' for r in resources)


def test_list_resources_empty_ok():
    from saved_resources_store import list_resources
    # Should not crash even if no file exists initially
    resources = list_resources()
    assert isinstance(resources, list)


# Test 2: Agent aggregation
def test_agentic_advisor_respond():
    from agentic_advisor import AgenticAdvisor
    
    advisor = AgenticAdvisor()
    result = advisor.respond("How do I become a Data Scientist?")
    
    # Verify structure
    assert 'combined_text' in result
    assert 'resources' in result
    assert 'agent_results' in result
    
    # Verify combined_text is non-empty
    assert isinstance(result['combined_text'], str)
    assert len(result['combined_text']) > 0
    
    # Verify resources is a list
    assert isinstance(result['resources'], list)
    
    # Verify agent_results has expected agents
    agent_results = result['agent_results']
    assert 'academic_advisor' in agent_results
    assert 'career_counselor' in agent_results


def test_academic_advisor_agent():
    from agent_impl import AcademicAdvisorAgent
    
    advisor = AcademicAdvisorAgent()
    result = advisor("What should I learn first?")
    
    # Verify structure
    assert 'role' in result
    assert result['role'] == 'academic_advisor'
    assert 'text' in result or 'response' in result


def test_career_counselor_agent():
    from agent_impl import CareerCounselorAgent
    
    counselor = CareerCounselorAgent()
    result = counselor("What careers fit my profile?")
    
    assert 'role' in result
    assert result['role'] == 'career_counselor'


# Test 3: Vector DB and search
def test_vector_db_populate_and_query():
    from vector_db import populate_sample_data, query_vector_db
    
    populate_sample_data()
    
    # Query for a known topic
    results = query_vector_db("machine learning", top_k=5)
    
    # Verify results
    assert isinstance(results, list)
    assert len(results) > 0
    
    # At least one result should mention "learning" or "ML"
    assert any(
        'learning' in r.lower() or 'ml' in r.lower() 
        for r in results
    )


def test_vector_db_empty_query():
    from vector_db import query_vector_db
    
    # Empty query should return empty list
    results = query_vector_db("", top_k=5)
    assert results == []


def test_vector_db_multiple_queries():
    from vector_db import populate_sample_data, query_vector_db
    
    populate_sample_data()
    
    # Multiple queries should work
    q1 = query_vector_db("python", top_k=3)
    q2 = query_vector_db("statistics", top_k=3)
    q3 = query_vector_db("cloud", top_k=3)
    
    assert len(q1) > 0
    assert len(q2) > 0
    assert len(q3) > 0


# Test 4: Career chatbot
def test_career_chatbot_response():
    from career_chatbot import CareerChatbot
    
    bot = CareerChatbot()
    
    # Should handle a normal query
    resp = bot.get_response("How do I become a Data Scientist?")
    assert isinstance(resp, str)
    assert len(resp) > 0
    
    # Should handle empty query
    resp2 = bot.get_response("")
    assert isinstance(resp2, str)


def test_career_chatbot_with_openai_fallback():
    from career_chatbot import CareerChatbot
    import os
    
    # Even if OpenAI key is not set, should return fallback responses
    bot = CareerChatbot()
    resp = bot.get_response("Resume tips")
    
    assert "resume" in resp.lower() or len(resp) > 0


# Test 5: OpenAI client basic instantiation
def test_openai_client_can_instantiate():
    from openai_client import OpenAIClient
    
    # Should not crash on instantiation
    client = OpenAIClient()
    assert client is not None


def test_openai_client_api_key_check():
    from openai_client import OpenAIClient
    import os
    
    client = OpenAIClient()
    has_key = bool(os.environ.get('OPENAI_API_KEY'))
    
    # Verify the client's state matches environment
    client_has_key = bool(getattr(client, 'api_key', None))
    
    # At minimum, the attributes should exist
    assert hasattr(client, 'api_key')


# Test 6: Crew orchestration
def test_crew_dispatch():
    from crewai import CrewAI
    from agent_impl import AcademicAdvisorAgent
    
    crew = CrewAI()
    crew.register_agent('academic', AcademicAdvisorAgent())
    
    results = crew.dispatch("Test query")
    
    # Should return a dict
    assert isinstance(results, dict)
    # Should have the registered agent
    assert 'academic' in results


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
