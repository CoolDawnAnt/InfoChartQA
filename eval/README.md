# Evaluation Instructions

<!-- This document provides step-by-step instructions to evaluate your model on **InfoChartQA**.

### ⚙️ Note: You can also refer to ''example.py'' on how to evaluate your model. -->

## Run the evaluation
This section provides step-by-step instruction to evaluate an OpenAI model on the text-based questions.

### Step 1: Specify the API_KEY
Specify your OpenAI API_KEY in the [15](https://github.com/CoolDawnAnt/InfoChartQA/blob/main/eval/example.py#L15) line of the [example.py](https://github.com/CoolDawnAnt/InfoChartQA/blob/main/eval/example.py).

### Step 2: Run the evaluation
```sh
$ python example.py
```
This will download the text-based questions for infochart (the `text` split) from HuggingFace (it takes ~1min for download at 10 MB/s) and evaluate the model on these questions.

## The evaluation process explanation [example.py](https://github.com/CoolDawnAnt/InfoChartQA/blob/main/eval/example.py)

### Prepare the dataset
<!-- Take `info` (text-based questions for infochart) split as example. Use 'datasets' to download our dataset. (Takes ~1min for download at 10 MB/s) -->
These codes will automatically download the questions from HuggingFace. The splits include: `text`: text-based questions, `visual_basic`: visual basic questions, `visual_metaphor`: visual metaphor questions.
```python
from datasets import load_dataset
ds = load_dataset("Jietson/InfoChartQA", split="text")
```


### Preprare the model

This part preprares your model that takes ```generate(text, images)``` as an interface to generate answers. You can specify your own ```BASE_URL``` and ```API_KEY```.

```python

from openai import OpenAI
import base64
from io import BytesIO

YOUR_API_KEY = YOU_API_KEY_HERE


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

```

You can also prepare your custom model class that can support ``generate(query, image_path)`` as interface api. An example model class is in ``models/qwen_2_5_vl.py``

### Run the model and save model's response.

<!-- For each entry in the dataset, you should instruct the full input question as followings (in function *build_questions*).  -->
This part evaluates the model and save the model's response in a local file (model_response.json).

```python
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

```

### Evaluation
In the end, the accuracy is calculated.

```python
from checker import evaluate
evaluate("./model_response.json", "./path_to_save_the_result.json")
```
