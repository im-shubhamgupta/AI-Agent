from datetime import datetime
import secrets
import random
import string




# print("1.print current time")

# choose = input("choose tools: ")

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")


def roll_dice():
    return random.randint(1,6)


def generate_password(length=12):
    """Generate a secure random password."""

    characters = (
        string.ascii_letters+
        string.digits + 
        string.punctuation
    )

    # password = ""

    # for _ in range(length):
    #     password += secrets.choice(characters)
    return "".join(secrets.choice(characters) for _ in range(length))

def read_text_file(file_path):

    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return "File not found"
    


# print(get_current_time())
# print(roll_dice())
# print(generate_password())