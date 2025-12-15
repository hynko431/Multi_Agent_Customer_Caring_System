# 🧪 System Test Queries

This file contains 12 specialized queries designed to test different parts of the Multi-Agent Customer Care System.

---

### 1. Order Status (Order Agent)
**Query**: "Where is my order #12346 currently, and when is it expected to arrive?"
- **Tests**: `OrderAgent`, `order_tools.get_order_info`.

### 2. Product Specs & Comparison (Product Agent)
**Query**: "What are the key technical differences between the TechBook Pro 15 and the TechBook Air 13? I need to know about RAM and CPU."
- **Tests**: `ProductAgent`, `product_tools.get_product_info`, `product_tools.compare_products`.

### 3. Technical Troubleshooting (Tech Support Agent)
**Query**: "My TechBook Pro is running very slowly and the fan is making a loud noise. What troubleshooting steps do you recommend?"
- **Tests**: `TechSupportAgent`, `knowledge_tools.search_kb`.

### 4. Warranty Validation (Order Agent)
**Query**: "Is my order #12345 still covered under the standard warranty? I bought it last year."
- **Tests**: `OrderAgent`, `order_tools.check_warranty`.

### 5. Returns & Refund Policy (Solutions Agent)
**Query**: "What is your official policy on returning a laptop if I've already opened the box? How many days do I have?"
- **Tests**: `SolutionsAgent`, `knowledge_tools.get_policy`.

### 6. Web Search for Better Prices (Search Tools)
**Query**: "Find me the best current deals online for a TechBook Workstation 16. Are there any seasonal sales happening?"
- **Tests**: `SearchTools`, `gemini.google_search`.

### 7. Competitor Comparison (Search + Product)
**Query**: "How does the TechBook Gaming 17 compare to the latest Razer Blade 16 in terms of performance and price? Search the web for latest reviews."
- **Tests**: `SearchTools`, `ProductAgent`, `Parallel Execution`.

### 8. Troubleshooting + Warranty (Order + Tech)
**Query**: "I just received order #12345 but the WiFi isn't working at all. Can you help me fix it, or let me know if I can get a replacement under warranty?"
- **Tests**: `OrderAgent`, `TechSupportAgent`, `Sequential Execution`.

### 9. Exchange Request (Order + Product + Solutions)
**Query**: "I bought the TechBook Air 13 (order #12347) but I realize I need more power. Can I exchange it for a TechBook Pro 15, and what would the price difference be?"
- **Tests**: `OrderAgent`, `ProductAgent`, `SolutionsAgent`, `Conditional Execution`.

### 10. Deep Knowledge Base Search (Tech Support)
**Query**: "I'm looking for the specific steps to reset the BIOS on a TechBook series laptop. Can you find that in your technical manual?"
- **Tests**: `TechSupportAgent`, `knowledge_tools.search_kb` (Specific query).

### 11. Availability & Live Pricing (Product Agent)
**Query**: "Do you have the TechBook Workstation 16 in stock right now? If so, what is the current price including any internal discounts?"
- **Tests**: `ProductAgent`, `product_tools.get_product_info`.

### 12. The "Ultimate" Coordination Test (All Agents)
**Query**: "I'm having a lot of trouble with my TechBook Pro 15 from order #12345. The WiFi keeps disconnecting and it feels slow. Can you help me troubleshoot? Also, if I can't fix it, I'm thinking about returning it for a TechBook Workstation 16. Can you check my return eligibility, compare those two models, and search the web for any competitor reviews or better deals on high-end workstations currently available?"
- **Tests**: `Orchestrator`, `OrderAgent`, `TechSupportAgent`, `ProductAgent`, `SolutionsAgent`, `SearchTools`, `Complex Coordination`.
