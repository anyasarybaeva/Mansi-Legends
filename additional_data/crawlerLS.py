from bs4 import BeautifulSoup
import requests
import os
import re
import pandas as pd

# URL веб-страницы, с которой мы начнем сканировать
url = 'https://www.khanty-yasang.ru/luima-seripos/no-8-1050'
root = "https://www.khanty-yasang.ru"

# Отправляем GET-запрос к странице
response = requests.get(url).text

# Проверяем, успешно ли был выполнен запрос
if response:
  # Создаем объект BeautifulSoup для парсинга HTML
  soup = BeautifulSoup(response, 'html.parser')

  # собираем ссылки на все выпуски333
  link_uls = soup.find_all("ul", {"class": "toggle-body"})
  all_links = [];
  for each in link_uls:
    hrefs = each.find_all('a')
    links = map(lambda x: root + x["href"], hrefs)
    all_links += list(links)
  # первые восемь выпусков представлены в пдф, пренебрежем ими
  all_links = all_links[8:]

  # тут будем хранить пары манскийский-русской
  parallel_corpora_dict = {}
  count = 0;
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
          if article_title: mansi_title = article_title[0].get_text()
          if article_text: mansi_text = article_text[0].get_text()
          if len(article_title) > 1: rus_title = article_title[1].get_text()
          if len(article_text) > 1: rus_text = article_text[1].get_text()

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
  path = os.getcwd() + '/Mansi-Legends/additional_data/'
  df.to_csv(path + 'luima_seripos.csv', sep='|', encoding='utf-8')
