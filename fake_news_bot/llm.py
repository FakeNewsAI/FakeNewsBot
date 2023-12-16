import os
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.agents import load_tools
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.cache import SQLiteCache
from langchain.globals import set_llm_cache
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

set_llm_cache(SQLiteCache(database_path=".langchain.db"))
load_dotenv()

template = """Act like fake news identifier who identifies whether the given news is true or false based on internet results or contexts given to you. Simply output whether the given news is True or False based on the given knowledge, do not output anything else. If the the event is old, explicitly mention it happended in the past. If you do not find any relevent sources, specify and classify the news as false.

News: {prompt}
"""

prompt = PromptTemplate(template=template, input_variables=["prompt"])


# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.environ.get("GEMINI_KEY"))


search = GoogleSearchAPIWrapper(google_api_key=os.environ.get("GOOGLE_SEARCH_KEY"))


def top5_results(query):
    return search.results(query, 5)


tool = [
    Tool(
        name="Google search",
        description="search Google for recent results on internet.",
        func=top5_results,
    )
]

agent_decider = initialize_agent(
    tool,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_tokens_limit=2048,
    return_intermediate_steps=True,
    max_iterations=10,
)


def ask_llm(prompt: str):
    return agent_decider({"input": prompt.format(prompt=prompt)})
