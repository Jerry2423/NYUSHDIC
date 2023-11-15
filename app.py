import time 
import gradio as gr
import openai
from prompt import setup_prompt
from api_keys import gpt_api_key
import utils
import os

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

meshy_prompt = ""

model_path =  "../house_light/model.glb"

cnt = 0


def solve():
  global model_path
  # time.sleep(3)
  extracted_text = utils.extract_text_surrounded_by_backticks(meshy_prompt)
  begin = meshy_prompt.find("{")
  end = meshy_prompt.find("}")
  print(meshy_prompt[begin:end+1])
  payload = utils.text_to_3d_gen(meshy_prompt[begin:end+1])
  taskid = utils.create_meshy_object(payload)
  utils.download_model(taskid)
  return os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{taskid}.glb")

def slow_echo(message, history):
  global cnt
  global messages
  global meshy_prompt
  global model_path
  messages.append({"role": "user", "content": message})
  response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=messages, temperature = 1.2)
  reply = response["choices"][0]["message"]["content"]
  messages.append({"role": "assistant", "content": reply})
  print("\n" + reply + "\n")
  if reply[len(reply)-1] == '1' or reply[len(reply)-2] == '1':
      print("start generating")
      meshy_prompt = reply
      reply = "Generating..."
      # cnt += 1
      # if cnt == 1 :
      #   model_path = "../house_light/model.glb"
      # elif cnt == 2 :
      #   model_path = "../house_dark/model.glb"

  for i in range(len(reply)):
    time.sleep(0.02)
    yield reply[:i+1]

with gr.Blocks() as demo:
  with gr.Row():
    with gr.Column():
      chatbot = gr.ChatInterface(fn = slow_echo, title="SpacialSynergy", examples=["hi, I want to build a 3d model"]).queue()
    with gr.Column():
      interface = gr.Interface(
        fn=solve, 
        title = "3D Model",
        inputs=None, 
        outputs = ["model3d"],
      )

demo.launch(share = False)