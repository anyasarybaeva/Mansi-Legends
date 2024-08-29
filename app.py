from flask import Flask, render_template, request, jsonify

# model = torch.load('path_to_model.pth') или использовать модель из Hugging Face.

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Заглушка вместо настоящей модели
def dummy_neural_network(input_text):
    # Пример работы нейронки: переводит текст в верхний регистр
    return input_text.upper()


@app.route('/process', methods=['POST'])
def process_text():
    data = request.get_json()
    input_text = data.get('text')

    # Обработка текста с помощью нейронной сети
    result = dummy_neural_network(input_text)

    return jsonify({'output': result})


if __name__ == '__main__':
    app.run(debug=True)
