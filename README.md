# InfoChartQA: A Benchmark for Multimodal Question Answering on Infographic Charts


🤗[Dataset](https://huggingface.co/datasets/Jietson/InfoChartQA) | 🖥️[Code](https://github.com/CoolDawnAnt/InfoChartQA) | 📄[Paper](https://arxiv.org/abs/2505.19028)

![xbhs3](teaser.jpg)

## About
**InfoChartQA** is a benchmark for evaluating multimodal large language models (MLLMs) on infographic charts enriched with pictorial visual elements like pictograms and icons. It features **5,948 pairs of infographic and plain charts** that share the same underlying data but differ in visual style, enabling controlled comparisons. The dataset contains a total of **58,857 questions**, including **50,920** text-based and **7,937** visual-element-based questions designed to probe model understanding of both content and complex visual design. Our analysis of 20 MLLMs reveals significant performance drops on infographic charts, highlighting key challenges and new research directions.

## 🤗 Dataset 
You can find our dataset on huggingface: [InfoChartQA Dataset](https://huggingface.co/datasets/Jietson/InfoChartQA)

## Evaluation 

### Evaluation Results
<p align="center">
  <img src="result.png" alt="xbhs3" width="70%">
</p>

### Usage
Each question entry is arranged as follows. **Note that for visual questions, there may be some extra input figures, which are cropped from the orginal figure. We present their bboxes in "extra_input_figure_bboxes".**
```
{
        "question_id": id of the question,
        "question_type_name": question type name, for example: "extreme" questions, 
        "question_type_id": question type id, this is only used for evaluation! For example: 72 means "extreme" questions,
        "figure_id": id of the figure,
        "question": question text,  
        "answer": ground truth answer,
        "instructions": instructions,
        "url": url of the input image,
        "extra_input_figure_ids": ids of the extra input figures,
        "extra_input_figure_bboxes": bbox of the extra input figures, in [x,y,w,h] format w/o normalization.
        "difficulty": difficulty level,
        "chart_type": chart_type,
}
```

Each question is built by:

```
input_image: item["url"] (may need to download for models that don't support url input)
extra_input_image: Cropped input_image using item["extra_input_figure_bboxes"],
input_text: item["question"] + item["instructions"] (if any)
```

where ``item`` is an entry of the dataset.


###  Evaluation Instructions


For detailed evaluation instructions and usage, please refer to the [Evaluation](./eval/README.md).




## 📄 Paper

- **[InfoChartQA: A Benchmark for Multimodal Question Answering on Infographic Charts](https://arxiv.org/abs/2505.19028)**  
*Tianchi Xie*, _Minzhi Lin,  Mengchen Liu, Yilin Ye, Changjian Chen, Shixia Liu_  

## 📚 Citation

If you use our work and are inspired by our work, please cite:

```
@misc{lin2025infochartqa,
      title={InfoChartQA: A Benchmark for Multimodal Question Answering on Infographic Charts}, 
      author={Tianchi Xie and Minzhi Lin and Mengchen Liu and Yilin Ye and Changjian Chen and Shixia Liu},
      year={2025},
      eprint={2505.19028},
      url={https://arxiv.org/abs/2505.19028}, 
}
```

## 🪪 License

Our original data contributions (all data except the charts) are distributed under the [CC BY-SA 4.0](https://github.com/CoolDawnAnt/InfoChartQA?tab=Apache-2.0-1-ov-file) license. The copyright of the charts belong to the original authors.

## ✨ Related Projects

- **OrionBench: A Benchmark for Chart and Human-Recognizable Object Detection in Infographics**  
  [Paper](https://arxiv.org/abs/2505.17473) | [Code](https://github.com/OrionBench/OrionBench/) | [Dataset](https://huggingface.co/datasets/OrionBench/OrionBench)


- **ChartGalaxy: A Dataset for Infographic Chart Understanding and Generation**  
  [paper](https://arxiv.org/abs/2505.18668) | [Code](https://github.com/ChartGalaxy/ChartGalaxy/) | [Dataset](https://huggingface.co/datasets/ChartGalaxy/ChartGalaxy)

## 💬 Contact

If you have any questions about this work, please contact us using the following email address: **[linmz21@mails.tsinghua.edu.cn](linmz21@mails.tsinghua.edu.cn)**. 
