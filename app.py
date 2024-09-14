from inference import load, translate
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


# Загрузка модели и токенизатора
model_path = "600m_added_vocab"  # Укажите путь к вашей модели
model, tokenizer = None, None
app = FastAPI()

# Разрешаем CORS для взаимодействия с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Позволяет всем источникам доступ к API, можно сузить до нужных доменов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str
    to_ru: bool

@app.post("/process")
async def process_text(input_data: TextInput):
    input_text = input_data.text
    print( input_data, "Received call", input_text, "to Russian?:", input_data.to_ru)
    # Пример обработки текста моделью
    output_text = translate(input_text, model, tokenizer, to_ru = input_data.to_ru)

    return {"output": output_text}

# Инициализация FastAPI

@app.on_event("startup")
async def startup_event():
    global model, tokenizer
    model, tokenizer = load(model_path)


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("htmlMain.html", {"request": request})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
