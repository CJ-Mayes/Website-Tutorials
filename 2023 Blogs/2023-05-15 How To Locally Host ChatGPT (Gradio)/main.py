import openai
import gradio as gr
openai.api_key = "Enter your own key here"

messages = [{"role": "system", "content": "Test"}]

def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply

demo = gr.Interface(
    fn=CustomChatGPT,
    inputs="text",
    outputs="text",
    title ="CJ - Demo"
                    )
demo.launch(share=False)
