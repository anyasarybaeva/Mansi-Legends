# overall_80K.csv -- стартовый датасет
# overall_80K_sorted.csv -- датасет с корректно определенными target и source
# overall_80K_sorted_no_monospace.csv -- датасет с корректно определенными target и source + чисткой моноспейсов

import os
import re
import pandas as pd

# функция для приведения особых букв к привычному формату + чистки переноса слов на новую строку
def replaceUTF16(input_string):
    result_string = re.sub('', 'а̄', input_string)
    result_string = re.sub('', 'ē', result_string)
    result_string = re.sub('', 'ё̄', result_string)
    result_string = re.sub('', 'о̄', result_string)
    result_string = re.sub('', 'ы̄', result_string)
    result_string = re.sub('', 'ю̄', result_string)
    result_string = re.sub('', 'э̄', result_string)
    result_string = re.sub('', 'я̄', result_string)
    
    result_string = re.sub('', 'А̄', result_string)
    result_string = re.sub('', 'Ē', result_string)
    result_string = re.sub('', 'Ё̄', result_string)
    result_string = re.sub('', 'О̄', result_string)
    result_string = re.sub('', 'Ы̄', result_string)
    result_string = re.sub('', 'Ю̄', result_string)
    result_string = re.sub('', 'Э̄', result_string)
    result_string = re.sub('', 'Я̄', result_string)

    # чистим переносы строк
    result_string = re.sub('(?<=[а̄ēё̄оы̄ю̄э̄я̄А̄ĒЁ̄О̄Ы̄Ю̄Э̄Я̄̄ӮӯӇӈ\w])[-–]\s(?![А-ЯА̄ĒЁ̄О̄Ы̄Ю̄Э̄Я̄̄ӮӇ])', '', result_string)
    result_string = re.sub('(?<=[а̄ēё̄оы̄ю̄э̄я̄А̄ĒЁ̄О̄Ы̄Ю̄Э̄Я̄̄ӮӯӇӈ\w])[-–]\s', '-', result_string)

    return result_string


# функция ищет слова, записанные побуквенно через пробел
def cutMonospace(input_string):
   if re.search('(?<=\s)(([А-Я]|А̄|Ē|Ё̄|О̄|Ы̄|Ю̄|Э̄|Я̄|Ӯ|Ӈ|[а-я]|а̄|ē|ё̄|о̄|ы̄|ю̄|э̄|я̄|ӯ|ӈ)\s){4,}(?=([А-Я]|А̄|Ē|Ё̄|О̄|Ы̄|Ю̄|Э̄|Я̄|Ӯ|Ӈ|[а-я]|а̄|ē|ё̄|о̄|ы̄|ю̄|э̄|я̄|ӯ|ӈ)\s)', input_string):
    return re.sub('(?<=\s)(([А-Я]|А̄|Ē|Ё̄|О̄|Ы̄|Ю̄|Э̄|Я̄|Ӯ|Ӈ|[а-я]|а̄|ē|ё̄|о̄|ы̄|ю̄|э̄|я̄|ӯ|ӈ)\s){4,}(?=([А-Я]|А̄|Ē|Ё̄|О̄|Ы̄|Ю̄|Э̄|Я̄|Ӯ|Ӈ|[а-я]|а̄|ē|ё̄|о̄|ы̄|ю̄|э̄|я̄|ӯ|ӈ)\s)', lambda m: ''.join(m.group(0).split()), input_string)
   else:
     return input_string



path = os.getcwd() + '/preprocess/'
data = pd.read_csv(path + "overall_80K.csv")

count = -1
for example in data["source"]:
    count += 1
    # чистим нестандартные буквы и моноспейсы, если нужно
    data.at[count, "target"] = cutMonospace(replaceUTF16(data.at[count, "target"]))
    data.at[count, "source"] = cutMonospace(replaceUTF16(data.at[count, "source"]))
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

# название файла выставить желаемое
data.to_csv(path + 'overall_80K_sorted.csv', sep=',', encoding='utf-8', index=False)
print("all done!")
