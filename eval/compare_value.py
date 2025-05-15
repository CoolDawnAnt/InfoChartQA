import re
from compare_str import fuzzy_string_match
unit_map = {
    'K': 1e3,
    'k': 1e3,
    'M': 1e6,  # 百万
    'm': 1e6,  # 百万
    'million': 1e6,  # 百万
    'bn': 1e9,  # 百万
    'Bn': 1e9,  # 百万
    'b': 1e9,  # 百万

    'B': 1e9,   # 十亿
    'T': 1e12,
    "%": 1e-2,
    "Cr": 1e8,
    "None": 1,
    "Billion": 1e9
}

def extract_numbers_keep_order(text):
    matches = []

    # 1. 包含逗号的数字（不能包含小数点）
    for m in re.finditer(r'-?(?:\d+,)+\d+', text):
        if '.' not in m.group():
            matches.append((m.start(), m.group()))

    # 2. 小数（不能包含逗号）
    for m in re.finditer(r'-?\d+\.\d+', text):
        if ',' not in m.group():
            matches.append((m.start(), m.group()))

    # 3. 纯整数（不包含点或逗号，且不嵌套在已有匹配中）
    for m in re.finditer(r'(?<![\d.,])-?\d+(?![\d.,])', text):
        val = m.group()
        start = m.start()
        # 避免包含在已有匹配中
        if '.' not in val and ',' not in val and all(not (start >= s and start < s + len(v)) for s, v in matches):
            matches.append((start, val))

    # 排序按出现顺序
    matches.sort()

    # 返回匹配值
    return [v for _, v in matches]

def get_last_number(value):
    numbers = extract_numbers_keep_order(value)
    if len(numbers) == 0:
        return None
    value = numbers[-1]
    
    if value.count('.') > 0:
        if value.count('.') == 1:
            return convert(value)
        if only_digits_and_commas(value, '.'):
            return convert(value.replace(".",""))
        return value
    elif value.count(',') > 0:
        if only_digits_and_commas(value, ','):
            return convert(value.replace(",",""))
        if value.count(',') == 1:
            return convert(value.replace(',','.'))
        return value
    return value

def only_digits_and_commas(s, divide):
    res1 = False
    res2 = False
    if divide == ",":
        pattern = r'^\d{1,3}(,\d{3})*$'
        if bool(re.fullmatch(r'[0-9,]+', s)):
            res1 = True
            if is_valid_thousand_separator(s, divide):
                res2 = True
    elif divide == ".":
        pattern = r'^\d{1,3}(.\d{3})*$'
        if bool(re.fullmatch(r'[0-9,]+', s)):
            res1 = True
            if is_valid_thousand_separator(s, divide):
                res2 = True
    return res1, res2
    
    

def is_valid_thousand_separator_old(s, divide):
    # 匹配是否为合法的千分位格式（例如：1,234,567）
    if divide == ",":
        pattern = r'^[-+]?\d{1,3}(,\d{3})*(\.(\d*))?$'
    elif divide == ".":
        pattern = r'^[-+]?\d{1,3}(.\d{3})*(\,(\d*))?$'
    else:
        return None
    return bool(re.match(pattern, s))

def convert(x):
    x_str = str(x)
    if x_str.replace('.', '', 1).isdigit() or (x_str.startswith('-') and x_str[1:].replace('.', '', 1).isdigit()):
        # print("convert",x)
        return int(float(x)) if float(x).is_integer() else float(x)
    # print("no need to convert",x)
    return x

def contains_number(s):
    for ch in s:
        if is_standard_digit(ch):
            return True
    return False

def clean(x):
    x = str(x)
    x = x.replace(" ","")
    x = x.replace("$","")
    x = x.replace("\n","")
    return convert(x)
def is_standard_digit(char):
    return bool(re.match(r'^[0-9]$', char))
def get_unit(value):
    _v = str(value)
    n = len(_v)
    R , L = n , 0
    for i in range(n - 1, -1, -1):
        if value[i].isalpha() or value[i] == '%':
            R = i
            break
    
    # print('debugging',L , R + 1)
    if R == n:
        return "None"
    for i in range(R, -1, -1):
        if not value[i].isalpha() and value[i] != '%':
            L = i + 1
            break
    if L > R:
        return "None"
    return value[L : R + 1]


    
def loose_is_digit(s):
    for ch in s:
        if is_standard_digit(ch) or ch == ',' or ch == '.' or ch == '+' or ch == '-':
            continue
        return False
    return True

