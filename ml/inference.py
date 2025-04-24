import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("HF_API_KEY")
if not api_key:
    raise ValueError("HF_API_KEY not found in environment variables. Did you set it in your .env file?")

API_URL = "https://router.huggingface.co/hf-inference/models/google/vit-base-patch16-224"
headers = {
        "Authorization": f"Bearer {api_key}"
        }

def predict(filename, top_k=1):
        with open(filename, "rb") as f:
                data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)
        response.raise_for_status()
        final_dict = response.json()[:top_k][0]
        final_dict["confidence"] = final_dict.pop("score")
        return final_dict

output = predict("form_example.png")
print(output)
