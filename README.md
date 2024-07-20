# AI Chatbot for Kids with LLM

## Project Overview
This project involves the development of an AI chatbot designed for kids, utilizing a client-server architecture. The system integrates an STM board and UART communication for audio recording, implements speech-to-text conversion, and uses WiFi modules to transmit queries to a server. The server hosts a fine-tuned Language Learning Model (LLM) which processes the queries and sends back responses, which are then converted to synthesized audio.

## Mentor
Prof. Jhuma Saha

## Project Duration
March-April 2024

## Features
- **Client-Server Architecture**: Efficient communication between client and server for real-time interactions.
- **STM Board Integration**: Utilizes STM microcontroller for audio recording.
- **UART Communication**: Ensures reliable data transmission between components.
- **Speech-to-Text Conversion**: Converts recorded audio into text using state-of-the-art algorithms.
- **WiFi Modules**: Enables wireless transmission of queries to the server.
- **Fine-Tuned LLM**: Processes queries and generates appropriate responses.
- **Text-to-Speech Conversion**: Converts text responses back to synthesized audio.

## Components
1. **STM Board**: Microcontroller board for handling audio recording.
2. **UART Communication**: Used for data transfer between STM board and other modules.
3. **WiFi Module**: ESP8266 or similar module for wireless communication.
4. **Server**: Hosts the fine-tuned Language Learning Model (LLM).
5. **LLM**: Fine-tuned for processing and generating responses to queries.
6. **Audio Processing**: Modules for speech-to-text and text-to-speech conversion.

## System Architecture
1. **Audio Recording**: The STM board records the user's speech via a microphone.
2. **Data Transmission**: The recorded audio data is transmitted to a processing unit using UART communication.
3. **Speech-to-Text**: The audio data is converted into text using speech-to-text algorithms.
4. **WiFi Transmission**: The text query is sent to the server over WiFi.
5. **Query Processing**: The server, equipped with a fine-tuned LLM, processes the text query.
6. **Response Generation**: The LLM generates a suitable response to the query.
7. **Text-to-Speech**: The response text is converted back into synthesized audio.
8. **Audio Playback**: The audio response is played back to the user.

## Installation and Setup

### Hardware Requirements
- STM Board (e.g., STM32)
- UART Interface
- WiFi Module (e.g., ESP8266)
- Microphone and Speaker
- Power Supply

### Software Requirements
- Python 3.x
- Speech-to-Text Conversion Library (e.g., Google Speech Recognition API)
- Text-to-Speech Conversion Library (e.g., gTTS)
- Server with a fine-tuned LLM (e.g., Flask, FastAPI)
- Firmware for STM board (e.g., STM32CubeIDE)

### Setup Instructions
1. **Hardware Setup**:
   - Connect the microphone to the STM board for audio input.
   - Set up UART communication between the STM board and the processing unit.
   - Connect the WiFi module to the STM board.
   - Connect the speaker for audio output.

2. **Software Setup**:
   - Install required Python libraries:
     ```sh
     pip install Flask fastapi google-speech google-text-to-speech
     ```
   - Set up the server with the fine-tuned LLM.
   - Deploy the speech-to-text and text-to-speech conversion services.

3. **Firmware Deployment**:
   - Write and deploy firmware for the STM board to handle audio recording and UART communication using STM32CubeIDE.
   - Ensure the STM board can communicate with the WiFi module for transmitting data.

## Usage
1. **Start the Server**:
   ```sh
   python server.py
2. **Power On the STM Board**:
  - Ensure all connections are secure and power on the STM board.
3. **Interact with the Chatbot**:
  - Speak into the microphone. The STM board will enable recording of your query which will be processed as text and transmitted to the server via wifi module.
  - The server will process the query and send back a text response, which will be processed as audio and played back through the speaker.
    
## Example Interaction
**User**: "What is the weather like today?"
**Chatbot**: "Hey there! Today is a bright and sunny day, perfect for playing outside! The temperature will be around 25 degrees Celsius, so don't forget to wear your sunscreen and stay hydrated!"

   
