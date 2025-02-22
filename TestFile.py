def infix_to_postfix(expression):
    # 定义操作符的优先级
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    # 初始化栈和输出列表
    stack = []
    output = []

    # 遍历中缀表达式的每个字符
    for char in expression:
        if char.isdigit():  # 如果是操作数
            output.append(char)
        elif char == '(':  # 如果是左括号
            stack.append(char)
        elif char == ')':  # 如果是右括号
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # 弹出左括号
        else:  # 如果是操作符
            while (stack and stack[-1] != '(' and
                   (precedence[char] <= precedence[stack[-1]])):
                output.append(stack.pop())
            stack.append(char)

    # 处理栈中剩余的操作符
    while stack:
        output.append(stack.pop())

    # 将后缀表达式列表转换为字符串并返回
    return ''.join(output)

# 示例
expression = "1-(1-1)-(3-2+2-3)^2"
postfix_expression = infix_to_postfix(expression)
#print(f"后缀表达式: {postfix_expression}")

def tokenize(expression):
    """将表达式字符串分解为数字、运算符和括号的列表"""
    tokens = []
    i = 0
    n = len(expression)
    while i < n:
        if expression[i].isspace():
            i += 1
            continue
        elif expression[i] in '+-*/^()':
            # 处理运算符、括号、负号（一元运算符）
            if expression[i] == '-' and (i == 0 or expression[i - 1] in '+-*/^('):
                # 处理负数（例如 "-3" 或 "(-5)")
                num = '-'
                i += 1
                while i < n and (expression[i].isdigit() or expression[i] == '.'):
                    num += expression[i]
                    i += 1
                tokens.append(num)
            else:
                # 普通运算符或括号
                tokens.append(expression[i])
                i += 1
        elif expression[i].isdigit() or expression[i] == '.':
            # 处理数字（整数或小数）
            num = ''
            while i < n and (expression[i].isdigit() or expression[i] == '.'):
                num += expression[i]
                i += 1
            tokens.append(num)
        else:
            raise ValueError(f"非法字符: {expression[i]}")
    return tokens


def infix_to_postfix(tokens:list[str]):
    """将中缀表达式转换为后缀表达式（逆波兰表示法）"""
    precedence = {'+': 2, '-': 2, '*': 3, '/': 3, '^': 4}
    associativity = {'+': 'left', '-': 'left', '*': 'left', '/': 'left', '^': 'right'}
    output = []
    stack = []

    for token in tokens:
        # 判断是否为数字（包含负数和小数）
        if token.replace('.', '', 1).lstrip('-').isdigit():
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            # 弹出栈中元素直到左括号
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # 丢弃左括号
        else:
            # 处理运算符
            while stack and stack[-1] != '(' and (
                    precedence[token] < precedence.get(stack[-1], 0) or
                    (precedence[token] == precedence.get(stack[-1], 0) and associativity[token] == 'left')
            ):
                output.append(stack.pop())
            stack.append(token)

    # 弹出栈中剩余运算符
    while stack:
        output.append(stack.pop())

    return output


# 测试示例
if __name__ == "__main__":
    test_cases = [
        "3 + 4 * 2 / (1 - -5) ^ 2",  # 预期输出: 3 4 2 * 1 5 - 2 ^ / +
        '3 + 4 * 2 / (1 + 5)^2',
        "2^3^2",  # 预期输出: 2 3 2 ^ ^
        "1 - (1 - 1) - (3 - 2 + 2 - 3)",  # 预期输出: 1 1 1 - - 3 2 - 2 + 3 - -
    ]

    for expr in test_cases:
        tokens = tokenize(expr)
        postfix = infix_to_postfix(tokens)
        #print(f"输入表达式: {expr}")
        #print(f"后缀表达式: {' '.join(postfix)}\n")
    print(infix_to_postfix("3 + 4 * 2 / ( 1 - -5 ) ^ 2".split(' ')))
