from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.googlesearch import GoogleSearchTools
from textwrap import dedent


def get_link_discovery_agent(session_id="link-discovery"):
    return Agent(
        name="link_discovery",
        session_id=session_id,
        model=Groq(id="deepseek-r1-distill-llama-70b", max_retries=1),
        tools=[GoogleSearchTools()],
        markdown=False,
        debug_mode=True,
        description="Search and return e-commerce links for a given product query in a specific country.",
        instructions=[
            "Return a **JSON array** of URLs where the exact product can be bought.",
            "Always perform GoogleSearch using: 'Buy {query} online in {country}'",
            "NEVER search for other brands or categories — only use what's in the query.",
            "Return only product/ecommerce links — NO reviews, blogs, or videos.",
            "Only return a clean JSON array. No markdown, no explanations.",
        ],
        additional_context=dedent(
            """
            You will be given:
            - A product query like "iPhone 16 Pro 128GB"
            - A country like "IN"

            You MUST run a commercial search using: "Buy iPhone 16 Pro 128GB online in IN".

            Examples:
            ✅ Good output:
            [
            "https://www.apple.com/in/iphone-16-pro",
            "https://www.flipkart.com/apple-iphone-16-pro/p/itm...",
            "https://www.amazon.in/dp/B0CHX2VPDR"
            ]

            ❌ Never include:
            - Reviews, comparisons, blogs
            - Markdown or explanation text
            """
        ),
    )
