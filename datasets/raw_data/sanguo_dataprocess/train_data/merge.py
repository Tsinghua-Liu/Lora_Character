import os
import json


def merge_json_files(input_folder, output_file):
    # 用于存储所有 JSON 文件中的元素
    merged_data = []

    # 遍历文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(input_folder, filename)

            # 打开并读取每个 JSON 文件
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # 确保 JSON 文件的内容是一个列表
                if isinstance(data, list):
                    merged_data.extend(data)
                else:
                    print(f"Warning: {filename} does not contain a list")

    # 将合并后的数据写入到输出文件中
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)
    print(f"文件有  {len(merged_data)} 条数据")


# 使用示例
input_folder = r"D:\desktop\ML\project\transformers-code-master\sanguo\datasets\raw_data\sanguo_dataprocess\train_data"
output_file = 'allname.json'
merge_json_files(input_folder, output_file)
