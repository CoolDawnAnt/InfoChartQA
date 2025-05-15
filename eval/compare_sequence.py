import json
from typing import List, Hashable, Union
from collections import Counter


def is_sequence_valid(sequence: List[Union[Hashable, str]],
                      case_sensitive: bool = False,
                      strip_spaces: bool = True,
                      fuzzy_duplicates: bool = False,
                      fuzzy_threshold: float = 0.6) -> bool:
    """
    检查序列是否合法（无重复元素）

    参数:
        sequence: 待检查的序列
        case_sensitive: 是否区分大小写（仅适用于字符串）
        strip_spaces: 是否去除字符串两端空格
        fuzzy_duplicates: 是否启用模糊查重（仅适用于字符串）
        fuzzy_threshold: 模糊匹配阈值(0-1)

    返回:
        bool: True表示无重复（合法），False表示有重复（非法）

    示例:
        >>> is_sequence_valid(["A", "B", "C"])  # True
        >>> is_sequence_valid(["A", "a"], case_sensitive=False)  # False
        >>> is_sequence_valid([" apple ", "apple"])  # False
    """
    if not sequence:
        return True

    processed = []
    # print(sequence)
    for item in sequence:
        # print(item)
        if isinstance(item, str):
            # 字符串预处理
            processed_item = item
            if not case_sensitive:
                processed_item = processed_item.lower()
            if strip_spaces:
                processed_item = processed_item.strip()
            processed.append(processed_item)
        else:
            processed.append(item)

    # 常规检查（精确匹配）
    # print(processed)
    if not fuzzy_duplicates:
        return len(processed) == len(set(processed))

    # 模糊查重模式
    for i in range(len(processed)):
        for j in range(i + 1, len(processed)):
            if isinstance(processed[i], str) and isinstance(processed[j], str):
                # 使用difflib进行模糊匹配
                from difflib import SequenceMatcher
                similarity = SequenceMatcher(None, processed[i], processed[j]).ratio()
                if similarity >= fuzzy_threshold:
                    return False
            else:
                # 非字符串类型退化为精确匹配
                if processed[i] == processed[j]:
                    return False
    return True


def extract_answers_from_file(file_path):
    """
    从JSON文件中读取数据并提取answer序列

    参数:
        file_path: str - JSON文件路径

    返回:
        dict - 包含提取序列和元数据的字典
    """
    try:
        # 读取JSON文件
        with open(file_path, 'r', encoding='utf-8') as f:
            input_data = json.load(f)

        # 初始化结果字典
        result = {
            "sequences": [],
            "details": []
        }

        # 遍历每个条目
        for key, item in input_data.items():
            # 检查answer字段是否存在
            if 'answer' not in item:
                continue

            # 提取answer并按逗号分割成序列，去除前后空格
            answer_sequence = [x.strip() for x in str(item['answer']).split(',')]

            # 存储序列和相关信息
            result["sequences"].append(answer_sequence)
            result["details"].append({
                "question_id": item.get("question_id", ""),
                "figure_path": item.get("figure_path", ""),
                "qtype": item.get("qtype", -1),
                "question": item.get("question", ""),
                "sequence_length": len(answer_sequence)
            })

        return result

    except FileNotFoundError:
        print(f"错误：文件 {file_path} 未找到")
        return None
    except json.JSONDecodeError:
        print("错误：文件内容不是有效的JSON格式")
        return None
    except Exception as e:
        print(f"处理文件时发生错误：{str(e)}")
        return None


from difflib import SequenceMatcher
from typing import List, Union, Optional


def fuzzy_match(s1: str, s2: str, threshold: float = 0.6) -> bool:
    """
    模糊字符串匹配（基于相似度阈值）
    :param s1: 字符串1
    :param s2: 字符串2
    :param threshold: 相似度阈值(0-1)
    :return: 是否匹配
    """
    flag = False
    flag |= SequenceMatcher(None, s1.lower().strip(), s2.lower().strip()).ratio() >= threshold
    flag |= s1 in s2
    flag |= s2 in s1
    # print(s1 , s2 , SequenceMatcher(None, s1.lower().strip(), s2.lower().strip()).ratio(),flag)
    return flag


def is_sequence_match_ordered(
        seq1: List[str],
        seq2: List[str],
        fuzzy: bool = False,
        threshold: float = 0.6
) -> bool:
    """
    检查两个序列是否顺序完全一致
    :param seq1: 序列1
    :param seq2: 序列2
    :param fuzzy: 是否启用模糊匹配
    :param threshold: 模糊匹配阈值
    :return: 是否匹配
    """
    if len(seq1) != len(seq1):
        return False

    if not is_sequence_valid(seq1, case_sensitive=True):
        return False

    if not is_sequence_valid(seq2, case_sensitive=True):
        return False

    # print(seq1 , seq2)
    if fuzzy:
        return all(fuzzy_match(x, y, threshold) for x, y in zip(seq1, seq2))
    else:
        return all(x.strip().lower() == y.strip().lower() for x, y in zip(seq1, seq2))


