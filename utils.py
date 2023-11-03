import re
import json

def extract_text_surrounded_by_backticks(input_string):
    # Define a regular expression pattern to match text within triple backticks
    pattern = r'```(.*?)```'
    
    # Use re.DOTALL to match across multiple lines, including newline characters
    extracted_text = re.findall(pattern, input_string, re.DOTALL)
    
    # If extracted_text is not empty, return the first match; otherwise, return None
    return extracted_text[0] if extracted_text else None

def text_to_3d_gen(extracted_str):
    payload = {"object_prompt":"", "style_prompt":"", "enable_pbr": True, "art_style": "", "negative_prompt":"low quality, low resolution, blurry, ugly"}
    response_dict = json.loads(extracted_str)
    for i in payload.keys:
        if i == "enable_pbr":
            continue
        if i != "negative_prompt":
            payload[i] = response_dict[i]
        else:
            payload[i] += response_dict[i]
    
    return payload

