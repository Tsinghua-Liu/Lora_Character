# coding=utf-8
import json
import re
from tqdm import tqdm
from pypinyin import lazy_pinyin

def hanzi_to_pinyin(hanzi):
    """
    将汉字转换为拼音的拼接形式
    :param hanzi: 汉字字符串
    :return: 拼音的拼接字符串
    """
    # 使用 lazy_pinyin 获取不带声调的拼音列表
    pinyin_list = lazy_pinyin(hanzi)
    pinyin_listnoblank = []
    for abc in pinyin_list:
        if abc == " ":
            continue
        else:
            pinyin_listnoblank.append(abc)

    # 将拼音列表拼接成一个字符串
    pinyin_result = ''.join(pinyin_listnoblank)
    return pinyin_result

"""把数据整理为 下面的格式
[
    {
        "role": "system",
        "content": "你需要扮演三国演义中的张飞，你需要根据当前的剧情进行发言。剧情： 在书生读着告示的过程中，挑着凉席进城来卖的涿州楼桑村百姓刘备（字玄德）来到告示墙前看着告示。此人是中山靖王刘胜之后，汉景帝的玄孙。之后，涿州县城百姓关羽（字云长）、张飞（字翼德）也先后来到告示墙前看着告示。, ： 听完书生读完告示，刘备挑起自己的凉席，深深地叹了一口气。, 刘 备： 唉！站在人群中的张飞听到刘备的叹气声，瞪着大环眼极为不满。"
    },
    {
        "role": "user",
        "content": ""
    },
    {
        "role": "assistant",
        "content": "张 飞：嗯？大丈夫不为国家出力，反在此长叹，何为大丈夫？"
    }
],

然后运行 sanguo/lora/data/sanguo/dataload  进行数据处理
最后就可以使用lora进行训练了
"""
character = "陶 谦"  # 构建曹操数据集
play_role_prompt = "你需要扮演三国演义中的人物，你需要以人物的语言风格进行对话。"
#回溯历史剧情长度
His_Plot_Time = 2
output_file = f"train_data/train_data_{hanzi_to_pinyin(character)}.json"

def split_plot(text):
    lines = text.split('\n')
    plots = []  # 按照"剧情"  对文本进行分割，保存到列表中
    plot = [] # 单个剧情
    Firstline = True
    for line in lines:
        stripped = line.strip()

        if stripped.startswith('剧情')  : #新的剧情
            if Firstline:
                #plots.append(plot)
                plot = []
                Firstline = False
            else:
                plots.append(plot)
                plot = []
            parts = stripped.split("：")
            plot.append({parts[0]: parts[1]})
        else :
            parts = stripped.split("：")
            if isinstance(parts,list):
                if len(parts) ==2 :
                    plot.append({parts[0]: parts[1]})
            else:
                print("：后无内容", str(parts))
    return plots


input_file = "cleaned_output.txt"
# 读取原始文件
with open(input_file, "r", encoding="utf-8") as f:
    original_text = f.read()
# 执行清洗操作
plots = split_plot(original_text)

def llm_sum(history_plot):
    return history_plot

save_train_data = []
for index,plot in tqdm(enumerate(plots)):
    history_plot = None
    for plot_ in plot:
        name_ = list(plot_.keys())[0]

        start_index  = (index-His_Plot_Time) if index>His_Plot_Time else 0
        end_index = index
        if character in name_: #这个剧情里面有曹操，那么就索引前面几个剧情和对话，直接进行拼接
            if end_index<2:  #整部剧前两个剧情就有角色
                history_plot = str(plot["剧情"])
            else:
                history_plot = str(plots[start_index:index]).replace("}, {"," ").replace("}","").replace("]","").replace("{","").replace("[","") \
                               + plot[0]["剧情"]
            history_plot = history_plot.replace("'", "").replace(":","：")
            history_plot = history_plot.replace("剧情:","").replace("剧情：","")
            history_plot = play_role_prompt + "剧情：" +  history_plot
            history_plot = llm_sum(history_plot) #使用大模型进行总结历史剧情
            break
        else:
            pass

    if history_plot!= None:
        #开始构建训练数据集的格式:支持多轮对话

        as_train_data = []
        system_message  =  {"role": "system", "content": history_plot}
        as_train_data.append(system_message)

        dialog = ""
        for plot_ in plot:
            name_ = list(plot_.keys())[0]
            text_ = list(plot_.values())[0]
            if character not in name_ and name_ != "剧情":
                dialog += f"{name_}：{text_}\n"
            if character in name_:
                if dialog != "":
                    role_message = {"role": "user", "content": dialog}
                    as_train_data.append(role_message)
                assistant_message = {"role": "assistant", "content": text_}
                as_train_data.append(assistant_message)
                dialog = ""

        save_train_data.append(as_train_data)


with open(output_file, "w", encoding="utf-8") as f:
    json.dump(save_train_data,f,ensure_ascii=False,indent=4)

print(f"训练数据集，已保存至 {output_file}, 一共 {len(save_train_data)} 条数据")