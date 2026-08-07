from langchain_groq import ChatGroq

from .prompts import EMERGENCY_PROMPT


def emergency_agent(query, api_key):

    llm = ChatGroq(
        groq_api_key=api_key,
        model="llama-3.1-8b-instant"
    )

    prompt = f"""
{EMERGENCY_PROMPT}

User Query:

{query}
"""

    response = llm.invoke(prompt)

    return response.content