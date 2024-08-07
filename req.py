import requests

url = "http://192.168.11.2/"
num = 1  # Number of requests to make
received_values = []  # List to store received values
prevdata= "" 
while(num>0):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.content.decode('utf-8', 'ignore').strip()
            print("Data retrieved successfully:", repr(data))
            received_values.append(data)
            print(num)
            if(data != prevdata):
                num = num - 1
            prevdata = data
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")

# Write the values in received_values to output.txt
with open("output.txt", "w") as f:
    # Write all received values separated by commas
    f.write(','.join(received_values))


# Open the output.txt file for reading
with open("output.txt", "r") as file:
    # Read the ASCII values from the file
    ascii_values = file.read().split(",")

    # Convert ASCII values to characters and concatenate them into a string
    text = "".join(chr(int(value.strip())) for value in ascii_values)

# Print the resulting text
print("Converted text:", text)

with open("final_test.txt", "w") as file:
    file.write(f"{text}"+"."*300)


import openai
from openai import OpenAI
client = OpenAI(api_key="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")

chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[{"role": "user", "content": f"You are a advanced chatbot for kids which tries to give fun but informative reponse to kids. Answer in english only"},
              {"role": "assistant", "content": f"Query: {text}" }]
    )
output_text = chat_completion.choices[0].message.content

with open("final_outputtxt", "w") as file:
    file.write(f"{output_text}"+"."*300)



# from openai import OpenAI
# import serial
# import time

# serial_port = 'COM14'
# baud_rate = 115200
# bytesize = 8

# with serial.Serial(serial_port, baudrate=baud_rate, bytesize=bytesize) as SerialObj:
#     print(f"Serial port {serial_port} opened successfully.")
    
#     with open("sampled_values.txt", "r") as file:
#                 for line in file:
#                     try:                                 
#                         sample_value =  line.strip()
#                         print(sample_value)
#                         SerialObj.write(sample_value.encode())             

#                     except serial.SerialException as e:
#                         print(f"Error opening or writing to serial port: {e}")
#                     except FileNotFoundError:
#                         print("Error: sampled_values.txt file not found.")