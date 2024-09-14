document.addEventListener('DOMContentLoaded', () => {
    const langOptions = document.querySelector('.lang-options');
    const mansitxt = document.getElementById('mansitxt');
    const rustxt = document.getElementById('rustxt');
    const symbols = document.querySelectorAll('.symbols span');
    const textInput = document.getElementById('textInput');
    const inputTextarea = document.getElementById('.input-block textarea');
    const outputTextarea = document.getElementById('translated-text');
    const translateButton = document.getElementById('.translate-button');
    const charCount = document.getElementById('charCount');

    // Функция для обновления состояния языков и символов
    function updateLanguageState() {

        if (rustxt.classList.contains('active')) {
            // Если активен русский язык
            rustxt.classList.remove('active');
            mansitxt.classList.add('active');

            // Включаем мансийские символы
            symbols.forEach(symbol => {
                symbol.classList.remove('disabled');
            });
        } else {
            // Если активен мансийский язык
            mansitxt.classList.remove('active');
            rustxt.classList.add('active');

            // Отключаем мансийские символы
            symbols.forEach(symbol => {
                symbol.classList.add('disabled');
            });
        }
    }

    // Ввод мансийских символов
    symbols.forEach(symbol => {
        symbol.addEventListener('click', function () {
            // Вставляем символ в текущее положение курсора
            const start = textInput.selectionStart;
            const end = textInput.selectionEnd;
            const value = textInput.value;

            // Обновляем значение текстового поля
            textInput.value = value.substring(0, start) + this.textContent + value.substring(end);

            // Перемещаем курсор после вставленного символа
            textInput.selectionStart = textInput.selectionEnd = start + this.textContent.length;

            // Фокусируемся на текстовом поле
            textInput.focus();
        });
    });

    // Подсчет введенных символов
    // Функция для обновления счетчика символов
    function updateCharCount() {
        const currentLength = textInput.value.length;
        const maxlength = this.getAttribute('maxlength');
        charCount.textContent = currentLength; maxlength;
        maxlength
    }

    // Добавляем обработчик события input для обновления счетчика при изменении текста
    textInput.addEventListener('input', updateCharCount);

    // Инициализируем счетчик при загрузке страницы
    updateCharCount();

    // Функция перевода backend
    document.getElementById('translate-button').addEventListener('click', function () {
        const textToTranslate = textInput.value;
        const selectedLanguage = document.querySelector('.lang-options span.active').textContent;

        fetch('https://your-backend-service-url.com/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: textToTranslate,
                targetLanguage: selectedLanguage === 'Русский' ? 'ru' : 'mansi'
            })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('HTTP error! Status: ');
                }
                return response.json();
            })
            .then(data => {
                outputTextarea.value = data.translatedText;
            })
            .catch(error => {
                outputTextarea.value = 'error';
            });
    });
});
