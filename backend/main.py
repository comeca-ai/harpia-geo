from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI(title="Harpia GEO")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def root():
    return {"status": "ok", "service": "Harpia GEO"}

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é o Harpia, assistente de GEO."},
            {"role": "user", "content": data.get("message", "")}
        ]
    )
    return {"response": response.choices[0].message.content}

@app.post("/api/diagnostico")
async def diagnostico(request: Request):
    data = await request.json()
    empresa = data.get("empresa")
    site = data.get("site")
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Gere 20 prompts GEO para esta empresa."},
            {"role": "user", "content": f"Empresa: {empresa}, Site: {site}"}
        ]
    )
    return {"empresa": empresa, "prompts": response.choices[0].message.content}
