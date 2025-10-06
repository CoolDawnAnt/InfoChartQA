from datasets import load_dataset
import json
from tqdm import tqdm

#####  download the dataset

ds = load_dataset("Jietson/InfoChartQA", split="text")

#### Prepare your model here

from openai import OpenAI
import base64
from io import BytesIO

YOUR_API_KEY = YOUR_API_KEY_HERE


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
    chart_figure = query["url"]  # This should be a list of url

    # Replace with your model
    response = model.generate(question_text, chart_figure)

    Responses[query_idx] = {
        "qtype": int(query["qtype"]),
        "answer": query["answer"],
        "question_id": query_idx,
        "response": response,
    }
    # break

with open("./model_response.json", "w", encoding="utf-8") as f:
    json.dump(Responses, f, indent=2, ensure_ascii=False)

#### Evaluate your answer
from checker import evaluate

evaluate("./model_response.json", "./path_to_save_the_result.json")