from tools import get_current_time,roll_dice,generate_password

def execute_tool(user_input):

    if "dice" in user_input.lower():
        return f"You rolled a {roll_dice()}"
        print("\nAI: ",roll_dice())
    elif "time" in user_input.lower():
        # print(get_current_time())
        return get_current_time()

    elif "password" in user_input.lower():
        # print(generate_password())
        return generate_password()

    return None #means Null empty # false