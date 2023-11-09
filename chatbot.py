import openai
from prompt import setup_prompt
from api_keys import gpt_api_key
import utils

openai.api_key = gpt_api_key 
messages = []

# system_msg = input("What type of chatbot would you like to create?\n")
messages.append({"role": "system", "content": setup_prompt})
messages.append({"role": "user", "content": "hi, I want to build a 3d model"})

response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages, temperature = 1.2)
reply = response["choices"][0]["message"]["content"]
messages.append({"role": "assistant", "content": reply})
print("\n" + reply + "\n")

final_prompt = ""

# print("Your 3d builder  assistant is ready!")
while input != "quit()":
    message = input()
    messages.append({"role": "user", "content": message})
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages, temperature = 1.2)
    reply = response["choices"][0]["message"]["content"]

    messages.append({"role": "assistant", "content": reply})
    print("\n" + reply + "\n")
    if reply[len(reply)-1] == '1' or reply[len(reply)-2] == '1':
        print("start generating")
        final_prompt = reply
        break


# extracted_text = utils.extract_text_surrounded_by_backticks(final_prompt)
# begin = final_prompt.find("{")
# end = final_prompt.find("}")
# print(final_prompt[begin:end+1])
# payload = utils.text_to_3d_gen(final_prompt[begin:end+1])
# taskid = utils.create_meshy_object(payload)
# utils.download_model(taskid)