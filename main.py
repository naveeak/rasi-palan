import os
import json
import requests
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util

app = FastAPI()

# Constants
JSON_URL = "https://raw.githubusercontent.com/tk120404/thirukkural/refs/heads/master/thirukkural.json"
JSON_FILE = "thirukkural.json"
MODEL_NAME = "all-MiniLM-L6-v2"

# Global variables
kurals = []
embeddings = None
model = None

class AnalysisRequest(BaseModel):
    text: str

def download_json():
    if not os.path.exists(JSON_FILE):
        print(f"Downloading {JSON_FILE}...")
        response = requests.get(JSON_URL)
        with open(JSON_FILE, "wb") as f:
            f.write(response.content)
        print("Download complete.")

@app.on_event("startup")
async def startup_event():
    global kurals, embeddings, model
    
    # 1. Ensure data exists
    download_json()
    
    # 2. Load Data
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        # The JSON might be a list or a dict with a key. 
        # Based on the URL, it's likely a list of objects.
        if isinstance(data, dict) and "kural" in data:
             kurals = data["kural"]
        else:
             kurals = data
             
    print(f"Loaded {len(kurals)} Kurals.")

    # 3. Load Model
    print(f"Loading model {MODEL_NAME}...")
    model = SentenceTransformer(MODEL_NAME)
    
    # 4. Generate Embeddings
    # We will embed the English explanation/meaning for matching.
    # Let's inspect the first kural to see available fields if we were exploring, 
    # but here we'll assume 'eng_exp' or similar exists.
    # Common fields: 'Number', 'Line1', 'Line2', 'Translation', 'mv', 'sp', 'mk', 'explanation'
    # The user mentioned "eng_exp" in my thought process, let's try to find a rich english text field.
    # I will create a list of texts to embed.
    
    texts_to_embed = []
    for k in kurals:
        # Concatenate english translation and explanation for better context
        # Adjust keys based on the actual JSON structure. 
        # I'll try to be robust.
        eng = k.get("eng", "") or k.get("Translation", "") or k.get("translation", "")
        exp = k.get("eng_exp", "") or k.get("explanation", "") or k.get("meaning", "")
        
        # Fallback if specific keys aren't found, dump all values
        if not eng and not exp:
            text = " ".join([str(v) for v in k.values() if isinstance(v, str)])
        else:
            text = f"{eng} {exp}"
            
        texts_to_embed.append(text)

    print("Generating embeddings...")
    embeddings = model.encode(texts_to_embed, convert_to_tensor=True)
    print("Embeddings ready.")

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

@app.post("/analyze")
async def analyze_text(request: AnalysisRequest):
    if not model or embeddings is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")
    
    # Encode the user's text
    query_embedding = model.encode(request.text, convert_to_tensor=True)
    
    # Compute cosine similarities
    cosine_scores = util.cos_sim(query_embedding, embeddings)[0]
    
    # Find the top match
    best_match_idx = np.argmax(cosine_scores.cpu().numpy())
    best_kural = kurals[best_match_idx]
    
    # Map fields to what frontend expects
    return {
        "number": best_kural.get("Number"),
        "line1": best_kural.get("Line1"),
        "line2": best_kural.get("Line2"),
        "eng": best_kural.get("Translation"),
        "eng_exp": best_kural.get("explanation"),
        "chapter_group_eng": "Unknown", 
        "chapter_eng": "Unknown"
    }

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
