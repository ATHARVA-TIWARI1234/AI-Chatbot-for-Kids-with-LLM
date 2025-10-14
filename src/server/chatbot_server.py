"""
Chatbot Server Module
Handles WiFi communication with ESP8266 and LLM query processing.
"""
import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ChatbotServer:
    """Server for processing chatbot queries with LLM."""
    
    def __init__(self):
        """Initialize chatbot server with configuration."""
        self.wifi_url = os.getenv('WIFI_URL', 'http://192.168.11.2/')
        
        # OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)
        
        self.system_prompt = (
            "You are an advanced chatbot for kids which tries to give fun but "
            "informative responses to kids. Answer in English only."
        )
    
    def fetch_query_from_wifi(self, max_attempts=1):
        """Fetch query data from WiFi module (ESP8266)."""
        received_values = []
        prev_data = ""
        attempts = max_attempts
        
        while attempts > 0:
            try:
                response = requests.get(self.wifi_url)
                if response.status_code == 200:
                    data = response.content.decode('utf-8', 'ignore').strip()
                    print("Data retrieved successfully:", repr(data))
                    received_values.append(data)
                    
                    if data != prev_data:
                        attempts -= 1
                    prev_data = data
                else:
                    print(f"Failed to retrieve data. Status code: {response.status_code}")
            except requests.RequestException as e:
                print(f"Error fetching data: {e}")
                break
        
        return ','.join(received_values)
    
    def decode_ascii_query(self, ascii_string):
        """Convert ASCII values to text query."""
        ascii_values = ascii_string.split(",")
        text = "".join(chr(int(value.strip())) for value in ascii_values if value.strip())
        print(f"Decoded query: {text}")
        return text
    
    def generate_response(self, query):
        """Generate response using OpenAI LLM."""
        chat_completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "user", "content": self.system_prompt},
                {"role": "assistant", "content": f"Query: {query}"}
            ]
        )
        response = chat_completion.choices[0].message.content
        print(f"Generated response: {response}")
        return response
    
    def process_query(self):
        """Main processing pipeline: fetch, decode, generate response."""
        # Fetch ASCII-encoded query from WiFi
        ascii_data = self.fetch_query_from_wifi()
        
        # Decode query
        query = self.decode_ascii_query(ascii_data)
        
        # Generate response
        response = self.generate_response(query)
        
        # Add padding for transmission
        padded_response = response + "." * 300
        
        return response, padded_response
    
    def save_response(self, response, filename='chatbot_response.txt'):
        """Save response to file for transmission."""
        with open(filename, 'w') as f:
            f.write(response)
        print(f"Response saved to {filename}")
    
    def run(self):
        """Main execution loop."""
        print("Chatbot server started...")
        response, padded_response = self.process_query()
        self.save_response(padded_response)
        return response


if __name__ == "__main__":
    server = ChatbotServer()
    server.run()
