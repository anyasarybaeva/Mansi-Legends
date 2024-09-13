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

    // Обработчик для смены языка
    document.getElementById('changeLang').addEventListener('click', function () {
        // Получаем текущие тексты
        const mansitxt = document.getElementById('mansitxt');
        const rustxt = document.getElementById('rustxt');

        // Меняем текст местами
        const tempText = mansitxt.textContent;
        mansitxt.textContent = rustxt.textContent;
        rustxt.textContent = tempText;

        // Убираем активный класс у обоих элементов
        mansitxt.classList.remove('active');
        rustxt.classList.remove('active');

        // Добавляем активный класс только к элементу на месте "Русский"
        rustxt.classList.add('active');
    });

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