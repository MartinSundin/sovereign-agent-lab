"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ['search_venues', 'get_venue_details']

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = """
I searched the Edinburgh venue database for locations that can accommodate **at least 300 guests** and also offer a **vegan menu**. Unfortunately, the current data set contains no venues that meet both of those criteria— the largest venues listed with vegan options have capacities of 180 and 160 guests.

If you’re flexible on any of the requirements, here are a couple of options that do provide ...
"""

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True   # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
I only updated the mcp_venue_server.py file for this specific exercise.
There were several other things I needed to change to run exercise 4.
1. Change model from meta-llama/Llama-3.3-70B-Instruct to nvidia/nemotron-3-super-120b-a12b. Llama ignores the tool output for some reason. This can be fixed but is more cumbersome than changing the model.
2. The function calling was called with empty arguments since the kwargs input had the form {'kwargs': {'min_capacity': 200, 'requires_vegan': True}}. This could be fixed by changing the code to:
  await session.initialize()
  result = await session.call_tool(tool_name, kwargs["kwargs"])
  return result.content[0].text if result.content else "{}"
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 5   # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 27   # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP offers the flexibility to wrap functions into decorators and you can use 'native' outputs, i.e. they do not need to be wrapped as json at every step. However, this could offer some drawbacks when one is composing functions and the discovery method is quite complicated.
"""

# ── Week 5 architecture ────────────────────────────────────────────────────
# Describe your full sovereign agent at Week 5 scale.
# At least 5 bullet points. Each bullet must be a complete sentence
# naming a component and explaining why that component does that job.

WEEK_5_ARCHITECTURE = """
- FILL ME IN
- FILL ME IN
- FILL ME IN
- FILL ME IN
- FILL ME IN
- Will come back to this exercise in week 5, I think is the idea
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
FILL ME IN
"""


foo = """
=================================================================
  Query 1 — Search + Detail Fetch
=================================================================

  [HUMAN]
  Find Edinburgh venues for 160 guests with vegan options and give me the full address of the best match.

  [AI]
  {"type": "function", "name": "search_venues", "parameters": {"kwargs": {"min_capacity": 160, "requires_vegan": true}}}


=================================================================
  Query 2 — Impossible Constraint
=================================================================

  [HUMAN]
  Find a venue for 300 people with vegan options.

  [AI]
  {"type": "function", "name": "search_venues", "parameters": {"kwargs": {"min_capacity": 300, "requires_vegan": true}}}


─────────────────────────────────────────────────────────────────
REQUIRED EXPERIMENT (before filling in ex4_answers.py):

  1. Open sovereign_agent/tools/mcp_venue_server.py
  2. Change The Albanach's status from 'available' to 'full'
  3. Save and run this script again
  4. Compare the output to what you just saw
  5. Revert the change

  Record what changed (and what didn't) in ex4_answers.py → EX4_EXPERIMENT_RESULT

✅  Results saved to /mnt/c/Users/sundi/OneDrive/Dokument/Python Scripts/sovereign-agent-lab/week1/outputs/ex4_results.json
    Complete the experiment above, then fill in week1/answers/ex4_answers.py
"""