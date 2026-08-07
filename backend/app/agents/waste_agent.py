from langchain_groq import ChatGroq

from .prompts import WASTE_PROMPT


def waste_agent(query, api_key):

    llm = ChatGroq(
        groq_api_key=api_key,
        model="llama-3.1-8b-instant"
    )

    prompt = f"""
{WASTE_PROMPT}

User Query:

{query}
"""

    response = llm.invoke(prompt)

    return response.content