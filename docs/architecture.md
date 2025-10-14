# System Architecture

## Overview
The AI Chatbot for Kids uses a client-server architecture with embedded hardware components for audio capture and wireless communication.

## Architecture Diagram

```
┌─────────────────┐
│   Microphone    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   STM Board     │ ◄─── Audio Recording
│   (STM32)       │
└────────┬────────┘
         │ UART
         ▼
┌─────────────────┐
│  Processing     │ ◄─── Speech-to-Text (Whisper)
│     Unit        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  WiFi Module    │ ◄─── ESP8266
│  (ESP8266)      │
└────────┬────────┘
         │ WiFi
         ▼
┌─────────────────┐
│  Server/Cloud   │ ◄─── LLM Processing (GPT-3.5)
│                 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Response      │ ◄─── Text-to-Speech (gTTS)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Speaker      │ ◄─── Audio Playback
└─────────────────┘
```

## Components

### Client Side (Embedded)
1. **STM Board (STM32)**
   - Handles audio recording from microphone
   - Communicates via UART with processing unit
   - Triggers recording on command

2. **WiFi Module (ESP8266)**
   - Provides wireless connectivity
   - Transmits queries to server
   - Receives responses from server

### Server Side
1. **Speech-to-Text (Whisper)**
   - Converts audio to text
   - Uses OpenAI's Whisper model

2. **LLM Processing (GPT-3.5)**
   - Processes queries
   - Generates kid-friendly responses
   - Fine-tuned for educational content

3. **Text-to-Speech (gTTS)**
   - Converts text responses to audio
   - Plays back to user

## Data Flow

1. **Audio Capture**: User speaks into microphone connected to STM board
2. **UART Transfer**: Audio data transferred via UART to processing unit
3. **Speech-to-Text**: Audio converted to text using Whisper
4. **WiFi Transmission**: Text query sent to server via ESP8266
5. **LLM Processing**: Server processes query with GPT-3.5
6. **Response Generation**: LLM generates appropriate response
7. **Text-to-Speech**: Response converted to audio
8. **Audio Playback**: Audio response sent back and played through speaker

## Communication Protocols

### UART Protocol
- **Baud Rate**: 115200
- **Data Format**: 8-bit
- **Trigger**: "Send" command initiates transmission

### WiFi Protocol
- **Method**: HTTP GET/POST
- **Encoding**: ASCII values for text transmission
- **Format**: Comma-separated values

## Security Considerations

1. **API Keys**: Stored in environment variables, never in code
2. **WiFi Credentials**: Stored in separate config file (not committed)
3. **Data Privacy**: Audio data processed locally before transmission

## Scalability

The architecture supports:
- Multiple concurrent users (server side)
- Different LLM models (configurable)
- Additional audio processing features
- Extended hardware configurations
