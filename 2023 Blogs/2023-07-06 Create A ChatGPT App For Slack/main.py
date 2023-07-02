import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain import OpenAI, LLMChain, PromptTemplate
from Tokens import SLACK_BOT_TOKEN,SLACK_APP_TOKEN, OPENAI_API_TOKEN
from langchain.memory.buffer_window import ConversationBufferWindowMemory


openai_api_key = OPENAI_API_TOKEN
# Initializes your app with your bot token and socket mode handler
app = App(token=SLACK_BOT_TOKEN)

# Langchain implementation
template = """Assistant is a large language model trained by OpenAI.
    {history}
    Human: {human_input}
    Assistant:"""

prompt = PromptTemplate(
    input_variables=["history", "human_input"],
    template=template
)

chatgpt_chain = LLMChain(
    llm=OpenAI(temperature=0),
    prompt=prompt,
    verbose=True,
    memory=ConversationBufferWindowMemory(k=2),
)

# Message handler for Slack
@app.message(".*")
def message_handler(message, say, logger):
    print(message)

    output = chatgpt_chain.predict(human_input=message['text'])
    say(output)

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()