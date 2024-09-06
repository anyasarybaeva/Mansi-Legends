document.addEventListener('DOMContentLoaded', () => {
    const symbols = document.querySelector('.symbols');
    const charCounter = document.querySelector('.char-counter');
    const inputTextarea = document.querySelector('.input-block textarea');
    const outputTextarea = document.querySelector('.output-block textarea');
    const translateButton = document.querySelector('.translate-button');
    const langOptions = document.querySelectorAll('.lang-options span');

    // Подсчет символов
    inputTextarea.addEventListener('input', () => {
        charCounter.textContent = $; { inputTextarea.value.length } / 5000;
    });

    // Переключение направления перевода
    langOptions.forEach(option => {
        option.addEventListener('click', () => {
            langOptions.forEach(opt => opt.classList.remove('active'));
            option.classList.add('active');

            // Показ/скрытие мансийских символов
            if (option.textContent === 'Русский') {
                symbols.style.display = 'none';
            } else {
                symbols.style.display = 'block';
            }
        });
    });

    // Функция перевода
    translateButton.addEventListener('click', () => {
        // Пример использования API перевода
        // Здесь добавьте логику для реального перевода
        outputTextarea.value = Переведенный текст: ${ inputTextarea.value };
    });
});
