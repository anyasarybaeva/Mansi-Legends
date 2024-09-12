from fastapi import FastAPI
from pydantic import BaseModel
from transformers import NllbTokenizer, AutoModelForSeq2SeqLM
import torch

# Инициализация FastAPI
app = FastAPI()

# Загрузка модели и токенизатора
model_path = "600m_added_vocab"  # Укажите путь к вашей модели
model, tokenizer = None, None

def fix_tokenizer(tokenizer, new_lang='mns_Cyrl'):
    old_len = len(tokenizer) - int(new_lang in tokenizer.added_tokens_encoder)
    tokenizer.lang_code_to_id[new_lang] = old_len-1
    tokenizer.id_to_lang_code[old_len-1] = new_lang
    tokenizer.fairseq_tokens_to_ids["<mask>"] = len(tokenizer.sp_model) + len(tokenizer.lang_code_to_id) + tokenizer.fairseq_offset
    tokenizer.fairseq_tokens_to_ids.update(tokenizer.lang_code_to_id)
    tokenizer.fairseq_ids_to_tokens = {v: k for k, v in tokenizer.fairseq_tokens_to_ids.items()}
    if new_lang not in tokenizer._additional_special_tokens:
        tokenizer._additional_special_tokens.append(new_lang)
    tokenizer.added_tokens_encoder = {}
    tokenizer.added_tokens_decoder = {}

def load(path: str):
    model = AutoModelForSeq2SeqLM.from_pretrained(path)
    model = model.cuda() if torch.cuda.is_available() else model
    tokenizer = NllbTokenizer.from_pretrained(path)
    fix_tokenizer(tokenizer)
    return model, tokenizer

def translate(text, model, tokenizer, to_ru=False, src_lang=None, tgt_lang=None, a=32, b=3, max_input_length=1024, num_beams=4, **kwargs):
    if not src_lang: src_lang = 'mns_Cyrl' if to_ru else "rus_Cyrl"
    if not tgt_lang: tgt_lang = 'rus_Cyrl' if to_ru else "mns_Cyrl"
    tokenizer.src_lang = src_lang
    tokenizer.tgt_lang = tgt_lang
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=max_input_length)
    result = model.generate(
        **inputs.to(model.device),
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_lang),
        max_new_tokens=int(a + b * inputs.input_ids.shape[1]),
        num_beams=num_beams,
        **kwargs
    )
    return tokenizer.batch_decode(result, skip_special_tokens=True)


@app.on_event("startup")
async def startup_event():
    global model, tokenizer
    model, tokenizer = load(model_path)

# Pydantic модель для запроса
class TranslationRequest(BaseModel):
    text: str
    to_ru: bool = True

# Маршрут для перевода текста
@app.post("/translate")
async def translate_text(request: TranslationRequest):
    result = translate(request.text, model, tokenizer, to_ru=request.to_ru)
    return {"translated_text": result[0]}
