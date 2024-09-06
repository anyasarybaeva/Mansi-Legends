import os
import re
import pandas as pd

path = os.getcwd() + '/preprocess/'
data = pd.read_csv(path + "overall_80K.csv")

mydata = data["source"]
# mydata = ["Пēс наканув э̄лаль вос о̄лэ̄гыт"]

for example in mydata:
    # print(example)
    if re.search('[а̄ēё̄оы̄ю̄э̄я̄А̄ĒЁ̄О̄Ы̄Ю̄Э̄Я̄̄ӮӯӇӈ]', example, re.UNICODE):
        print(example)
