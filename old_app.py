from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Если у вас есть модель, раскомментируйте эти строки
# model = torch.load('model/model.pth')
# model.eval()

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

@app.post("/process")
async def process_text(input_data: TextInput):
    input_text = input_data.text

    # Пример обработки текста моделью
    output_text = model_process(input_text)

    return {"output": output_text}

def model_process(text):
    # Здесь можно вставить логику обработки текста с использованием модели
    # Пример обработки текста — перевод в верхний регистр
    return text.upper()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("htmlMain.html", {"request": request})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)