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

# ── PyNanoClaw architecture — SPECULATION QUESTION ─────────────────────────
#
# (The variable below is still called WEEK_5_ARCHITECTURE because the
# grader reads that exact name. Don't rename it — but read the updated
# prompt: the question is now about PyNanoClaw, the hybrid system the
# final assignment will have you build.)
#
# This is a forward-looking, speculative question. You have NOT yet seen
# the material that covers the planner/executor split, memory, or the
# handoff bridge in detail — that is what the final assignment (releases
# 2026-04-18) is for. The point of asking it here is to check that you
# have read PROGRESS.md and can imagine how the Week 1 pieces grow into
# PyNanoClaw.
#
# Read PROGRESS.md in the repo root. Then write at least 5 bullet points
# describing PyNanoClaw as you imagine it at final-assignment scale.
#
# Each bullet should:
#   - Name a component (e.g. "Planner", "Memory store", "Handoff bridge",
#     "Rasa MCP gateway")
#   - Say in one clause what that component does and which half of
#     PyNanoClaw it lives in (the autonomous loop, the structured agent,
#     or the shared layer between them)
#
# You are not being graded on getting the "right" architecture — there
# isn't one right answer. You are being graded on whether your description
# is coherent and whether you have thought about which Week 1 file becomes
# which PyNanoClaw component.
#
# Example of the level of detail we want:
#   - The Planner is a strong-reasoning model (e.g. Nemotron-3-Super or
#     Qwen3-Next-Thinking) that takes the raw task and produces an ordered
#     list of subgoals. It lives upstream of the ReAct loop in the
#     autonomous-loop half of PyNanoClaw, so the Executor never sees an
#     ambiguous task.

WEEK_5_ARCHITECTURE = """
- The full autonomus agent follows a Reach pattern where a Planner first outlines the necessary steps and then Executors perform the individual tasks.
- The Planner first outlines a sequence of steps necessary to complete a task. This requires a strong reasoning model like Qwen3 since some tasks might not be possible to complete, forcing the model to reason about how to change the plan. A typical scenario is when a booking is made, but needs to be confirmed via email.
- The Executor is built to apply a tool to solve a single isolated task, e.g. researching if a venue fullfills all the criteria. For this a simpler model (e.g. Gemini Flash) that can handle tool calls can be used. A simpler model can be used to reduce spending.
- The Executor should also have a fallback logic for 'simple' failures, e.g. as part of the prompt or context. In case the fallbacks fail, the task needs to be delegated back to the Planner.
- The RASA CALM Agent has the added benefit of having access to deterministic logic. So in case a task is crucial and there is no room for hallucinations (e.g. the capacity of a venue is often approximate while serving a vegan option is crucial), the RASA agent is prefered. The Rasa agent also has easy access to speech tools for when phone calls are necessary.
- Some of the executor tasks might be long running and can require a 'session memory'. It is then necessary to build a local RAG system that keeps the session in memory until it finishes. This should ideally be decided by the planner, but can be hard-coded in some cases.
- At the end of a long running session, it needs to be decided what information should be added to the top-level memory. This task should be completed by the planner agent since it has access to the full plan and can therefore filter the session information.
- For each step, the planner needs to decide if any new information should be added to the context for each executor task. However, this might create too much overhead. It can therefore be useful if the planner inserts tags (like <tbd from="task2" id="weather">) for unknown info at planning time and that these are later populated deterministically. Such tags can also be used to determine the sequence of execution for the tasks.
- PyNanoClaw should also have some top-level failure/feedback mode that circles back to the user. E.g. 'there were no available vegan restaurants, is vegetarian a good option?'. This is to prevent the model from hallucinating. Similarly, tool calls should ideally be verified deterministically to prevent hallucinated tool calls.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
This question does require more testing and research. I can state my assumptions, but they are untested.
For the high-level planning I would use a reasoning model like Qwen3-Next-Thinking.
For the low-level execution tasks I would use a deterministic algorithm, were possible, and a simpler non-reasoning model otherwise to save tokens and time.
Swapping the models seems incorrect since building the plan requires more 'thinking', a simple model would output something that can contain flaws.Similarly, using a reasoning model for a task where the goal is well defined means that the model will spend time reasoning if the step is correct although this has already been determined by the planner.
"""
