import json
import os
from collections import defaultdict
from compare_value import compare_value
from compare_sequence import is_sequence_match_ordered, is_sequence_match_unordered
from compare_str import fuzzy_string_match
from compare_multiple import multiple_choice_checker

def has_more_digits_than_other_chars(s):
    if isinstance(s, (int, float)):
        return True
    s = s.replace('.', '1')
    s = s.replace(',', '1')
    s = s.replace('$', '1')
    s = s.replace('B', '1')
    s = s.replace('T', '1')
    s = s.replace('K', '1')
    digit_count = 0
    other_count = 0
    for char in s:
        if char.isdigit():
            digit_count += 1
        else:
            other_count += 1

    return digit_count > other_count


def evaluate_answer(answer, response, qtype):
    if qtype in [1, 2, 101, 102]:
        if has_more_digits_than_other_chars(answer):
            return "Exact Numeric", compare_value(answer, response)
        else:
            return "Vague String", fuzzy_string_match(answer, response)
    elif qtype in [72, 54]:
        return "Exact Numeric", compare_value(answer, response)
    elif qtype in [10, 50, 51, 52, 110]:
        return "Vague Numeric", compare_value(answer, response, eps=0.05)
    elif qtype in [13, 103, 113]:
        if answer.lower() in response.lower():
            return "Exact String", True
        return "Exact String", compare_value(answer, response)
    elif qtype in [40, 41, 42, 43, 44]:
        response = response.replace("\n", ",")
        response = response.replace(" ", "")
        answer = answer.replace(" ", "")
        return "Vague Unordered Sequence", is_sequence_match_unordered(answer.split(","), response.split(","), fuzzy=True)
    elif qtype in [60, 61, 70, 80, 90]:
        return "Vague String", fuzzy_string_match(answer, response)
    elif qtype in [71]:
        response = response.replace("\n\n", "")
        response = response.replace("\n", ",")
        response = response.replace(" ", "")
        response = response.replace("<", ",")
        response = response.replace(">", ",")
        if response.count(":") == 1:
            response = response[response.find(':') + 1:]
        answer = answer.replace(" ", "")
        return "Vague Ordered Sequence", is_sequence_match_ordered(answer.split(","), response.split(","), fuzzy=True)
    elif qtype in [30]:
        for an in answer:
            if is_sequence_match_ordered(an.split(","), response.split(","), fuzzy=True):
                return "Vague Ordered Sequence", True
        return "Vague Ordered Sequence", False
    elif qtype in [202,1919810,1919811,1919812]:
        return "Exact String", multiple_choice_checker(answer , response)
    else:
        print('there is no qtype',qtype)
        return "Exact Numeric", compare_value(answer, response)


def process_json_data(json_data):
    results = []
    stats = {
        'qtype_stats': defaultdict(lambda: {'correct': 0, 'total': 0}),
        'figure_stats': defaultdict(lambda: {'correct': 0, 'total': 0}),
        'total_correct': 0,
        'total_questions': 0
    }

    for key, item in json_data.items():
        question_id = item["question_id"]
        if 'qtype' in item:
            qtype = item["qtype"]
        elif 'qid' in item:
            qtype = item["qid"]
        else:
            qtype = 1
        if "response" not in item or item['response'] == 'Error!':
            continue

        answer = str(item["answer"])
        response = str(item["response"])
        response = response.replace(" "," ")


        figure_path = item["figure_path"]
        if type(figure_path) == list:
            figure_path = figure_path[0]

        eval_method, score = evaluate_answer(answer, response, qtype)

        results.append({
            "figure_path": figure_path,
            "answer": answer,
            "response": response,
            "question": item["question"] if "question" in item else "",
            "question_id": question_id,
            "qtype": qtype,
            "score": score,
            "eval_method": eval_method
        })

        stats['qtype_stats'][qtype]['correct'] += score
        stats['qtype_stats'][qtype]['total'] += 1

        stats['figure_stats'][figure_path]['correct'] += score
        stats['figure_stats'][figure_path]['total'] += 1

        stats['total_correct'] += score
        stats['total_questions'] += 1

    return results, stats


def calculate_accuracy(correct, total):
    return round(correct / total * 100, 2) if total > 0 else 0.0


def generate_stat_report(stats):
    report = {}

    report['overall_accuracy'] = calculate_accuracy(
        stats['total_correct'], stats['total_questions'])

    qtype_report = {}
    for qtype, counts in stats['qtype_stats'].items():
        qtype_report[f"qtype_{qtype}"] = {
            'accuracy': calculate_accuracy(counts['correct'], counts['total']),
            'correct': counts['correct'],
            'total': counts['total']
        }
    report['qtype_accuracy'] = qtype_report

    figure_report = {}
    for figure_path, counts in stats['figure_stats'].items():
        figure_report[figure_path] = {
            'accuracy': calculate_accuracy(counts['correct'], counts['total']),
            'correct': counts['correct'],
            'total': counts['total']
        }
    report['figure_accuracy'] = figure_report

    return report

from copy import deepcopy
def evaluate(input_file, output_file=None, stats_file=None):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if type(data).__name__=='list':
        __ = deepcopy(data)
        data = {}
        for _ in __:
            data[_['question_id']] = deepcopy(_)
    
    
    results, stats = process_json_data(data)
    report = generate_stat_report(stats)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Score save to {output_file}")

    if stats_file:
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"Statis saved to {stats_file}")

    print(f"Acc: {report['overall_accuracy']}% {stats['total_questions']}")

    return results, report
