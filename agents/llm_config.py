# agents/llm_config.py
# Shared LLM configuration for NYAYA_GPT agents.
#
# Strategy to stay within Groq free-tier rate limits (TPM):
#   - Simple agents (no tools): Use Llama 4 Scout 17B (higher TPM bucket)
#   - Tool agents (Pinecone/Tavily): Use Llama 3.1 8B Instant (tool-calling support)
#
# Using hosted_vllm/ prefix with Groq's OpenAI-compatible endpoint
# to avoid needing the LiteLLM dependency.

import os
from crewai import LLM
from dotenv import load_dotenv

load_dotenv()

def get_llm(temperature=0.1):
    """Llama 4 Scout 17B — used by simple agents that don't call external tools.
    Separating onto a different model avoids sharing TPM quota with tool-calling agents."""
    return LLM(
        model="hosted_vllm/meta-llama/llama-4-scout-17b-16e-instruct",
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
        temperature=temperature,
        max_tokens=4096,
    )

def get_smart_llm(temperature=0.1):
    """Llama 3.1 8B Instant — used by tool-calling agents (legal search, precedents, state law).
    This model has strong function/tool calling support on Groq. Max tokens reduced to 512 to stay under 6000 TPM limit."""
    return LLM(
        model="hosted_vllm/llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
        temperature=temperature,
        max_tokens=512,
    )
