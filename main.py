import os
import json
import requests
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
from bs4 import BeautifulSoup
from typing import Optional

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
    text: Optional[str] = None
    url: Optional[str] = None

def download_json():
    if not os.path.exists(JSON_FILE):
        print(f"Downloading {JSON_FILE}...")
        response = requests.get(JSON_URL)
        with open(JSON_FILE, "wb") as f:
            f.write(response.content)
        print("Download complete.")

def extract_text_from_url(url: str) -> str:
    """Extract text content from a web page URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text from common article containers
        article_tags = soup.find_all(['article', 'main', 'div'], class_=lambda x: x and any(
            term in str(x).lower() for term in ['content', 'article', 'post', 'entry']
        ))
        
        if article_tags:
            text = ' '.join([tag.get_text(separator=' ', strip=True) for tag in article_tags])
        else:
            # Fallback to all paragraphs
            paragraphs = soup.find_all('p')
            text = ' '.join([p.get_text(separator=' ', strip=True) for p in paragraphs])
        
        # Clean up whitespace
        text = ' '.join(text.split())
        
        if not text or len(text) < 50:
            raise ValueError("Insufficient text extracted from URL")
        
        return text
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract text from URL: {str(e)}")

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
    
    # Validate input
    if not request.text and not request.url:
        raise HTTPException(status_code=400, detail="Either text or url must be provided")
    
    # Get text from URL or use provided text
    text_to_analyze = request.text
    if request.url:
        text_to_analyze = extract_text_from_url(request.url)
    
    # Encode the user's text
    query_embedding = model.encode(text_to_analyze, convert_to_tensor=True)
    
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
        "mk": best_kural.get("mk")  # Tamil meaning
    }

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