def get_numeric(value):
    _v = str(value)
    n = len(_v)
    L , R = -1 , n
    
    i = 0
    while i < n:
        if not is_standard_digit(value[i]) and value[i] != '+' and value[i] != '-':
            i = i + 1
            continue
        j = i
        while j < n and loose_is_digit(value[j]):
            j = j + 1
        L, R = i, j
        # print("cnm",i , j,value[i:j])
        i = j
    if L == -1:
        return 0
    else:
        return value[L : R]
def convert_to_number(value):
    unit_part = get_unit(value)
    
    value = str(value).replace("$","")
    if is_number(value):
        return float(value)
    # 提取数字部分和单位部分
    if not is_number(value[:-1]):
        return value
    number_part = float(value[:-1])  # 去掉最后一个字符（单位）
    return number_part * unit_part


def is_number(s):
    try:
        float(s)  # 尝试将字符串转换为浮点数
        return True
    except ValueError:
        return False

def is_valid_thousand_separator(s, divide):
    # 匹配是否为合法的千分位格式（例如：1,234,567）

    if divide == ",":
        pattern = r'^[-+]?\d{1,3}(,\d{3})*(\.(\d*))?$'
    elif divide == ".":
        pattern = r'^[-+]?\d{1,3}(.\d{3})*(\,(\d*))?$'
    else:
        return False
    return bool(re.match(pattern, s))

def Convert2Number(value):
    # print('fucker',value)
    if value[-1] == '.':
        value = value[:-1]
    f = 1
    # print('fucker',value)
    if (value[0] == '+') or (value[0] == '-'):
        f = 1 if (value[0] == '+') else 0
        value = value[1:]
    sep, comma = ',', '.'
    # print(value,is_valid_thousand_separator(value , ','),is_valid_thousand_separator(value , '.'))
    if ((not is_valid_thousand_separator(value , ',')) and is_valid_thousand_separator(value, '.')):
        sep, comma = '.' , ','
    elif (not is_valid_thousand_separator(value , ',')) and (not is_valid_thousand_separator(value, '.')):# 2018,36.8
        value = value.split(',')[-1]
    # print("sep check",value , sep, comma,is_valid_thousand_separator(value , ','))
    cmx = value.replace(sep,"")
    cmx = cmx.replace(comma,".")
    # print(f,value)
    if is_number(cmx):
        return float(cmx) if f else -float(cmx)
    else:
        return -1145141919810

# from quantulum3 import parser as PSP
def get_unit_and_numeric(_s):
    s = str(_s)
    lst = s.split(' ')
    n = len(lst)
    for i in range(n - 1 , -1 , -1):
        if contains_number(lst[i]):
            # print("cmx",lst[i])
            Answer = lst[i]
            Answer = Answer.replace(" ","")
            Answer = Answer.replace("$","")
            Answer = Answer.replace("\n","")
            # print("zst",Answer)
            number = get_numeric(Answer)
            unit = get_unit(Answer)
            if unit == 'None' and i + 1 < n:
                unit = get_unit(lst[i + 1])
            if unit not in unit_map:
                unit = "None"
            return number , unit
    return "1145141919810" , "None"
    
def compare_numeric_value(_answer, _response, eps = 0.001):
    response = _response.replace('\n',' ')
    answer = _answer.replace(' ',' ')
    ans_number, ans_unit = get_unit_and_numeric(answer) 
    response_number, response_unit = get_unit_and_numeric(response)
    

    # print(response_number,response_unit)
    # print(ans_number,ans_unit,type(ans_number))
    ans_number = Convert2Number(ans_number)
    response_number = Convert2Number(response_number)

    
    for unit1 in [ans_unit, 'None']:
        for unit2 in [response_unit, 'None']:
            _ = ans_number * unit_map[unit1]
            __ = response_number * unit_map[unit2]
            # print(_ , __, abs((_ - __) / abs(_) ))
            if abs((_ - __) / (0.01 + abs(_)))  < eps:
                return True
    # for special_case in [100 , 1000 , 1000000,1000000000]: # special case for % and B->M->k
    for special_case in [100, 1000, 1000000, 1000000000]:

        if abs(special_case * ans_number - response_number) / (0.01 + abs(special_case * ans_number)) < eps:
            return True
        if abs(special_case * response_number - ans_number) / (0.01 + abs(ans_number)) < eps:
            return True
        
        
    return False

def compare_value(_answer, _response, eps = 0.001):
    answer = str(_answer)
    response = str(_response)
    
    # print("{ debugging }",answer , "{ debugging }",response)
    # if answer=="0.085":
    #     print('wxh')
        
    if contains_number(str(answer)):
        return compare_numeric_value(str(answer), str(response), eps = eps)
    else:
        return fuzzy_string_match(answer , response)

if __name__ == '__main__':
    f = compare_value("14.200000000000001","14.2 µg/m³",0.05)
    print(f)