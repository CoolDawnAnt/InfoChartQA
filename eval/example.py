from datasets import load_dataset
import json
from tqdm import tqdm

#####  download the dataset

ds = load_dataset("Jietson/InfoChartQA", split="text")

#### Prepare your model here

from openai import OpenAI
import base64
from io import BytesIO
from models.qwen_2_5_vl import Qwen2_5_VL
# YOUR_API_KEY = YOUR_API_KEY_HERE


class GPT4o(object):
    def __init__(self):
        self.client = OpenAI(
            api_key=YOUR_API_KEY,
            base_url="https://api.openai.com/v1"
        )

    def encode_image(self, image, format='PNG'):
        buffer = BytesIO()
        if format.upper() == 'JPEG':
            image.save(buffer, format=format, quality=95)
        else:
            image.save(buffer, format=format)
        image_data = buffer.getvalue()
        buffer.close()
        base64_str = base64.b64encode(image_data).decode('utf-8')

        return base64_str

    def ask(self, context=None, image_urls=None, model="gpt-4o"):
        content = [{"type": "text", "text": context}]
        if image_urls is not None:
            for image_url in image_urls:
                content.append({"type": "image_url", "image_url": {"url": image_url}, }, )
        number_of_trials = 0
        while number_of_trials < 5:
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": content
                        }
                    ]
                )
                return response.choices[0].message.content
            except Exception as e:
                print(e)
                number_of_trials += 1

        return 'Error!'

    def generate(self, text, images):
        return self.ask(text, images, "gpt-4o")


model = GPT4o()
# or model = Qwen2_5_VL() or YOUR CUSTOM MODEL

#### Format Input

def build_question(query):
    question = ""
    if "prompt" in query:
        question += f"{query['prompt']}\n"
    question += f"{query['question']}\n"
    if "options" in query and len(query["options"]) > 0:
        for option in query["options"]:
            question += f"{option}\n"
    if "instructions" in query:
        question += query["instructions"]
    return question


#### Run your model and save your answer

Responses = {}

for query in tqdm(ds):
    query_idx = query["question_id"]
    question_text = build_question(query)
    figure_path = query["url"]  # This should be a list of url for models that support url input

    """
        Note that for models that do not support url input, you may need to download images first.
        For example, for model like Qwen2.5-VL, you may need to down load the image first and pass the local image path to the model,
        like: figure_path = YOUR_LOCAL_IMAGE_PATH OF query['figure_id']
    """

    # Replace with your model
    response = model.generate(question_text, figure_path)

    Responses[query_idx] = {
        "qtype": int(query["question_type_id"]),
        "answer": query["answer"],
        "question_id": query_idx,
        "response": response,
    }

with open("./model_response.json", "w", encoding="utf-8") as f:
    json.dump(Responses, f, indent=2, ensure_ascii=False)

#### Evaluate your answer
from checker import evaluate

evaluate("./model_response.json", "./path_to_save_the_result.json")