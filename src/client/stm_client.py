"""
STM Client Module
Handles audio recording via STM board, UART communication, and speech-to-text conversion.
"""
import os
import pyaudio
import wave
from openai import OpenAI
import serial
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class STMClient:
    """Client for STM board communication and audio processing."""
    
    def __init__(self):
        """Initialize STM client with configuration from environment variables."""
        self.serial_port = os.getenv('SERIAL_PORT', 'COM9')
        self.baud_rate = int(os.getenv('BAUD_RATE', '115200'))
        self.bytesize = 8
        
        # OpenAI client for speech-to-text
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)
        
        # Audio settings
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = int(os.getenv('SAMPLE_RATE', '44100'))
        self.chunk = 2048
        self.record_seconds = int(os.getenv('RECORD_SECONDS', '10'))
    
    def wait_for_trigger(self, serial_obj):
        """Wait for 'Send' trigger from STM board."""
        print("Waiting for trigger from STM board...")
        while True:
            line_bytes = serial_obj.readline()
            message = line_bytes.decode(errors='ignore').strip()
            if message == "Send":
                print("Received 'Send' trigger. Starting audio recording...")
                return True
    
    def record_audio(self, output_filename='recorded_audio.wav'):
        """Record audio from microphone."""
        audio = pyaudio.PyAudio()
        
        stream = audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        
        print("Recording...")
        frames = []
        sampled_values = []
        
        for i in range(0, int(self.rate / self.chunk * self.record_seconds)):
            data = stream.read(self.chunk)
            frames.append(data)
            # Convert binary data to integer samples
            int_samples = [
                int.from_bytes(data[j:j+2], byteorder='little', signed=True) 
                for j in range(0, len(data), 2)
            ]
            # Normalize samples to range [0, 255]
            normalized_samples = [(sample + 32768) // 256 for sample in int_samples]
            sampled_values.extend(normalized_samples)
        
        print("Finished recording.")
        
        # Stop and close stream
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # Save audio to WAV file
        with wave.open(output_filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))
        
        print(f"Audio saved as {output_filename}")
        return output_filename, sampled_values
    
    def transcribe_audio(self, audio_file_path):
        """Convert audio to text using OpenAI Whisper."""
        with open(audio_file_path, 'rb') as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        print(f"Transcription: {transcription}")
        return transcription
    
    def send_to_uart(self, serial_obj, text):
        """Send transcription text via UART."""
        try:
            # Add padding for transmission
            padded_text = text + "." * 100
            serial_obj.write(padded_text.encode())
            print(f"Sent to UART: {text}")
        except serial.SerialException as e:
            print(f"Error writing to serial port: {e}")
    
    def run(self):
        """Main execution loop."""
        with serial.Serial(
            self.serial_port, 
            baudrate=self.baud_rate, 
            bytesize=self.bytesize
        ) as serial_obj:
            print(f"Serial port {self.serial_port} opened successfully.")
            
            # Wait for trigger
            self.wait_for_trigger(serial_obj)
            
            # Record audio
            audio_file, _ = self.record_audio()
            
            # Transcribe audio
            transcription = self.transcribe_audio(audio_file)
            
            # Send transcription via UART
            self.send_to_uart(serial_obj, transcription)


if __name__ == "__main__":
    client = STMClient()
    client.run()
