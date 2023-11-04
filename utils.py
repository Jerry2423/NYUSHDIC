import re
import os
import requests
import json
from api_keys import meshy_api_key

def extract_text_surrounded_by_backticks(input_string):
    # Define a regular expression pattern to match text within triple backticks
    pattern = r'```(.*?)```'
    
    # Use re.DOTALL to match across multiple lines, including newline characters
    extracted_text = re.findall(pattern, input_string, re.DOTALL)
    
    # If extracted_text is not empty, return the first match; otherwise, return None
    return extracted_text[0] if extracted_text else None

def text_to_3d_gen(extracted_str):
    payload = {"object_prompt":"", "style_prompt":"", "enable_pbr": True, "art_style": "", "negative_prompt":"low quality, low resolution, blurry, ugly, "}
    response_dict = json.loads(extracted_str)
    for i in payload.keys():
        if i == "enable_pbr":
            continue
        if i != "negative_prompt":
            payload[i] = response_dict[i]
        else:
            payload[i] += response_dict[i]
    
    return payload


def create_meshy_object(payload, target="3d"):
    headers = {
        "Authorization": f"Bearer {meshy_api_key}"
    }

    response = requests.post(
        f"https://api.meshy.ai/v1/text-to-{target}",
        headers=headers,
        json=payload,
    )
    response.raise_for_status()

    meshy_response = response.json()
    return meshy_response["result"]



def download_model(task_id, target="3d"):
    headers = {
        "Authorization": f"Bearer {meshy_api_key}"
    }

    response = requests.get(
        f"https://api.meshy.ai/v1/text-to-{target}/{task_id}",
        headers=headers,
    )
    response.raise_for_status()

    # Convert the JSON response to a Python dictionary
    retrieve_response = json.loads(response.text)

    print(retrieve_response["progress"])
    # Extract the "model_url"
    if retrieve_response["progress"] == 100:
        model_url = retrieve_response["model_url"]

        # Get the directory of the script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Define the file name
        file_name = "model.glb"

        # Define the complete file path
        file_path = os.path.join(script_dir, file_name)

        # Check if the file already exists
        if not os.path.isfile(file_path):
            # Download the file
            response = requests.get(model_url)

            if response.status_code == 200:
                with open(file_path, "wb") as file:
                    file.write(response.content)
                print(f"File downloaded successfully to {file_path}.")
            else:
                print(f"File download failed with status code {response.status_code}.")
                if "error" in response.text:
                    error_message = json.loads(response.text)["error"]
                    print(f"Error message: {error_message}")
        else:
            print(f"File '{file_path}' already exists. Skipping download.")

    else:
        print("the model is still in progress...")

    #