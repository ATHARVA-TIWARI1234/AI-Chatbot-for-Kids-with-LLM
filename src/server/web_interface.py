"""
Web Interface Module
Provides a Chainlit-based web interface for the chatbot.
"""
import os
import chainlit as cl
from openai import OpenAI
from gtts import gTTS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")
client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = (
    "You are an advanced chatbot for kids which tries to give fun but "
    "informative responses to kids. Answer in English only."
)


@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages with audio files."""
    
    # Extract audio file from message
    audio_elements = [file for file in message.elements if file]
    
    if not audio_elements:
        await cl.Message(content="Please upload an audio file.").send()
        return
    
    # Save uploaded audio file
    audio_file_path = audio_elements[0].path
    print(f"Received audio file: {audio_file_path}")
    
    # Copy to local path for processing
    local_audio_path = 'input.mp3'
    with open(audio_file_path, 'rb') as source:
        with open(local_audio_path, 'wb') as dest:
            dest.write(source.read())
    
    # Transcribe audio using Whisper
    with open(local_audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
    
    print(f"Transcription: {transcription}")
    
    # Generate response using GPT
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "user", "content": SYSTEM_PROMPT},
            {"role": "assistant", "content": f"Query: {transcription}"}
        ]
    )
    
    response_text = chat_completion.choices[0].message.content
    print(f"Response: {response_text}")
    
    # Convert response to speech
    language = 'en'
    tts = gTTS(text=response_text, lang=language, slow=False)
    tts.save("output.mp3")
    
    # Send response
    await cl.Message(content=response_text).send()


if __name__ == "__main__":
    # Run with: chainlit run src/server/web_interface.py
    pass
