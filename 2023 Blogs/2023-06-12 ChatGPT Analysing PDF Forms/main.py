import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain import OpenAI, VectorDBQA
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter

'''
import nltk
nltk.download("punkt")
'''

import pandas as pd
loader = UnstructuredFileLoader("2023-rules-of-tennis-english.pdf")
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=3000,chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# Replace with your Key
KEY = os.environ["OPENAI_API_KEY"] = " Insert Your Key Here "
embeddings = OpenAIEmbeddings(openai_api_key=KEY)
doc_search = Chroma.from_documents(texts,embeddings)
chain = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=doc_search)

query = "During a tie-break how many points does a player need to win the game and set?"
# A generic numerical question
print(query)
print(chain.run(query))

query = "If a player is serving and it is their first serve, the ball hits the net but bounces in the correct service court, what happens?"
# Open-ended question testing the rulebooks documentation
print(query)
print(chain.run(query))

query = "What is the difference in centimetres between the baseline and the net?"
# Asking a question that is only more vaguely cited in the rulebook
print(query)
print(chain.run(query))
