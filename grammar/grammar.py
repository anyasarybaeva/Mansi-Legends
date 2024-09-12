import requests
import pdfplumber
import os
import re


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

    return result_string


# URL для загрузки PDF
pdf_url = "https://ouipiir.ru/sites/default/files/docs/878-1625.pdf"
pdf_filename = "document.pdf"
path = os.getcwd() + '/grammar/'

# Скачиваем PDF файл
response = requests.get(pdf_url)
with open(pdf_filename, 'wb') as f:
    f.write(response.content)

# Функция для обработки PDF и удаления лишних элементов
def clean_pdf_text(pdf_path):
    cleaned_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                for line in lines:
                    cleaned_text += line.strip() + "\n"
                    cleaned_text = replaceUTF16(cleaned_text)
                    

    return cleaned_text.strip()

# Получаем очищенный текст
cleaned_text = clean_pdf_text(pdf_filename)
cleaned_text = re.sub('\n\d{1,2}\n', '\n', cleaned_text)
with open(path + "dictation.txt", "w") as file:
    file.write(cleaned_text)
