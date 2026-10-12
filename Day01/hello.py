from openai import OpenAI     # pyAI model
from dotenv import load_dotenv
import os

#Load configuration from the .env file
load_dotenv()

#create a client that communicate with ollama
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
    )


print(os.getenv("MODEL"))

#send a question to the AI model
response = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[
        {
            "role": "user",
            "content": "What is MMachine Learning?"
        }
    ]
)
#Display the response from the AI model
print(response.choices[0].message.content)