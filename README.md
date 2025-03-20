# 使用lora 训练大语言模型（Qwen7b）扮演角色

![image](https://github.com/user-attachments/assets/bd783501-5633-440d-b7f9-88029c60afa7)
![image](https://github.com/user-attachments/assets/dc301892-6820-4e58-9f3c-d88ad5f4568e)


### 本项目使用的是  三国演义  剧本当中的数据：datasets/raw_data/sanguo_dataprocess/train_data<br>
该数据是本人自行爬虫构建的。

lora/train_data/sanguo/data_load.py文件中构建了数据集。
![image](https://github.com/user-attachments/assets/fbc537df-6871-4d2b-8644-bec31b907ba5)


### 运行
CUDA_VISIBLE_DEVICES=0 python Lora_Character/lora
/train_lora_model.py
 --character_name  allname --num_train_epochs 2

## 本项目支持多轮对话微调，数据格式按照datasets/raw_data/sanguo_dataprocess/train_data/train_data_simazhao.json
![image](https://github.com/user-attachments/assets/9cf069ea-fa45-4b67-ac94-2e845984f82e)

## 思路详见训练代码：
![image](https://github.com/user-attachments/assets/12bf3993-7115-4ae1-9275-35b50f1d903e)
只需要将多轮对话中的 assistant 的回复进行 MASK 即可。注意是在Label 中MASK
