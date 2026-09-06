# import lib
import os 
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# set api key 
api_key = os.environ.get('DEEPSEEK_API_KEY')

# connect to llm 
client = OpenAI(api_key=api_key, 
	base_url="https://api.deepseek.com")

# accept user input vars
food= input('What food are you interested in: ')
question= input('What is your question: ')

# define prompt
prompt=f""" {question} in {food}. Keep the answers short. Less than 50 words. Format the answers nicely. One short sentence per line."""

# call llm 
response=client.chat.completions.create(
	model="deepseek-v4-flash",
	messages=[{
	"role":"system",
	"content":"you are a nutrition assistant. Answer the user's nutrition question directly and briefly."
	},{
	"role":"user",
	"content":prompt
	}])

# print response
answer = response.choices[0].message.content
print(answer)
