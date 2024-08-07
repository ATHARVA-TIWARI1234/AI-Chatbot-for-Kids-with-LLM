import chainlit as cl
from langchain.llms import OpenAI
import time
import json
import tiktoken
import numpy as np
from collections import defaultdict 
from openai import OpenAI
from gtts import gTTS 
import shutil
import openai
client = OpenAI(api_key="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")

@cl.on_message
async def main(message: cl.Message):

    images = [file for file in message.elements]
    print(images[0])
    audio_file = open(images[0].path, "rb")
    print(audio_file)
    new_file_path = 'input.mp3'
    with open(new_file_path, 'wb') as new_file:
        content = audio_file.read()
        new_file.write(content)
    with open("/Users/mihiragarwal/Desktop/Project Courses/Embedded Project/input.mp3", "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
                        model="whisper-1", 
                        file=audio_file, 
                        response_format="text"
                        )
    
    print("First prompt")
    print(transcription)
    
    chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[{"role": "user", "content": f"You are a advanced chatbot for kids which tries to give fun but informative reponse to kids. Answer in english only"},
              {"role": "assistant", "content": f"Query: {transcription}" }]
    )
    text = chat_completion.choices[0].message.content
    language = 'en'
    myobj = gTTS(text=text, lang=language, slow=False) 
    myobj.save("output.mp3")
    await cl.Message(
        content=f"{chat_completion.choices[0].message.content}",
    ).send()