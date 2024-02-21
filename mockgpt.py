import os
import gradio as gr
from openai import OpenAI

client = OpenAI(api_key = "KEY")

# upload file
uploaded_file = client.files.create(
    file = open(r"C:\Users\sarah\Downloads\both.pdf", 'rb'),
    purpose = 'assistants',
)

# create assistant
# id of existing assistant
assistant_id = "ID"

# initialize conversation history
conversation_history = ""

def ask(option, custom_input):
    global conversation_history

    # option or input
    user_input = custom_input if custom_input else option

    # update conversation history with user's input
    conversation_history += "User: " + user_input + "\n"

    # create thread
    thread = client.beta.threads.create()

    # create message inside thread with updated conversation
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=conversation_history
    )

    # run assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )   

    # retrieve assistant's response
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            for message in messages.data:
                if message.role == "assistant":
                    # Update conversation history with assistant's response
                    assistant_response = message.content[0].text.value
                    conversation_history += "AI: " + assistant_response + "\n"
                    return assistant_response

# gradio interface
iface = gr.Interface(
    fn=ask,
    inputs=[
        gr.Radio(choices=["Rules of Evidence Quiz", "Quiz On Witness Facts", "Direct Examination", "Cross Examination"], label="Select an Option"),
        gr.Textbox(label="Or input:")
    ],
    outputs="text",
    live=False
)

# launch website
iface.launch(share=True)
