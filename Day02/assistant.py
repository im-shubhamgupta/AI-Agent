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

print("=" * 40)
print(" My AI Assistant")
print("=" * 40)


meassages = []

while True:
    #Get user input
    user_input = input("You: ")

    #Check if the user wants to exit the chat
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Exiting the chat. Goodbye! Have a great day")
        break


    meassages.append(
        {
            "role": "user",
            "content": user_input
        },
    )

    #send a question to the AI model
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=meassages
    )

    ai_reply = response.choices[0].message.content
    print("\n: ", ai_reply)
    #Save AI Reply:--
    meassages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )
    #debugging
    print("\n-------------------Debugging Conversation History-------------------")
    for message in meassages:
        # print(message["role"].title(), ":", message["content"])
        # print(message)
        print(f"{message['role'].title()}: {message['content']}")

    print("-----------------------------------------------------------")
    

