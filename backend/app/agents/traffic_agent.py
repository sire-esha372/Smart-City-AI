from langchain_groq import ChatGroq

from .prompts import TRAFFIC_PROMPT


def traffic_agent(query, api_key):

    llm = ChatGroq(
        groq_api_key=api_key,
        model="openai/gpt-oss-20b"
    )

    prompt = f"""
{TRAFFIC_PROMPT}

User Query:

{query}
"""

    response = llm.invoke(prompt)

    return response.content