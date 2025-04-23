import re

pattern = re.compile(r'(\d+)(√)')
reverse_pattern = re.compile(r'([⁰¹²³⁴⁵⁶⁷⁸⁹]+)(?!√)')
def convert_sqrt_expression(s):
    global pattern, reverse_pattern
    superscript_map = {
        '0': '⁰',
        '1': '¹',
        '2': '²',
        '3': '³',
        '4': '⁴',
        '5': '⁵',
        '6': '⁶',
        '7': '⁷',
        '8': '⁸',
        '9': '⁹'
    }
    reverse_superscript_map = {v: k for k, v in superscript_map.items()}



    def replacer(match):
        number = match.group(1)
        sqrt_symbol = match.group(2)
        superscript = ''.join([superscript_map[d] for d in number])
        return superscript + sqrt_symbol

    converted = pattern.sub(replacer, s)



    def reverse_replacer(match):
        sup_chars = match.group(1)
        normal = ''.join([reverse_superscript_map.get(c, c) for c in sup_chars])
        return normal

    final = reverse_pattern.sub(reverse_replacer, converted)

    return final


# 示例使用
input_str = "sin(2) * 1 - 2 * ( 3 / 2 ) * 2√4 - 2".replace(' ','')
output_str = convert_sqrt_expression(input_str)
print(output_str)  # 输出：1-2*(3/2)+²√4