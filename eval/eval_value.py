import json
import re
import os
import shutil
from pathlib import Path
from compare_value import is_number, convert, convert_to_number, clean, is_valid_thousand_separator, only_digits_and_commas
from compare_value import compare_value
file_idx = 0


def compare(data_chart, data_image):
    matching_question = []
    qid = []
    res = []
    path = {}
    path_score = {}
    for question_id, chart_data in data_chart.items():
        if "response" not in chart_data:
            continue
        # 确保对应 question_id 在 data_image 中
        if question_id in data_image:
            image_data = data_image[question_id]
            if "response" not in image_data or "score" not in image_data:
                continue
            qa = {
                "question_id": chart_data["question_id"],
                "qid":chart_data["qid"],
                "figue":data_qa[chart_data["question_id"]]["figure_path"],
                "question":data_qa[chart_data["question_id"]]["question"],
                "answer":chart_data["answer"],
                "response":chart_data["response"]
            }
            if chart_data["score"] == 0:
                matching_question.append(qa)
            # 检查条件
            if chart_data["score"] == 0 and image_data["score"] == 1:
                qid.append(chart_data["qid"])
                
                if data_qa[chart_data["question_id"]]["figure_path"] not in path:
                    path[data_qa[chart_data["question_id"]]["figure_path"]] = 0
                path[data_qa[chart_data["question_id"]]["figure_path"]] -= 1 
                
                
            if chart_data["score"] == 1 and image_data["score"] == 0:
                if data_qa[chart_data["question_id"]]["figure_path"] not in path:
                    path[data_qa[chart_data["question_id"]]["figure_path"]] = 0
                path[data_qa[chart_data["question_id"]]["figure_path"]] += 1 
                
                
            if data_qa[chart_data["question_id"]]["figure_path"] not in path_score:
                path_score[data_qa[chart_data["question_id"]]["figure_path"]] = {"image": 0, "chart": 0}
            path_score[data_qa[chart_data["question_id"]]["figure_path"]]["image"] += (image_data["score"] if not image_data["score"] == -1 else 0)
            path_score[data_qa[chart_data["question_id"]]["figure_path"]]["chart"] += (chart_data["score"] if not chart_data["score"] == -1 else 0)

    # 输出结果
    # print("Matching question IDs:", matching_question)
    # with open("compare_res.json", "w") as f:
    #     json.dump(matching_question, f, indent=4)
    # print(qid)
    path = dict(sorted(path.items(), key=lambda item: item[1]))
    # print(path)
   
    path_score = dict(sorted(path_score.items(), key=lambda item: item[1]["chart"]))
    # print(path_score)
    # for item in path_score:
    #     print(item,path_score[item])
        
        
    easy_path_score = {k: v for k, v in path_score.items() if v['chart'] < v['image']}
    easy_path_score = {k: path_score[k] for k in sorted(easy_path_score)}
    even_path_score = {k: v for k, v in path_score.items() if v['chart'] == v['image']}
    even_path_score = {k: path_score[k] for k in sorted(even_path_score)}
    hard_path_score = {k: v for k, v in path_score.items() if v['chart'] > v['image']}
    hard_path_score = {k: path_score[k] for k in sorted(hard_path_score)}
    
    res = {}
    # 如果文件存在，读取原有数据
    
    # file_path = "/data/tianchi/minzhi/chartQA/code/ana/bar/simple/gemini/value.json"
    # if Path(file_path).exists():
    #     with open(file_path, "r") as f:
    #         existing_data = json.load(f)
    # else:
    #     existing_data = {}

    # # 更新数据（假设 path_score 是一个字典）
    # print(len(existing_data))
    # # print(existing_data)
    # print("--------------------------------------")
    # # print(path_score)
    # existing_data.update(path_score)  # 或者用其他方式合并数据

    # print(len(existing_data))
    # # 写入合并后的数据
    # with open(file_path, "w") as f:
    #     json.dump(existing_data, f, indent=4)

   
    # # print(path_score.keys())
    # print("-----------------")
    
    # global file_idx
    # for item in easy_path_score:
    #     print(f"/data/tianchi/minzhi/chartQA/code/CharXiv/img/bar/single/archive{file_idx}/plain_chart/"+item+".png",easy_path_score[item])
    #     source_filepath = f"/data/tianchi/minzhi/chartQA/code/CharXiv/img/bar/single/archive{file_idx}/chart/h/"+item+".png"
    #     target_filepath = ""
    #     if os.path.exists(source_filepath):
    #         print(f"           {source_filepath}")
    #         # shutil.copy(source_filepath, target_filepath)
    #     source_filepath = f"/data/tianchi/minzhi/chartQA/code/CharXiv/img/bar/single/archive{file_idx}/chart/v/"+item+".png"
        # if os.path.exists(source_filepath):
        #     print(f"           {source_filepath}")
            # shutil.copy(source_filepath, target_filepath)
            


