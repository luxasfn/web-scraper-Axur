
import requests
from bs4 import BeautifulSoup
import base64
import os

SCRAPE_URL = "https://intern.aiaxuropenings.com/scrape/407988b0-b245-4a8d-bde5-1a1bbaaf902a"
API_URL = "https://intern.aiaxuropenings.com/v1/chat/completions"
SUBMIT_URL = "https://intern.aiaxuropenings.com/api/submit-response"
API_TOKEN = "MgHq0yyMENKo9lc6JQCekKeolyeywTxk"
MODEL_NAME = "microsoft-florence-2-large"
PROMPT = "<DETAILED_CAPTION>"

response = requests.get(SCRAPE_URL)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")
img_tag = soup.find("img")
img_src = img_tag.get("src")

if img_src.startswith("data:image"):
    header, encoded = img_src.split(",", 1)
    file_ext = header.split(";")[0].split("/")[-1]
    img_data = base64.b64decode(encoded)
    img_path = f"imagem_scrape.{file_ext}"
    with open(img_path, "wb") as f:
        f.write(img_data)
    print(f"Imagem salva em: {img_path}")
else:
    raise ValueError("A imagem não está embutida como base64.")

with open(img_path, "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode("utf-8")

payload = {
    "model": MODEL_NAME,
    "messages": [
        {"role": "user", "content": PROMPT}
    ],
    "temperature": 0.5,
    "images": [image_base64]
}

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.post(API_URL, headers=headers, json=payload)

if response.status_code == 200:
    print("Resposta recebida do modelo.")
    resposta_json = response.json()
    submit = requests.post(SUBMIT_URL, headers=headers, json=resposta_json)
    if submit.status_code == 200:
        print("Resposta submetida com sucesso.")
        print(submit.text)
    else:
        print(f"Erro ao submeter resposta: {submit.status_code}")
        print(submit.text)
else:
    print(f"Erro ao consultar modelo: {response.status_code}")
    print(response.text)
