'''FileHeader
: @Author: Chroniflow
: @Date: 2/4/2026, 9:25:06 PM
: @LastEditors: Chroniflow
: @LastEditTime: 2/4/2026, 9:25:10 PM
: @Description: 
: @Copyright: Copyright (©)}) 2026 Chroniflow. All rights reserved.
: @Email: code@ylyq.site
'''


def parse(input_string: str, 
          bool_args: None | list[str] = None, 
          str_args: None | list[str] = None) -> dict:
    """
    从字符串中解析布尔型和字符串型参数
    
    :param input_string: 包含参数的字符串
    :type input_string: str
    :param bool_args: 布尔型参数名列表，例如 ["--arg1", "--arg2"]
    :type bool_args: list[str]
    :param str_args: 字符串型参数名列表，例如 ["--str1", "--str2"]
    :type str_args: list[str]
    
    :return: 字典，包含解析出的参数值
    :rtype: dict
    """
    # 初始化参数列表
    if bool_args is None:
        bool_args = []
    if str_args is None:
        str_args = []
    
    # 初始化结果字典
    result: dict = {}
    
    # 初始化所有布尔型参数为False
    for arg in bool_args:
        result[arg] = False
    
    # 初始化所有字符串型参数为空字符串
    for arg in str_args:
        result[arg] = ""
    
    # 如果输入字符串为空，直接返回
    if not input_string:
        return result
    
    # 分割字符串
    parts = input_string.split()
    i = 0
    length = len(parts)
    
    # 遍历所有部分
    while i < length:
        token = parts[i]
        
        # 如果是布尔型参数
        if token in bool_args:
            result[token] = True
            i += 1
        # 如果是字符串型参数
        elif token in str_args:
            # 检查是否有下一个元素，且下一个元素不是参数
            if i + 1 < length and parts[i + 1] not in bool_args and parts[i + 1] not in str_args:
                result[token] = parts[i + 1]
                i += 2  # 跳过值
            else:
                # 有参数但没有值，保持为空字符串
                i += 1
        else:
            # 不是目标参数，继续下一个
            i += 1
    
    return result