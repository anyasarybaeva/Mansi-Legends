import os
import re
import pandas as pd

path = os.getcwd() + '/preprocess/'
data = pd.read_csv(path + "overall_80K.csv")

count = -1
for example in data["source"]:
    count += 1
    # убираем потенциально мансийские названия в кавычках
    cut_version = re.sub('[\"«].*?[»\"]', '', example)
    # убираем потенциально мансийские названия населенных пунктов (но тут может уже дать осечку)
    cut_version = re.sub('([А-Я]|А̄|Ē|Ё̄|О̄|Ы̄|Ю̄|Э̄|Я̄|Ӯ|Ӈ)([а-я]|а̄|ē|ё̄|о̄|ы̄|ю̄|э̄|я̄|ӯ|ӈ)+(-([А-Я]|А̄|Ē|Ё̄|О̄|Ы̄|Ю̄|Э̄|Я̄|Ӯ|Ӈ|[а-я]|а̄|ē|ё̄|о̄|ы̄|ю̄|э̄|я̄|ӯ|ӈ)+)?', '', cut_version)
    if len(re.findall('(а̄|ē|ё̄|о̄|ы̄|ю̄|э̄|я̄|ӯ|ӈ|А̄|Ē|Ё̄|О̄|Ы̄|Ю̄|Э̄|Я̄|Ӯ|Ӈ)', cut_version)) > 0:
        # один несчастый пример с дурацкими символами
        if example.startswith("Иван Егорович был из деревни") == True:
            continue
        new_source = data["target"][count]
        new_target = data["source"][count]
        data.at[count, "target"] = new_target
        data.at[count, "source"] = new_source

data.to_csv(path + 'overall_80K_sorted.csv', sep=',', encoding='utf-8', index=False)
print("all done!")
