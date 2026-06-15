from openclaw import Agent

# Step 1: define tools (what the agent can do)
def search_emails(query):
    return f"Searching emails for: {query}"

def summarize(text):
    return f"Summary: {text[:50]}..."

# Step 2: create agent
agent = Agent(
    name="EmailAgent",
    tools=[search_emails, summarize],
    model="gpt-4o-mini"
)

# Step 3: run agent
response = agent.run(
    "Find emails about Project Alpha and summarize them"
)

print(response)
