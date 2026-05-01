# agents/llm_config.py
# Shared LLM configuration. 
# We use 70B for agents with tools (to prevent hallucinations) 
# and 8B for drafting/logic (to save tokens).

import os
from crewai import LLM
from dotenv import load_dotenv

load_dotenv()

def get_llm(temperature=0.1):
    """Fast 8B model for drafting and logical steps."""
    return LLM(
        model="hosted_vllm/llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
        temperature=temperature
    )

def get_smart_llm(temperature=0.1):
    """Powerful 70B model for agents that use Tools (prevents brave_search hallucinations)."""
    return LLM(
        model="hosted_vllm/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
        temperature=temperature
    )
