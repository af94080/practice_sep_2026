**Description**<br>
A router-based multi-agent system that dynamically selects data sources to answer a user query, then synthesizes a final answer.<br>
<br>
1. An LLM (DeepSeek) acts as a router — it reads the user's query and decides which source(s) are needed: `web`, `document`, or `local_db`, returned as a comma-separated list.<br>
2. The **document agent** answers strictly from a hardcoded company handbook (vacation, WFH, and sick day policy).<br>
3. The **web agent** queries Tavily for the current US industry average vacation days, then asks the LLM to summarize that search result.<br>
4. The **local_db agent** is a stubbed-out lookup that returns a canned employee count if "employee" appears in the query.<br>
5. Each selected agent's output is collected into a list, keeping sources isolated so they don't cross-contaminate each other's answers.<br>
6. A second LLM call takes the original query plus all agent results and produces one final, grounded answer — instructed to say so if the combined results are insufficient.
