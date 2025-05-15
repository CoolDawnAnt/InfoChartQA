def is_string_match(answer, response, case_sensitive=False):
    """
    判断两个字符串是否匹配，支持模糊子串匹配
    
    参数:
        answer: 预期字符串
        response: 待检查字符串
        case_sensitive: 是否区分大小写（默认不区分）
    
    返回:
        bool: 是否匹配
    """
    if not case_sensitive:
        answer = answer.lower()
        response = response.lower()
    
    # 1. 完全一致
    if answer == response:
        return True
    
    # 2. answer是response的子串
    if answer in response:
        return True
    
    # 3. 模糊匹配：允许少量字符不匹配（简单实现）
    # 这里使用简单的子序列检查，可以根据需求替换为更复杂的模糊匹配算法
    len_answer = len(answer)
    len_response = len(response)
    
    # answer比response长，肯定不是子串
    if len_answer > len_response:
        return False
    
    # 简单子序列检查（允许中间有少量不匹配字符）
    i = j = 0
    mismatch_count = 0
    max_mismatch = max(1, len_answer // 4)  # 允许25%的字符不匹配
    
    while i < len_answer and j < len_response:
        if answer[i] == response[j]:
            i += 1
            j += 1
        else:
            j += 1
            mismatch_count += 1
            if mismatch_count > max_mismatch:
                return False
    
    return i == len_answer


# 更强大的模糊匹配版本（使用difflib）
from difflib import SequenceMatcher

def fuzzy_string_match(answer, response, threshold=0.8, case_sensitive=False):
    """
    使用difflib的模糊匹配
    
    参数:
        threshold: 相似度阈值(0-1)
    """
    if not case_sensitive:
        answer = answer.lower()
        response = response.lower()
    
    # 完全匹配
    if answer == response:
        return True
    
    # 子串匹配
    if answer in response:
        return True
    
    # 模糊匹配
    similarity = SequenceMatcher(None, answer, response).ratio()
    return similarity >= threshold

# 在问答系统中的应用
# qa_pairs = [
#     {"answer": "人工智能", "response": "AI(人工智能)是未来趋势"},
#     {"answer": "Python", "response": "我们使用python编程"},
#     {"answer": "机器学习", "response": "深度学习是机器学习的分支"},
#     {"answer": "42", "response": "答案是42"},
#     {"answer": "hello", "response": "hi there"}
# ]

# print("\n问答系统匹配结果:")
# for pair in qa_pairs:
#     matched = fuzzy_string_match(pair["answer"], pair["response"])
#     print(f"Answer: '{pair['answer']}' | Response: '{pair['response']}' → "
#           f"{'匹配' if matched else '不匹配'}")