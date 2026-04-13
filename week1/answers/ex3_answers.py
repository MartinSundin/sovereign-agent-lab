"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->
I see an empty message. What can I assist you with?
How many guests are you confirming for tonight's event?
Your input ->  160 guests
And how many of those guests will need vegan meals?
Your input ->  ~50 vegan
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  200 deposit
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
Your input ->  /stop
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  I am calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160 guests
And how many of those guests will need vegan meals?
Your input ->  about 50
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  GBP 3000
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £3000 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
Your input ->  /stop
"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "a deposit of £3000 exceeds the organiser's authorised limit of £300"   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  just calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  I think we are about 160 people
And how many of those guests will need vegan meals?
Your input ->  what is your parking availability?
I'm sorry, I'm not trained to help with that.
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
Your input ->  I need to know if you have any AV equipment at the venue
I'm sorry, I'm not trained to help with that.
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
Your input ->  yes
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  200 GBP
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
Your input ->  yes
Thank you — booking confirmed. 160 guests, 0 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
Your input ->  /stop
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
The agent skipped asking for number of vegan meals when it got restricted and assumed zero vegan meals.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
The langgraph stated that it did not have enough information while RASA stated that it cannot assist with the query. I did not try to confuse the langchain agent as much, so it is possible that it is not a fair comparison.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ["actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
I set the escalating time to a low value (8 and 0) when I tested it (at about 9:45 am). I received the following escalation:

I need to check one thing with the organiser before I can confirm.
The issue is: it is past 16:45 — insufficient time to process the confirmation before the 5 PM deadline.
Can I call you back within 15 minutes?
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
The old RASA relied more on mechanical parsing while the new one relies more on LLM-based parsing. This is for example to parse how many guests, vegans, deposit, etc. The function from_llm (internal function) still uses python to handle the LLM output and to parse it into (non-string) values.
The old approach was more robust to hallucinations, but less flexible in terms of the inputs it could handle. One middle ground here can be to use a more classical NLP approach such as an information-extraction model to parse responses and then escalate to a more complex model when the inputs are not recognized.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
My impression is that langgraph is more flexible in terms of how it can be extended and call external tools.
As far as I know, RASA is just another tool with slightly different functionality, but both langgraph and RASA have about the same external functionality. I don't think CALM can improvise a response, it instead fails on the safe side by escalating the conversation.
In theory it is possible that a CALM agent hallucinates a tool (or tool call), but CALM seems less prone to hallucinations than langgraph.
"""
