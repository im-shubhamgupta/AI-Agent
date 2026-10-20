from openai import OpenAI     # pyAI model
from dotenv import load_dotenv
import os

#Load configuration from the .env file
load_dotenv('../.env')

#create a client that communicate with ollama
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
    )

print("=" * 40)
print(" My AI Assistant")
print("=" * 40)

roles = { # dictionary
    
        "1": "you are a friendly school teacher. Explain every concept in simple language with real-life examples.",
    
        "2": "you are a senior Python developer. Explain programming concepts clearly  and always include Python code snippets",
        "3": "you are an experienced travel guide. Recommend places, food, transportation and travel tips.",
    
        "4": "you are a motivaional coach. Encourage the user and give practical advice with a positive attitude.",
    
        "5": "you are a professional interviewer. Ask one interview question at a time and provide feedback after each question.",
    }


print("\nplease choose your AI  role")
# for key, value in role.items():
for key, value in roles.items():
    print(f"{key}: {value}")

ai_role = input("Choose role: ")

meassages = [{
            "role": "system",
            # "content": "You are a friendly AI Teacher. Explain every concept in simple language with real-life examples."
            # "content": "You are a Technical expert. Explain every concept in simple language with real-life examples."
            # "content": roles[0][ai_role]
            "content": roles.get(ai_role, "You are helpful AI assistant. Explain every concept in simple language with real-life examples.") # second params is the default value
        }
    ]

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
    #rint("\n-------------------Debugging Conversation History-------------------")
    #or message in meassages:
    #   # print(message["role"].title(), ":", message["content"])
    #   # print(message)
    #   print(f"{message['role'].title()}: {message['content']}")

    #rint("-----------------------------------------------------------")
    

