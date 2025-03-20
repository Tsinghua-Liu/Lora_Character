import re
"""
请你使用python 代码，帮我删除以下内容。注意代码必须通用，最终的目的是保留核心的台词信息和剧情：
"
字幕：
导   演：
编   剧：
第一集演员表所对应的几行（这几行当中都没有 "："），对于演员表所对应的处理逻辑：一次向下找几行，直到找到冒号停止，这之间的内容全部删除。
"
"""

def clean_drama_text(text):
    lines = text.split('\n')
    cleaned_lines = []
    skip_mode = False  # 用于标记是否处于需要跳过的演员表区域
    for line in lines:
        stripped = line.strip()
        # 处理演员表区域
        if skip_mode:
            if '：' in line:  # 遇到冒号时结束跳过模式
                skip_mode = False
            continue  # 跳过区域内的所有行
        # 匹配演员表标题（包含"演员表"且没有冒号）
        if '演员表' in stripped and ':' not in stripped:
            skip_mode = True
            continue
        # 处理需要删除的元数据行
        if stripped.startswith('字幕：'):
            continue

        if re.match(r'^导\s*演：', stripped):
            continue
        if re.match(r'^编\s*剧：', stripped):
            continue
        if re.match(r'电视剧插曲', stripped):
            continue
        if stripped.startswith('\n'):
            continue
        if stripped == "":
            continue
        cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

input_file = "output.txt"
output_file = "cleaned_output.txt"

# 读取原始文件
with open(input_file, "r", encoding="utf-8") as f:
    original_text = f.read()

# 执行清洗操作
processed_text = clean_drama_text(original_text)

# 保存清洗后的文件
with open(output_file, "w", encoding="utf-8") as f:
    f.write(processed_text)

print(f"清洗完成，已保存至 {output_file}")