# Evaluation Instructions

This document provides step-by-step instructions to evaluate your model on **InfoChartQA**.

## 📂 Input Format

Each question entry in the JSON file should follow this format:

```json
{
  "question_id": 123,
  "qtype": 1,
  "figure_path": "path/to/main_chart.png",
  "visual_figure_path": ["path/to/element1.png", "path/to/element2.png"],
  "question": "What does the icon represent?",
  "answer": "B",
  "instructions": "Please select the most appropriate answer.",
  "prompt": "You are an expert in understanding infographic charts.",
  "options": {
    "A": "Option 1",
    "B": "Option 2",
    "C": "Option 3",
    "D": "Option 4"
  }
}
```

### Text Input Format to Model

To evaluate, you should construct the question prompt as:

```python
def build_question(query):
    question = ""
    if "prompt" in query:
        question += f"{query['prompt']}\n"
    question += f"{query['question']}\n"
    if "options" in query:
        for k, v in query["options"].items():
            question += f"{k} {v}\n"
    if "instructions" in query:
        question += query["instructions"]
    return question
```

## ⚙️ Evaluation Workflow

1. Load all questions from `visual_basic.json`.
2. Construct the text input using the function above.
3. Provide the input chart images:

   * One main chart (`figure_path`)
   * Optional design elements (`visual_figure_path`)
4. Feed both the text and image(s) into your MLLM for answer generation.
5. Save responses into a new JSON file (e.g., `model_response.json`).

### Example Code

```python
import json

with open("visual_basic.json", "r", encoding="utf-8") as f:
    queries = json.load(f)

for query in queries:
    question = build_question(query)
    figure_path = [query["figure_path"]]
    visual_paths = query.get("visual_figure_path", [])
    
    # Replace with your model's API
    response = model.generate(question, [figure_path] + visual_paths)
    query["response"] = response

with open("model_response.json", "w", encoding="utf-8") as f:
    json.dump(queries, f, indent=2)
```

## ✅ Run Evaluation

Once you have your output file:

```bash
python -c "import checker; checker.evaluate('model_response.json', 'result.json')"
```

Or use in a Python script:

```python
from checker import evaluate
evaluate("model_response.json", "result.json")
```
