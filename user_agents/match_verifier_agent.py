from agno.agent import Agent
from agno.models.openai import OpenAIChat
from textwrap import dedent


def get_match_verifier_agent(session_id="match-verifier"):
    return Agent(
        name="match_verifier",
        session_id=session_id,
        model=OpenAIChat(id="gpt-4o", max_retries=1),
        markdown=False,
        description="Determine if a scraped product matches the user's original query intent.",
        debug_mode=True,
        instructions=[
            'Return a JSON object in this format: {"match": true/false, "reason": string}.',
            "Only return true if the product name and variant clearly match the intended specification.",
            "Do not return explanations outside of the JSON object.",
        ],
        additional_context=dedent(
            """
        You will receive:
        - A structured product specification with keys: brand, product, variant, category.
        - A scraped product name or description.

        Your task is to determine whether the scraped product matches the original intent.

        Be strict with matching:
        - Accept only high-confidence matches.
        - Minor spelling variations are okay.
        - Generic accessories or older/newer models should be rejected.

        Example Input:
        {
          "asked_item": "iPhone 16 Pro",
          "scraped_item": "Apple iPhone 16 Pro 128 GB - Space Black"
        }

        Example Output:
        {
          "match": true,
          "reason": "Exact match on brand, product, and storage variant."
        }
        """
        ),
    )
