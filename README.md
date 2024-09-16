# Mansi-Legends
[![MainRDM.png](https://i.postimg.cc/CM63n7kr/MainRDM.png)](https://postimg.cc/xqMxWKsL)
<br>Переводчик мансийского языка с использованием алгоритмов и методов машинного обучения.
## Описание проекта
Данный проект создается в рамках <b>AI Product Hack</b> - хакатона, организованного магистратурой по ИИ AI Talent Hub и компанией Napoleon IT. В рамках хакатона был выбран кейс №10 от ЮНИИТ под названием "Русско-Мансийский переводчик". Идеей нашего проекта является создание эффективного переводчика для мансийского языка, чтобы сохранить и популяризировать этот язык. Целями нашего проекта являются автоматизация процесса перевода, увеличение доступности мансийского языка и поддержка культурного наследия народа Манси. 
<br><br>Проект разворачивается в облачной инфраструктуре Yandex.Cloud. Данный сервис был выбран для реализации проекта, так как в рамках AI Product Hack участникам команд был выдан доступ к ресурсам Yandex.Cloud. Разворачивание проекта в облачной инфраструктуре Yandex.Cloud предоставляет ряд преимуществ и возможностей для эффективной работы и масштабирования. Использование Yandex.Cloud позволяет обеспечить надежную и безопасную инфраструктуру для проекта.
<br><br>На данный момент этот проект предоставляет возможность для пользователей переводить текст с русского на мансийский и наоборот, а также вводить специальные мансийские символы. Проект реализован в виде веб-сайта с возможностью осуществить перевод, узнать информацию о проекте и перейти по ссылкам в блоке с контактными данными. Дальнейшее развитие данного проекта предполагает развитие в полноценный портал мансийского языка и возможное расширение на другие редкие малые языки.
### Архитектура решения
[![Mansi-Legends-Architecture2.png](https://i.postimg.cc/T1tJxp3Z/Mansi-Legends-Architecture2.png)](https://postimg.cc/bS2tHYbT)
<br>Все решение выполнено в Yandex.Cloud. Имеется обученная модель NLLB, API Gateway и frontend. Запрос от пользователя с frontend идет через API Gateway в трансформер, после чего он выдает результат. Далее frontend отображает соответствующий перевод. Для решения используется модель NLLB (No Language Left Behind), позволяющая эффективно работать с редкими языками, что выделяет ее среди других переводчиков. Модель обучена на предоставленном корпусе данных, а также на самостоятельно найденных и синтетически сгенерированных текстах, что позволило улучшить точность трансформера.
### Структура проекта
Проект разделен на смысловые ветки.

[Полусинтетический датасет](https://github.com/anyasarybaeva/Mansi-Legends/tree/36)
- **backtranslated.csv**: полусинтетический датасет

[Краулинг и обработка данных](https://github.com/anyasarybaeva/Mansi-Legends/tree/feature/4)
- **additional_data/**: директория для скрейпинга, обработки и хранения результатов обработки дополнительных данных
  - **crawlerLS.py**: краулер и обработка текстов газеты Луима Сэрипос
- **grammar/**:  директория для скрейпинга и хранения дидактических материалов
  - **grammar.py**: скрейпер
- **preprocess/**: директория для предобработки и хранения результатов предобработки датасета
  - **preprocess.py**: преодбработчик датасета

[Приложение](https://github.com/anyasarybaeva/Mansi-Legends))
- **app.py**: Главный файл приложения FastAPI, откуда запускается сервер.
- **static/**: Директория для статических файлов, включая CSS и JavaScript.
  - **css/style.css**: Стили для веб-страницы.
  - **js/script.js**: Логика для взаимодействия с сервером через JavaScript.
  - **image/*.png**: Картинки для веб-страницы.
- **templates/htmlMain.html**: HTML-шаблон для основной веб-страницы.
### Запуск приложения
Командой `uvicorn app:app --reload` запускается сервер, который будет доступен по адресу [http://51.250.35.86:8005/.](http://51.250.35.86:8005/)
Для остановки сервера используйте сочетание клавиш `Ctrl + C` в терминале.

### Наша команда
[![ML.png](https://i.postimg.cc/3RwNy0yv/ML.png)](https://postimg.cc/Z9142Rxb)
<br>— <b>Максим Свистунов</b>, ML Engineer. Обучение модели и оптимизация алгоритмов.
<br>— <b>Анна Сарыбаева</b>, Project Manager. Организационные и технические процессы, backend-разработка.
<br>— <b>Владимир Михайлов</b>, Аналитик. Письменное написание алгоритмов.
<br>— <b>Оксана Соломенчук</b>, Data Engineer. Анализ и сбор данных, а также их редактирование и интерпретация.
<br>— <b>Вадим Паненко</b>, Дизайнер. UI/UX дизайн, разработка frontend’а, общий дизайн проекта.
