---
dataset_info:
  features:
  - name: question_id
    dtype: string
  - name: qtype
    dtype: string
  - name: figure_path
    dtype: image
  - name: visual_figure_path
    list: image
  - name: question
    dtype: string
  - name: answer
    dtype: string
  - name: instructions
    dtype: string
  - name: prompt
    dtype: string
  - name: options
    list: string
  splits:
  - name: info
    num_bytes: 9389294399.0
    num_examples: 55091
  - name: plain
    num_bytes: 15950918129.0
    num_examples: 55091
  - name: visual_metaphor
    num_bytes: 144053150.0
    num_examples: 450
  - name: visual_basic
    num_bytes: 1254942699.466
    num_examples: 7297
  download_size: 20376840742
  dataset_size: 26739208377.466
configs:
- config_name: default
  data_files:
  - split: info
    path: data/info-*
  - split: plain
    path: data/plain-*
  - split: visual_metaphor
    path: data/visual_metaphor-*
  - split: visual_basic
    path: data/visual_basic-*

---



# InfoChartQA:  Benchmark for Multimodal Question Answering on Infographic Charts

🤗[Dataset](https://huggingface.co/datasets/Jietson/InfoChartQA)

# Dataset 
You can find our dataset on huggingface: 🤗[InfoChartQA Dataset](https://huggingface.co/datasets/Jietson/InfoChartQA)

# Usage

Each question entry is arranged as:

```
--question_id: int
--qtype: int
--figure_path: image
--visual_figure_path: list of image
--question: str
--answer: str
--instructions: str
--prompt: str
--options: list of dict ("A/B/C/D":"option_content")
```

Each question is built as:

```
image_input: figure_path, visual_figure_path_1...visual_figure_path_n (if any)
text_iunput: prompt (if any) + question + options (if any) + instructions (if any)
```

# Evaluate

You should store and evaluate model's response as:

```python
# Example code for evaluate
def build_question(query):#to build the question
    question = ""
    if "prompt" in query:
    	question = question + f"{query["prompt"]}\n"
    question = question + f"{query["question"]}\n"
    if "options" in query:
        for _ in query["options"]:
        	question = question + f"{_} {query['options'][_]}\n"
	if "instructions" in query:
    	question = question + query["instructions"]
    return question

with open("visual_basic.json","r",encode="utf-8") as f:
	queries = json.load(f)

for idx in range(queries):
    question = build_question(queries[idx])
    figure_path = [queries[idx]['figure_path']]
    visual_figure_path = queries[idx]['visual_figure_path']
    
	response = model.generate(question, [figure_path, visual_figure_path])# generate model's response based on 
    
    queries[idx]["response"] = reponse

with open("model_reponse.json","w",encode="utf-8") as f:
	json.dump(queries, f)
from checker import evaluate
evaluate("model_reponse.json", "path_to_save_the_result")
```



 
