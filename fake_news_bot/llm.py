import os
from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.globals import set_llm_cache


from fake_news_bot.chat_model import ChatGoogleGenerativeAI

from fake_news_bot.db import MySQLCache as SQLiteCache

llm_cache = SQLiteCache(database_path=".langchain.db")
set_llm_cache(llm_cache)
load_dotenv()

# system_message = "Act like fake news identifier who identifies whether the given news is true or false based on internet results or contexts given to you. Simply output whether the given news is True or False based on the given knowledge, do not output anything else. If the the event is old, explicitly mention it happended in the past. If you do not find any relevent sources, specify and classify the news as false."
system_message = "Identify the credibility of the given news below based on google search results."

template = """{system_message}

News: {prompt}
"""

prompt = PromptTemplate(template=template, input_variables=["system_message","prompt"])


# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=os.environ.get("GEMINI_KEY"),
    temperature=0.01
)


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
    max_iterations=15,
)


def ask_llm(prompt: str):
    return agent_decider({"input": prompt.format(system_message=system_message,prompt=prompt)})