def eval_value(path):
    print(path.split("/")[-1])
    with open(path, 'r') as file:
        # 解析 JSON 数据
        data = json.load(file)
    count = {0:0, 1:0}
    for idx in data:
        item = data[idx]
        if "response" not in item:
            continue
        # print(item["response"])
        if compare_value(item["answer"], item["response"]):
            data[idx]["score"] = 1
        else: 
            data[idx]["score"] = 0
        # if idx == "3":
        #     print(item["answer"], item["response"],data[idx]["score"])
        #     break
        count[data[idx]["score"]] += 1
                
    with open(path.replace(path.split('/')[-1],"score-"+path.split('/')[-1]), 'w') as f:
        json.dump(data, f, indent=4)      
    print(count,count[1]/(count[0] + count[1]))
    return count


def analysis(chartpath, imagepath):
    print("")
    eval_value(chartpath)
    eval_value(imagepath)
    chartpath =  chartpath.replace(chartpath.split('/')[-1],"score-"+chartpath.split('/')[-1])
    imagepath =  imagepath.replace(imagepath.split('/')[-1],"score-"+imagepath.split('/')[-1])
    with open(chartpath, 'r') as file:
        data_chart = json.load(file)
    with open(imagepath, 'r') as file:
        data_image = json.load(file)
    # compare(data_chart, data_image)
    # compare(data_image, data_chart, target_root = "/data/tianchi/minzhi/chartQA/code/ana/bar/simple/value/hard")


file_idx = 3

# with open(f"/data/tianchi/CharXiv/data/line/line_QA_value.json", 'r') as file:
#     # 解析 JSON 数据
#     data_qa = json.load(file)
    
# analysis("/data/tianchi/minzhi/chartQA/code/ana/bar/simple/gemini/record/bar-difference-internlm-xcomposer2-4khd-7b-chart.json",
#          "/data/tianchi/minzhi/chartQA/code/ana/bar/simple/gemini/record/bar-difference-internlm-xcomposer2-4khd-7b-image.json")


# model = 'gemini-2.0-flash'
# analysis(f"/data/tianchi/CharXiv/results/{model}/{model}_line_value_plain.json",
#          f"/data/tianchi/CharXiv/results/{model}/{model}_line_value_info.json")

# analysis(f"/data/tianchi/CharXiv/results/{model}/{model}_line_difference_plain.json",
#          f"/data/tianchi/CharXiv/results/{model}/{model}_line_difference_info.json")

