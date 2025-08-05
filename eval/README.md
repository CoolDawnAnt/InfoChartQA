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
This will download the text-based questions for infochart (the `info` split) from HuggingFace (it takes ~10min for download at 10 MB/s) and evaluate the model on these questions.

## The evaluation process explanation [example.py](https://github.com/CoolDawnAnt/InfoChartQA/blob/main/eval/example.py)

### Prepare the dataset
<!-- Take `info` (text-based questions for infochart) split as example. Use 'datasets' to download our dataset. (Takes ~10min for download at 10 MB/s) -->
These codes will automatically download the questions from HuggingFace. The splits include: `info`: text-based questions for infochart, `plain`: text-based questions for plainchart, `visual_basic`: visual basic questions, `visual_metaphor`: visual metaphor questions.
```python
from datasets import load_dataset
ds = load_dataset("Jietson/InfoChartQA", split="info")
```


### Preprare the model

This part preprares your model that takes ```generate(text, images)``` as an interface to generate answers. You can specify your own BASE_URL and API_KEY.

```python

from openai import OpenAI
import base64
from io import BytesIO
YOUR_API_KEY = YOUR_API_KEY_HERE

class GPT4o(object):
    def __init__(self):
        self.client = OpenAI(
            api_key= YOUR_API_KEY,
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

    def ask(self, context = None, images = None, model="gpt-4o"):
        content = [{"type": "text","text": context}]
        if images is not None:
            for image in images:
                print(image)
                base64_image = self.encode_image(image)
                content.append({ "type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}, },)
        number_of_trials = 0
        while number_of_trials < 5:
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content":content
                        }
                    ]
                )
                return response.choices[0].message.content
            except Exception as e:
                print(e)
                number_of_trials += 1

        return 'Error!'
    
    def generate(self, text, images):
        return self.ask(text , images, "gpt-4o")

model = GPT4o()

```

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

Responses = {}

for query in tqdm(ds):
    query_idx = query["question_id"]
    question_text = build_question(query)
    chart_figure = [query["figure_path"]] # This should be a list of PIL Image Object
    visual_figure = query.get("visual_figure_path",[])

    # Replace with your model
    response = model.generate(question_text, chart_figure + visual_figure)


    Responses[query_idx] = {
        "qtype": int(query["qtype"]),
        "answer": query["answer"],
        "question_id": query_idx,
        "response": response,
    }

with open("./model_response.json", "w", encoding="utf-8") as f:
    json.dump(Responses, f, indent = 2, ensure_ascii=False)
```

### Evaluation
In the end, the accuracy is calculated.

```python
from checker import evaluate
evaluate("./model_response.json", "./path_to_save_the_result.json")
```