def is_sequence_match_unordered(
        seq1: List[str],
        seq2: List[str],
        fuzzy: bool = False,
        threshold: float = 0.8
) -> bool:
    """
    检查两个序列是否元素一致（不考虑顺序）
    :param seq1: 序列1
    :param seq2: 序列2
    :param fuzzy: 是否启用模糊匹配
    :param threshold: 模糊匹配阈值
    :return: 是否匹配
    """
    if len(seq1) != len(seq2):
        return False

    seq1_processed = [s.lower().strip() for s in seq1]
    seq2_processed = [s.lower().strip() for s in seq2]

    if fuzzy:
        # 构建双向最佳匹配
        matched_indices = set()
        for i, s1 in enumerate(seq1):
            for j, s2 in enumerate(seq2):
                if j not in matched_indices and fuzzy_match(s1, s2, threshold):
                    matched_indices.add(j)
                    break
        return len(matched_indices) == len(seq1)
    else:
        return sorted(seq1_processed) == sorted(seq2_processed)


# 测试用例
if __name__ == "__main__":
    A = "Russia, DR Congo, Ethiopia, Bangladesh, Iraq, Yemen, Pakistan, India"
    B = "Russia: 2  \nD.R. Congo: 3  \nEthiopia: 5  \nBangladesh: 5  \nIraq: 7  \nYemen: 7  \nPakistan: 12  \nIndia: 134"
    B = B.replace("\n", ",")
    B = B.replace(" ", "")
    A = A.replace(" ", "")
    print(is_sequence_match_ordered(A.split(","), B.split(","), fuzzy=True))

    # 测试数据
    exact_ordered = ["Apple", "Banana", "Orange"]
    exact_unordered = ["Banana", "Orange", "Apple"]
    fuzzy_ordered = [" Apple ", "banana", "Orang"]
    fuzzy_unordered = ["banan", "orang", " apple"]

    # 精确顺序匹配测试
    print("精确顺序匹配:")
    print(exact_ordered, exact_ordered, is_sequence_match_ordered(exact_ordered, exact_ordered))  # True
    print(exact_ordered, exact_unordered, is_sequence_match_ordered(exact_ordered, exact_unordered))  # False

    # 精确无序匹配测试
    print("\n精确无序匹配:")
    print(exact_ordered, exact_unordered, is_sequence_match_unordered(exact_ordered, exact_unordered))  # True
    print(exact_ordered, ["Apple", "Banana"], is_sequence_match_unordered(exact_ordered, ["Apple", "Banana"]))  # False

    # 模糊顺序匹配测试
    print("\n模糊顺序匹配:")
    print(exact_ordered, fuzzy_ordered, is_sequence_match_ordered(exact_ordered, fuzzy_ordered, fuzzy=True))  # True
    print(exact_ordered, fuzzy_unordered,
          is_sequence_match_ordered(exact_ordered, fuzzy_unordered, fuzzy=True))  # False

    # 模糊无序匹配测试
    print("\n模糊无序匹配:")
    print(exact_ordered, fuzzy_unordered,
          is_sequence_match_unordered(exact_ordered, fuzzy_unordered, fuzzy=True))  # True
    print(exact_ordered, ["App", "Banan"],
          is_sequence_match_unordered(exact_ordered, ["App", "Banan"], fuzzy=True))  # False

    answer = "Trondheim,Munich,TheHague,Muscat,RasAlKhaimah,Dubai,Taipei,Doha,Ajman,AbuDhabi"
    response = "Trondheim,Munich,TheHague,Muscat,RasAlKhaimah,Dubai,Taipei,Doha,Ajman,AbuDhabi"
    print(is_sequence_match_ordered(answer.split(","), response.split(","), fuzzy=True))

    assert is_sequence_valid(["A", "B", "C"]) == True
    assert is_sequence_valid(["A", "A"]) == False

    # 大小写测试
    assert is_sequence_valid(["A", "a"], case_sensitive=False) == False
    assert is_sequence_valid(["A", "a"], case_sensitive=True) == True

    # 空格处理测试
    assert is_sequence_valid(["apple", " apple "]) == False
    assert is_sequence_valid(["apple", " apple "], strip_spaces=False) == True

    # 模糊匹配测试
    assert is_sequence_valid(["apple", "applee"], fuzzy_duplicates=True) == False
    assert is_sequence_valid(["apple", "aple"], fuzzy_duplicates=True, fuzzy_threshold=0.8) == False
    assert is_sequence_valid(["apple", "orange"], fuzzy_duplicates=True) == True

    # 混合类型测试
    assert is_sequence_valid([1, "1"]) == True
    assert is_sequence_valid([1, 1]) == False

    # 边界情况
    assert is_sequence_valid([]) == True
    assert is_sequence_valid([None, None]) == False


