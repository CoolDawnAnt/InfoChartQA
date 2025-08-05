from datasets import load_dataset
import json
from checker import evaluate
from tqdm import tqdm
ds = load_dataset("Jietson/InfoChartQA", split="info")


Responses = {}

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



for query in tqdm(ds):
    query_idx = query["question_id"]
    question_text = build_question(query)
    chart_figure = [query["visual_figure_path"]] # This should be a list of PIL Image Object
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



evaluate("./model_response.json", "./path_to_save_the_result.json")