# file_list = ["/Users/linminzhi/Documents/chartQA/code/QA/our_bar/icon-label/record/gemini-2.0-flash_label_difference_bar_QA.json",
            #  "/Users/linminzhi/Documents/chartQA/code/QA/our_bar/icon-label/record/new_gemini-2.0-flash_label_difference_bar_QA.json",
            #  "/Users/linminzhi/Documents/chartQA/code/QA/our_bar/icon-label/record/gemini-2.0-flash_visual_difference_bar_QA.json",
            #  "/Users/linminzhi/Documents/chartQA/code/QA/our_bar/icon-label/record/new_gemini-2.0-flash_visual_difference_bar_QA.json",
            #  "/Users/linminzhi/Documents/chartQA/code/QA/our_bar/icon-label/record/gemini-2.0-flash_label_value_bar_QA.json",
            #  "/Users/linminzhi/Documents/chartQA/code/QA/our_bar/icon-label/record/new_gemini-2.0-flash_label_value_bar_QA.json",
            #  "/Users/linminzhi/Documents/chartQA/code/QA/our_bar/icon-label/record/gemini-2.0-flash_visual_value_bar_QA.json",
            #  "/Users/linminzhi/Documents/chartQA/code/QA/our_bar/icon-label/record/new_gemini-2.0-flash_visual_value_bar_QA.json",
            #  "/Users/linminzhi/Documents/chartQA/code/QA/our_bar/icon-label/record/line_gemini-2.0-flash_label_difference_QA.json",
            #  "/Users/linminzhi/Documents/chartQA/code/QA/our_bar/icon-label/record/line_gemini-2.0-flash_visual_difference_QA.json",
            #  "/Users/linminzhi/Documents/chartQA/code/QA/our_bar/icon-label/record/line_gemini-2.0-flash_label_value_QA.json",
            #  "/Users/linminzhi/Documents/chartQA/code/QA/our_bar/icon-label/record/line_gemini-2.0-flash_visual_value_QA.json"
            #  ]
file_list = ["/Users/linminzhi/Documents/chartQA/code/QA/our_bar/icon-label/record/icon-label/gemini-2.0-flash_flag_no-label_label_value_bar_QA.json",
             "/Users/linminzhi/Documents/chartQA/code/QA/our_bar/icon-label/record/icon-label/gemini-2.0-flash_flag_origin_label_value_bar_QA.json",
             "/Users/linminzhi/Documents/chartQA/code/QA/our_bar/icon-label/record/icon-label/gemini-2.0-flash_no-label_icon_value_bar_QA.json",
             "/Users/linminzhi/Documents/chartQA/code/QA/our_bar/icon-label/record/icon-label/gemini-2.0-flash_no-label_label_value_bar_QA.json",
             "/Users/linminzhi/Documents/chartQA/code/QA/our_bar/icon-label/record/icon-label/gemini-2.0-flash_origin_icon_value_bar_QA.json",
             "/Users/linminzhi/Documents/chartQA/code/QA/our_bar/icon-label/record/icon-label/gemini-2.0-flash_origin_label_value_bar_QA.json"]
for file in file_list:
    count1 = eval_value(file)
    # count2 = eval_value(file.replace("gemini-2.0-flash","new_gemini-2.0-flash"))
    # count = {0:count1[0]+count2[0],1:count1[1]+count2[1]}
    # print(count,count[1]/(count[0] + count[1]))
    print()

# eval_value("/Users/linminzhi/Documents/chartQA/code/QA/our_bar/hard/gemini-2.0-flash_value_bar_info_QA.json")
# eval_value("/Users/linminzhi/Documents/chartQA/code/QA/our_bar/hard/gemini-2.0-flash_value_bar_plain_QA.json")
# eval_value("/Users/linminzhi/Documents/chartQA/code/QA/our_bar/radial/gemini-2.0-flash-exp_radial_difference_bar_QA_plain.json")
# eval_value("/Users/linminzhi/Documents/chartQA/code/QA/our_bar/radial/gemini-2.0-flash-exp_radial_extreme_bar_QA_info.json")
# eval_value("/Users/linminzhi/Documents/chartQA/code/QA/our_bar/radial/gemini-2.0-flash-exp_radial_extreme_bar_QA_plain.json")
# eval_value("/Users/linminzhi/Documents/chartQA/code/QA/our_bar/radial/gemini-2.0-flash-exp_radial_value_bar_QA_info.json")
# eval_value("/Users/linminzhi/Documents/chartQA/code/QA/our_bar/radial/gemini-2.0-flash-exp_radial_value_bar_QA_plain.json")