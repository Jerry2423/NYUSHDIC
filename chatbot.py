import openai
from prompt import setup_prompt

openai.api_key = ""
messages = []
# system_msg = input("What type of chatbot would you like to create?\n")
messages.append({"role": "system", "content": setup_prompt})
messages.append({"role": "user", "content": "hi, I want to build a 3d model"})

response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages, temperature = 1.2)
reply = response["choices"][0]["message"]["content"]
messages.append({"role": "assistant", "content": reply})
print("\n" + reply + "\n")

# print("Your 3d builder  assistant is ready!")
while input != "quit()":
    message = input()
    messages.append({"role": "user", "content": message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages, temperature = 1.2)
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    print("\n" + reply + "\n")