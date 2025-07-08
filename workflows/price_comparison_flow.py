from agno.workflow import Workflow, RunResponse
from user_agents.link_discovery_agent import get_link_discovery_agent
from user_agents.match_verifier_agent import get_match_verifier_agent
from user_agents.crawler_agent import get_crawler_agent
import json
import re

def extract_first_json_object(text: str) -> str:
    """Returns first valid JSON object found in text using regex"""
    match = re.search(r'\{.*?\}', text, re.DOTALL)
    return match.group(0) if match else ""

class PriceComparisonWorkflow(Workflow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.link_agent = get_link_discovery_agent(self.session_id)
        self.match_agent = get_match_verifier_agent(self.session_id)
        self.crawler_agent = get_crawler_agent(self.session_id)
        self.crawler_agent.show_tool_calls = True

    def run(self, query: list[str], country: str, cancel_event=None) -> RunResponse:

        # Step 2: Discover links
        discovery_input = json.dumps({"query": query, "country": country})
        try:
            link_result = self.link_agent.run(discovery_input).content.strip()
            print("[DEBUG] Raw link discovery output:", repr(link_result))
            discovered_links = json.loads(link_result)
            print(f"[INFO] Discovered {len(discovered_links)} links")
        except Exception as e:
            return RunResponse(content={"error": "Failed to discover product links", "exception": str(e)})

        if cancel_event and cancel_event.is_set():
            return RunResponse(content={"status": "cancelled"})

        final_results = []
        for link in discovered_links:
            print(f"[INFO] Crawling: {link}")
            crawl_prompt = f"Extract product info from this link: {link}"
            try:
                crawl_response = self.crawler_agent.run(crawl_prompt).content.strip()
                print("[DEBUG] Raw crawl output:", crawl_response)
                item = json.loads(extract_first_json_object(crawl_response))
                print("[DEBUG]", item)
            except Exception:
                print("[WARN] No JSON found in crawl output")
                continue

            match_input = json.dumps({
                "asked_item": query,
                "scraped_item": item.get("productName", "")
            })

            try:
                match_response = self.match_agent.run(match_input).content.strip()
                if json.loads(match_response).get("match"):
                    print("[DEBUG] item", item)
                    item["link"] = link
                    final_results.append(item)
                    print("[DEBUG] final_results", final_results)

            except Exception as e:
                print("[WARN] Match agent error:", str(e))
                continue


        print(f"[INFO] Returning {len(final_results)} matched results.")
        return RunResponse(content={"results": final_results})
