import pyaudio
import wave
from openai import OpenAI
import serial
import time


#code for UART sender
serial_port = 'COM9'
baud_rate = 115200
bytesize = 8


Flag = True
with serial.Serial(serial_port, baudrate=baud_rate, bytesize=bytesize) as SerialObj:
    print(f"Serial port {serial_port} opened successfully.")
    while Flag:
        line_bytes = SerialObj.readline()  # Read bytes from serial port
        tef = line_bytes.decode(errors='ignore').strip()
        if tef == "Send":
            print("Received 'Send' statement. Sending sample values...")
            Flag = False

    client = OpenAI(api_key="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")
    # Settings
    FORMAT = pyaudio.paInt16  # 16-bit PCM format
    CHANNELS = 1  # Mono audio
    RATE = 44100  # Sampling rate (44.1 kHz)
    CHUNK = 2048  # Number of frames per buffer
    RECORD_SECONDS = 10  # Duration of recording

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open stream
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []
    sampled_values = []

    # Record audio
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        # Convert binary data to integer samples
        int_samples = [int.from_bytes(data[j:j+2], byteorder='little', signed=True) for j in range(0, len(data), 2)]
        # Normalize samples to range [0, 255]
        normalized_samples = [(sample + 32768) // 256 for sample in int_samples]
        sampled_values.extend(normalized_samples)

    print("Finished recording.")

    # Stop stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a WAV file
    output_filename_wav = "recorded_audio.wav"
    with wave.open(output_filename_wav, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved as {output_filename_wav}")

    count = 0

    # Save sampled values to a text file
    output_filename_txt = "tati.txt"
    with open(output_filename_txt, 'w') as txt_file:
        for value in sampled_values:
            txt_file.write(f"{value}\n")
            count = count + 1
            
            
    print(f"Count: {count}")

    print(f"Sampled values saved as {output_filename_txt}")
    new_file_path = 'recorded_audio.wav'

    # Ensure there are no non-printable characters in this line
    audio_file = open(new_file_path,'rb')

    transcription = client.audio.transcriptions.create(
                            model="whisper-1", 
                            file=audio_file, 
                            response_format="text"
                            )
    print(transcription)
    
    
    #convert count to character
    
    fuck = chr(len(transcription))
    
    #store transcription in a sampled_values.txt file
    with open("sampled_values.txt", "w") as file:
        file.write(f"{transcription}"+"."*100)
    
    
    with open("sampled_values.txt", "r") as file:
        for line in file:
            try:                                 
                sample_value =  line.strip()
                print(sample_value)
                SerialObj.write(sample_value.encode())             

            except serial.SerialException as e:
                print(f"Error opening or writing to serial port: {e}")
            except FileNotFoundError:
                print("Error: sampled_values.txt file not found.")

