from bs4 import BeautifulSoup
import requests
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



# URL веб-страницы, с которой мы начнем сканировать
url = 'https://www.khanty-yasang.ru/luima-seripos/no-8-1050'
root = "https://www.khanty-yasang.ru"

# Отправляем GET-запрос к странице
response = requests.get(url).text

path = os.getcwd() + '/additional_data/'
# fix_count = 0
# Проверяем, успешно ли был выполнен запрос
if response:
  # Создаем объект BeautifulSoup для парсинга HTML
  soup = BeautifulSoup(response, 'html.parser')

  # собираем ссылки на все выпуски333
  link_uls = soup.find_all("ul", {"class": "toggle-body"})
  all_links = []
  for each in link_uls:
    hrefs = each.find_all('a')
    links = map(lambda x: root + x["href"], hrefs)
    all_links += list(links)
  # первые восемь выпусков представлены в пдф, пренебрежем ими
  all_links = all_links[8:]

  # тут будем хранить пары манскийский-русской
  parallel_corpora_dict = {}
  count = 0
  for issue_link in all_links:
    # для удобства слежки за прогрессом
    print(issue_link)
    issue_response = requests.get(issue_link).text
    if issue_response:
      issue_soup = BeautifulSoup(issue_response, 'html.parser')
      # берем активную ссылку
      active_html = issue_soup.find("a", {"class": "active"})["href"]

      # собираем все ссылки на статьи текущего выпуска
      all_articles_on_page = issue_soup.find_all(href=re.compile(active_html + '/.*'))
      all_links_on_page = [root + i["href"] for i in all_articles_on_page]
      all_links_on_page = list(dict.fromkeys(all_links_on_page))

      # смотрим каждую статью
      for link in all_links_on_page:
        article_response = requests.get(link).text
        if article_response:
          article_soup = BeautifulSoup(article_response, 'html.parser')

          article_title = article_soup.find_all("h1", {"class": "page-title"})
          article_text = article_soup.find_all("div", class_=["field-body", "field-item even"])

          # записываем заголовки и статьи
          if article_title: mansi_title = cutMonospace(replaceUTF16(article_title[0].get_text()))
          if article_text: mansi_text = cutMonospace(replaceUTF16(article_text[0].get_text()))
          if len(article_title) > 1: rus_title = cutMonospace(replaceUTF16(article_title[1].get_text()))
          if len(article_text) > 1: rus_text = cutMonospace(replaceUTF16(article_text[1].get_text()))

          # для ручного исправления текстов с подсчетом исправленных текстов; не используется
          # list_to_correct = [mansi_title, mansi_text]
          # if len(article_title) > 1: list_to_correct.extend(rus_title)
          # if len(article_text) > 1: list_to_correct.extend(rus_text)
          # for example in list_to_correct:
          #   if (re.findall('(?<=\s)(([А-Я]|А̄|Ē|Ё̄|О̄|Ы̄|Ю̄|Э̄|Я̄|Ӯ|Ӈ|[а-я]|а̄|ē|ё̄|о̄|ы̄|ю̄|э̄|я̄|ӯ|ӈ)\s){4,}(?=([А-Я]|А̄|Ē|Ё̄|О̄|Ы̄|Ю̄|Э̄|Я̄|Ӯ|Ӈ|[а-я]|а̄|ē|ё̄|о̄|ы̄|ю̄|э̄|я̄|ӯ|ӈ)\s)', example)):
          #     fixed_version = re.sub('(?<=\s)(([А-Я]|А̄|Ē|Ё̄|О̄|Ы̄|Ю̄|Э̄|Я̄|Ӯ|Ӈ|[а-я]|а̄|ē|ё̄|о̄|ы̄|ю̄|э̄|я̄|ӯ|ӈ)\s){4,}(?=([А-Я]|А̄|Ē|Ё̄|О̄|Ы̄|Ю̄|Э̄|Я̄|Ӯ|Ӈ|[а-я]|а̄|ē|ё̄|о̄|ы̄|ю̄|э̄|я̄|ӯ|ӈ)\s)', lambda m: ''.join(m.group(0).split()), example)
          #     fixed_example = input("Введи исправленную версию: ")
          #     fix_count += 1
          #     print('--------------------------------')

          # раскомментировать для сохранения в отдельных папках в txt
          # with open(path + "luima_seripos_txt_mansi/mansi_title" + str(count) + ".txt", "w") as file:
          #   file.write(mansi_title)
          # with open(path + "luima_seripos_txt_mansi/mansi_text" + str(count) + ".txt", "w") as file:
          #   file.write(mansi_text)

          # if rus_title:
          #   with open(path + "luima_seripos_txt_rus/rus_title" + str(count) + ".txt", "w") as file:
          #     file.write(rus_title)
          # if rus_text:
          #   with open(path + "luima_seripos_txt_rus/rus_text" + str(count) + ".txt", "w") as file:
          #     file.write(rus_text)
          
          # if mansi_title and rus_title:
          #   with open(path + "luima_seripos_txt_both/both_title" + str(count) + ".txt", "w") as file:
          #     file.write(mansi_title + '\n\n\n' + rus_title)
          # if mansi_text and rus_text:
          #   with open(path + "luima_seripos_txt_both/both_text" + str(count) + ".txt", "w") as file:
          #     file.write(mansi_text + '\n\n\n' + rus_text)
          

          # записываем заголовки и статьи
          parallel_corpora_dict.update(
              {
                  count:
                  {
                      "mansi": mansi_title,
                      "rus": rus_title
                      },
                  count+1:
                  {
                        "mansi": mansi_text,
                        "rus": rus_text
                        }
                  })
          count += 2

        else: print("bs4 could't get article")
    else: print("bs4 could't get issue")
else: print("bs4 could't get start url")

if parallel_corpora_dict:
  df = pd.DataFrame.from_dict(parallel_corpora_dict, orient='index')
  df = df[['mansi', 'rus']]
  # ввести желаемое название файла
  df.to_csv(path + 'luima_seripos_no_monospace_all.csv', sep='|', encoding='utf-8')


    # список кодов особых букв
    # result_string = re.sub('\uf50f', 'а̄', input_string)
    # result_string = re.sub('\uf511', 'ē', input_string)
    # result_string = re.sub('\uf513', 'ё̄', input_string)
    # result_string = re.sub('\uf519', 'о̄', input_string)
    # result_string = re.sub('\uf521', 'ы̄', input_string)
    # result_string = re.sub('\uf52d', 'ю̄', input_string)
    # result_string = re.sub('\uf523', 'э̄', input_string)
    # result_string = re.sub('\uf529', 'я̄', input_string)
    
    # result_string = re.sub('\uf50e', 'А̄', input_string)
    # result_string = re.sub('\uf510', 'Ē', input_string)
    # result_string = re.sub('\uf512', 'Ё̄', input_string)
    # result_string = re.sub('\uf518', 'О̄', input_string)
    # result_string = re.sub('\uf520', 'Ы̄', input_string)
    # result_string = re.sub('\uf52c', 'Ю̄', input_string)
    # result_string = re.sub('\uf522', 'Э̄', input_string)
    # result_string = re.sub('\uf528', 'Я̄', input_string)

# print(fix_count)
