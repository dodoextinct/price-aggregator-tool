# 🛍️ Price Aggregator Tool

An agent-powered price comparison tool that takes a product query and country, discovers relevant e-commerce links, crawls and extracts product data (name, price, link), and returns only exact matches.

Hosted at: **[https://price-aggregator-tool.onrender.com](https://price-aggregator-tool.onrender.com)**

Approach
- This tool uses an agent-based architecture to break down the price comparison task into modular steps:
- Link Discovery Agent performs a country-specific search to find e-commerce pages for the asked query and country.
- Crawler Agent uses Crawl4AI to extract structured data like product name and price.
- Match Verifier Agent checks if scraped data semantically matches the user’s intent to ensure high accuracy.

Note:
- The model used is an open-source model and a free tier.
- This may slow the speed of result creation.
---

## 🔍 How It Works

Given a JSON input with a product query and country, the tool:

1. **Discovers links** from top e-commerce sources via a Google Search agent.
2. **Crawls product pages** using `Crawl4AI` to extract structured product data.
3. **Matches** results against the original spec to ensure only accurate matches are returned.

---

## 🧪 Test the Tool (cURL)

```bash
curl -X POST https://price-aggregator-tool.onrender.com/compare \
  -H "Content-Type: application/json" \
  -d '{
    "query": "iPhone 16 Pro, 128GB",
    "country": "US"
  }'

curl -X POST https://price-aggregator-tool.onrender.com/compare \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Single bed",
    "country": "IN"
  }'
'''

![image](https://github.com/user-attachments/assets/0bf81838-68cd-4d2c-ad88-b8c4bfcff7fa)

