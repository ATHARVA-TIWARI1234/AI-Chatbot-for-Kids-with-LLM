# AI Chatbot for Kids with LLM

An interactive AI chatbot designed for children, featuring embedded hardware integration with STM board, UART communication, and OpenAI's GPT-3.5 for generating kid-friendly responses.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Hardware Setup](#hardware-setup)
- [Usage](#usage)
- [System Architecture](#system-architecture)
- [Hardware Components](#hardware-components)
- [Example Interaction](#example-interaction)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)

## Project Overview

This project implements an AI chatbot system specifically designed for kids, utilizing a client-server architecture. The system integrates:
- **STM32 microcontroller** for audio recording
- **UART communication** for reliable data transmission
- **WiFi modules (ESP8266)** for wireless connectivity
- **OpenAI's Whisper** for speech-to-text conversion
- **GPT-3.5-turbo** for generating appropriate, educational responses
- **Google Text-to-Speech (gTTS)** for voice synthesis

**Mentor**: Prof. Jhuma Saha  
**Project Duration**: March-April 2024

## Features

- **Real-time Audio Processing**: Records and processes audio from microphone
- **Speech-to-Text**: Converts spoken queries to text using OpenAI Whisper
- **AI-Powered Responses**: Generates kid-friendly, educational responses
- **Wireless Communication**: ESP8266-based WiFi connectivity
- **UART Integration**: Reliable serial communication with STM board
- **Web Interface**: Chainlit-based interactive web UI
- **Secure Configuration**: Environment-based API key management

## Project Structure

```
AI-Chatbot-for-Kids-with-LLM/
├── src/
│   ├── __init__.py
│   ├── client/
│   │   ├── __init__.py
│   │   └── stm_client.py          # STM board client implementation
│   └── server/
│       ├── __init__.py
│       ├── chatbot_server.py      # LLM query processing server
│       └── web_interface.py       # Chainlit web interface
├── config/
│   └── wifi.conf.example          # WiFi configuration template
├── docs/
│   └── architecture.md            # Detailed system architecture
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

## Installation

### Prerequisites

- Python 3.8 or higher
- STM32 board with UART support
- ESP8266 WiFi module
- Microphone and speaker
- OpenAI API key

### Software Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/ATHARVA-TIWARI1234/AI-Chatbot-for-Kids-with-LLM.git
   cd AI-Chatbot-for-Kids-with-LLM
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your configuration:
   ```env
   OPENAI_API_KEY=your_actual_api_key_here
   SERIAL_PORT=COM9  # or /dev/ttyUSB0 on Linux
   BAUD_RATE=115200
   WIFI_URL=http://192.168.11.2/
   RECORD_SECONDS=10
   SAMPLE_RATE=44100
   ```

2. **Configure WiFi (optional)**
   ```bash
   cp config/wifi.conf.example config/wifi.conf
   ```
   Edit `config/wifi.conf` with your WiFi credentials.

## Hardware Setup

### Required Components

- **STM32 Board**: Microcontroller for handling audio recording and UART communication
- **ESP8266 WiFi Module**: For wireless communication with the server
- **Microphone**: Audio input device compatible with STM32
- **Speaker**: Audio output device for playing responses
- **UART Interface**: Serial communication interface (usually built into STM32)
- **Power Supply**: Appropriate power supply for all components (typically 5V/3.3V)
- **Connecting Wires**: For establishing connections between components

### Hardware Connection Instructions

1. **Microphone Connection**
   - Connect the microphone's VCC pin to STM32's 3.3V or 5V (check microphone specifications)
   - Connect the microphone's GND pin to STM32's GND
   - Connect the microphone's output pin to an ADC-enabled pin on the STM32 (e.g., PA0)

2. **UART Setup**
   - Identify UART TX and RX pins on STM32 (e.g., UART1: PA9-TX, PA10-RX)
   - Connect STM32 TX to the processing unit/computer RX
   - Connect STM32 RX to the processing unit/computer TX
   - Ensure common ground between STM32 and processing unit

3. **ESP8266 WiFi Module Connection**
   - Connect ESP8266's VCC to 3.3V power supply (NOT 5V)
   - Connect ESP8266's GND to common ground
   - Connect ESP8266's TX to STM32 RX pin (or designated UART pin)
   - Connect ESP8266's RX to STM32 TX pin through a voltage divider (5V to 3.3V) if needed
   - Connect ESP8266's CH_PD (Chip Enable) pin to 3.3V

4. **Speaker Connection**
   - Connect speaker to a PWM-capable pin on STM32 (e.g., PA8)
   - Use an amplifier circuit if needed for adequate volume
   - Connect speaker's ground to common ground

5. **Power Supply**
   - Ensure STM32 board is powered via USB or external power supply
   - Provide stable 3.3V supply for ESP8266 (use voltage regulator if necessary)
   - Use a common ground for all components

### Hardware Configuration

1. **STM32 Firmware Setup**
   - Flash the STM32 with firmware for audio capture and UART communication
   - Configure UART baud rate to 115200 (as specified in `.env`)
   - Set up ADC for microphone input sampling
   - Configure PWM for speaker output

2. **ESP8266 Configuration**
   - Flash ESP8266 with WiFi communication firmware
   - Configure WiFi credentials using the `config/wifi.conf` file
   - Set up HTTP client/server for data transmission

3. **Testing Hardware**
   - Verify UART communication by checking serial output
   - Test microphone by checking audio input levels
   - Verify WiFi connectivity by pinging the ESP8266
   - Test speaker output with a simple tone

### Safety Considerations

- Always disconnect power before making hardware connections
- Verify voltage levels to avoid damaging components
- Use proper grounding to prevent electrical noise
- Ensure adequate heat dissipation for all components
- Keep the setup away from water and extreme temperatures

## Usage

### Running the STM Client

For embedded hardware with STM board:

```bash
python src/client/stm_client.py
```

This will:
1. Wait for trigger signal from STM board
2. Record audio when triggered
3. Transcribe audio to text
4. Send transcription via UART

### Running the Chatbot Server

For processing queries received via WiFi:

```bash
python src/server/chatbot_server.py
```

This will:
1. Fetch query from WiFi module
2. Process with GPT-3.5
3. Generate kid-friendly response
4. Save response for transmission

### Running the Web Interface

For web-based interaction:

```bash
chainlit run src/server/web_interface.py
```

Then open your browser to `http://localhost:8000` and upload audio files for processing.

## System Architecture

```
Microphone → STM Board → UART → Processing Unit
                                      ↓
                               Speech-to-Text
                                      ↓
                               WiFi Module (ESP8266)
                                      ↓
                              Server (GPT-3.5)
                                      ↓
                               Response Generation
                                      ↓
                               Text-to-Speech
                                      ↓
                                  Speaker
```

For detailed architecture information, see [docs/architecture.md](docs/architecture.md).

## Hardware Components

| Component | Description | Purpose |
|-----------|-------------|---------|
| STM32 Board | Microcontroller | Audio recording and UART communication |
| ESP8266 | WiFi Module | Wireless data transmission |
| Microphone | Audio Input | Captures user speech |
| Speaker | Audio Output | Plays synthesized responses |
| UART Interface | Serial Communication | Data transfer between components |

## Example Interaction

**User**: *"What is the largest animal on Earth?"*

**Chatbot**: *"Hey there! The largest animal on Earth is the blue whale! These magnificent creatures can grow up to 100 feet long and weigh as much as 200 tons - that's like 33 elephants! They live in the ocean and eat tiny creatures called krill. Isn't that amazing?"*

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is part of an academic research project.

## Acknowledgments

- **Mentor**: Prof. Jhuma Saha
- **Institution**: IIT Gandhinagar
- **Duration**: March-April 2024
- **Technologies**: OpenAI (Whisper, GPT-3.5), Python, STM32, ESP8266

## Contact

For questions or collaboration opportunities, please open an issue on GitHub.
