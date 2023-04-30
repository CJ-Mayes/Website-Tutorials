import os
import pandas as pd

os.environ["OPENAI_API_KEY"] = "redacted - insert your key here"
df = pd.read_csv('ATP_rankings.csv')

from langchain.agents import create_csv_agent
from langchain.llms import OpenAI

agent = create_csv_agent(OpenAI(temperature=0),
                         'ATP_rankings.csv',
                         verbose=True)

agent.agent.llm_chain.prompt.template
agent.run("how many rows are there?")

agent.agent.llm_chain.prompt.template
agent.run("how many individuals have the first name Pedro? What are their full names?")

agent.agent.llm_chain.prompt.template
agent.run("how many more points do the Top 10 ranked individuals have than the bottom 10 ranked individuals combined?")
