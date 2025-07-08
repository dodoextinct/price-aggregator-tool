from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.crawl4ai import Crawl4aiTools
from agno.models.openai import OpenAIChat


def get_crawler_agent(session_id="crawl-agent"):
    return Agent(
        name="crawler_agent",
        session_id=session_id,
        model=Groq(id="deepseek-r1-distill-llama-70b", max_retries=1),
        tools=[Crawl4aiTools(max_length=3500)],
        show_tool_calls=True,
        markdown=False,
        description="Extract structured product information from a given URL using Crawl4ai tool.",
        instructions=[
            "Use Crawl4ai tool to fetch the URL.",
            "Only extract the product title, price, currency, and link.",
            "Skip unrelated sections, review tabs, or footer text.",
            "If multiple products are returned, only select the top relevant one.",
            "Return JSON like: {productName, price, currency, link}",
        ],
        additional_context="""
        You will be given a product page URL. Use the Crawl4ai tool to extract the content.

        From the extracted content, extract the most accurate:
        - productName
        - price (as number)
        - currency (e.g., INR or ₹)
        - original link

        Example Output:
        {
          "productName": "boAt Airdopes 311 Pro",
          "price": 1799,
          "currency": "INR",
          "link": "https://www.example.com/airdopes-311-pro"
        }
        """,
        debug_mode=True,
    )
