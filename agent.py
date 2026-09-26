from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape
from dotenv import load_dotenv
import os
load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')



model =ChatGroq(model='groq:openai/gpt-oss-120b', temperature=0)