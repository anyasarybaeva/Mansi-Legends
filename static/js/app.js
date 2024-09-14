document.addEventListener('DOMContentLoaded', () => {
    const langOptions = document.querySelector('.lang-options');
    const mansitxt = document.getElementById('mansitxt');
    const rustxt = document.getElementById('rustxt');
    const symbols = document.querySelectorAll('.symbols span');
    const textInput = document.getElementById('textInput');
    const inputTextarea = document.getElementById('.input-block textarea');
    const outputTextarea = document.getElementById('translated-text');
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

    // Обработчик для смены языка
    document.getElementById('changeLang').addEventListener('click', function () {
        // Меняем текст местами
        const mansitxt = document.getElementById('mansitxt');
        const rustxt = document.getElementById('rustxt');
        const tempText = mansitxt.textContent;
        mansitxt.textContent = rustxt.textContent;
        rustxt.textContent = tempText;

        // Обновляем состояние языков и символов
        updateLanguageState();
    });

    // Изначально устанавливаем состояние языков и символов
    rustxt.classList.add('active');

    symbols.forEach(symbol => {
        symbol.classList.add('disabled'); // Отключаем мансийские символы при загрузке
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
});
