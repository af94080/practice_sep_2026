# import
import os 
from dotenv import load_dotenv 
from openai import OpenAI
from tavily import TavilyClient

# load_env / api_key / client
load_dotenv()
deepseek_api_key = os.environ.get('DEEPSEEK_API_KEY')
tavily_api_key = os.environ.get('TAVILY_API_KEY')
client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")

# call llm 
# call plan : llm 
def call_llm(prompt):
    result = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages = [{
            "role": "user",
            "content": prompt
            }]
    )
    return result.choices[0].message.content

# constant
# dummy for DOC
company_handbook = """
Employees receive 15 vacation days per year.
Employees can work from home up to 3 days per week.
Employees receive 10 paid sick days per year.
"""

# router function: mimics tool
def web_agent(query):

    client = TavilyClient(api_key=tavily_api_key)
    search_query = f"current US industry average vacation days employees"
    response = client.search(search_query)
    response_short = response["results"][0]["content"]
    web_agent_prompt = f"""
    Answer the query 
    {search_query}
    Using this web result
    {response_short}
    Provide an answer.
    Give me the current US industry average for vacation days.
    Start your answer with `the current US industry average for vacation days` 
    Do not discuss the company handbook.
    Do not provide an explanation.
    """
    
    response_web_agent = call_llm(web_agent_prompt)
    return response_web_agent

def document_agent(query):
    prompt = f"""Using only the company handbook below,
    provide the company's vacation policy:
    {company_handbook}
    Provide only the vacation policy.
    Do not discuss the industry average.
    """
    return (call_llm(prompt))

def local_db(query):
    if "employee" in query:
        return("The database shows 1,250 employees.")
    else:
        return "I don't have information about that."

# agent function: calls router based on plan
def run_agent(query, plan):
    if plan == "web":
        return web_agent(query)
    elif plan == "document":
        return document_agent(query) 
    elif plan == "local_db":
        return local_db(query)            
# query
query = input("What is your question: ")

# prompt
prompt = f""" Look at the below query:

{query}

And return the source or sources.

Use only these three sources:
web
document
local_db

Return the source name or names alone in a single comma delimited string.
Do not provide any explanation.
"""

# plans

plans = call_llm(prompt)
plans = [plan.strip() for plan in plans.split(',')]
print('PLANS: ', plans)

agents = []
for plan in plans:
    if plan not in ['web','document','local_db']:
        print(f"ERROR: {plan} not expected")
    else:
        agent = run_agent(query, plan)
        agents.append(agent)
    
# show agents
print('RESULTS agents: ', agents)

# second LLM prompt
second_llm_prompt = f"""
Answer the following question:

{query}

Here are the results from the sources:

{agents}

Use the results from the selected sources to answer the question.
Do not use information that is not contained in the results.
If the results do not contain enough information to answer the question, say so.
"""

# call the LLM with the second prompt
result_2 = call_llm(second_llm_prompt)

# print the second LLM result
print('SECOND LLM CALL result: ', result_2)
