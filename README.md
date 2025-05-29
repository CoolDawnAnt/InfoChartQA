

# InfoChartQA:  Benchmark for Multimodal Question Answering on Infographic Charts



![xbhs3](C:\Users\Admin\Desktop\teaser.jpg)🤗[Dataset](https://huggingface.co/datasets/Jietson/InfoChartQA)

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
text_input: prompt (if any) + question + options (if any) + instructions (if any)
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

Or simply use after your answer is generated:

```python
python -c "import checker; checker.evaluate(sys.argv[1], sys.argv[2])" PATH_TO_INPUT_FILE PATH_TO_INPUT_FILE 
```

# LeaderBoard

| Model                        | Infographic | Plain   | Δ     | Basic  | Metaphor | Avg.   | 
|------------------------------|-------------|---------|-------|--------|----------|--------| 
| **Baselines**                |             |         |       |        |          |        | 
| Human                        | 95.35\*      | 96.28\*  | 0.93  | 93.17\*| 88.69    | 90.93  | 
| **Proprietary Models**       |             |         |       |        |          |        | 
| OpenAI O4-mini               | 79.41       | 94.61   | 15.20 | 92.12  | 54.76    | 73.44  | | GPT-4.1                      | 70.01       | 83.36   | 13.35 | 88.47  | 50.87    | 69.67  | 
| GPT-4o                       | 66.09       | 81.77   | 15.68 | 81.77  | 47.19    | 64.48  | 
| Claude 3.5 Sonnet            | 65.67       | 83.11   | 17.44 | 90.36  | 55.33    | 72.85  | 
| Gemini 2.5 Pro Preview       | 83.31       | 93.88   | 10.07 | 90.01  | 60.42    | 75.22  | 
| Gemini 2.5 Flash Preview     | 71.91       | 84.66   | 12.75 | 82.02  | 56.28    | 69.15  | 
| **Open-Source Models**       |             |         |       |        |          |        | 
| Qwen2.5-VL-72B               | 62.06       | 78.47   | 16.41 | 77.34  | 54.64    | 65.99  | 
| Llama-4 Scout                | 67.41       | 84.84   | 17.43 | 81.76  | 51.89    | 66.83  | 
| Intern-VL3-78B               | 66.38       | 82.18   | 15.80 | 79.46  | 51.52    | 65.49  | 
| Intern-VL3-8B                | 56.82       | 73.50   | 16.68 | 74.26  | 49.57    | 61.92  | 
| Janus Pro                    | 29.61       | 45.29   | 15.68 | 41.18  | 42.21    | 41.69  | 
| DeepSeek VL2                 | 39.81       | 47.01   | 7.20  | 58.72  | 44.54    | 51.63  | 
| Phi-4                        | 46.20       | 66.97   | 20.77 | 61.87  | 38.31    | 50.09  | 
| LLaVA OneVision Chat 78B     | 47.78       | 63.66   | 15.88 | 62.11  | 50.22    | 56.17  | 
| LLaVA OneVision Chat 7B      | 38.41       | 54.43   | 16.02 | 61.03  | 45.67    | 53.35  | 
| Pixtral                      | 44.70       | 60.88   | 16.11 | 64.23  | 50.87    | 57.55  | 
| Ovis1.6-Gemma2-9B            | 50.56       | 64.52   | 13.98 | 60.96  | 34.42    | 47.69  | 
| ChartGemma                   | 19.99       | 33.81   | 13.82 | 30.52  | 33.77    | 32.15  | 
| TinyChart                    | 26.34       | 44.73   | 18.39 | 14.72  | 9.03     | 11.88  | 
| ChartInstruct-LLama2         | 20.55       | 27.91   | 7.36  | 33.86  | 33.12    | 33.49  |

 # License

Our original data contributions (all data except the charts) are distributed under the [CC BY-SA 4.0](https://github.com/princeton-nlp/CharXiv/blob/main/data/LICENSE) license. Our code is licensed under [Apache 2.0](https://github.com/princeton-nlp/CharXiv/blob/main/LICENSE) license. The copyright of the charts belong to the original authors.

##  Cite

If you use our work and are inspired by our work, please consider cite us (available soon):

```
@misc{lin2025infochartqabenchmarkmultimodalquestion,
      title={InfoChartQA: A Benchmark for Multimodal Question Answering on Infographic Charts}, 
      author={Minzhi Lin and Tianchi Xie and Mengchen Liu and Yilin Ye and Changjian Chen and Shixia Liu},
      year={2025},
      eprint={2505.19028},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2505.19028}, 
}
```

