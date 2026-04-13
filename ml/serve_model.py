# клауд Елдоса N1 — Qalqan AI v5.0
# Local ML Model API Server
# Runs on localhost:8001 — Qalqan API calls this for ML predictions
# Inference: <50ms per URL on RTX 3070 Ti

import os
import json
import time
import torch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification

MODEL_DIR = "./qalqan_model"

app = FastAPI(title="Qalqan AI — Local ML Model", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Load model
print("Loading XLM-RoBERTa model...")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = XLMRobertaTokenizer.from_pretrained(MODEL_DIR)
model = XLMRobertaForSequenceClassification.from_pretrained(MODEL_DIR).to(device)
model.eval()
print(f"Model loaded on {device}")

# Load metrics
metrics_path = os.path.join(MODEL_DIR, "training_metrics.json")
training_metrics = {}
if os.path.exists(metrics_path):
    with open(metrics_path) as f:
        training_metrics = json.load(f)


class PredictRequest(BaseModel):
    url: str

class BatchRequest(BaseModel):
    urls: list[str]


@app.get("/")
def health():
    return {
        "status": "online",
        "model": "xlm-roberta-base (fine-tuned)",
        "device": str(device),
        "metrics": training_metrics,
    }


@app.post("/predict")
def predict(req: PredictRequest):
    start = time.time()

    inputs = tokenizer(req.url, max_length=128, padding="max_length",
                       truncation=True, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)
        pred_class = torch.argmax(probs, dim=1).item()
        confidence = probs[0][pred_class].item()

    labels = {0: "SAFE", 1: "DANGEROUS"}
    latency = int((time.time() - start) * 1000)

    return {
        "verdict": labels[pred_class],
        "confidence": round(confidence, 4),
        "threat_score": int(confidence * 100) if pred_class == 1 else int((1 - confidence) * 100),
        "source": "xlm_roberta_local",
        "latency_ms": latency,
    }


@app.post("/batch")
def batch_predict(req: BatchRequest):
    start = time.time()
    results = []

    for url in req.urls:
        inputs = tokenizer(url, max_length=128, padding="max_length",
                           truncation=True, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)
            pred_class = torch.argmax(probs, dim=1).item()
            confidence = probs[0][pred_class].item()

        labels = {0: "SAFE", 1: "DANGEROUS"}
        results.append({
            "url": url,
            "verdict": labels[pred_class],
            "confidence": round(confidence, 4),
            "threat_score": int(confidence * 100) if pred_class == 1 else int((1 - confidence) * 100),
        })

    return {
        "results": results,
        "total": len(results),
        "latency_ms": int((time.time() - start) * 1000),
    }


if __name__ == "__main__":
    import uvicorn
    print("\nStarting Qalqan ML API on http://localhost:8001")
    print("Endpoints: /predict, /batch, /")
    uvicorn.run(app, host="0.0.0.0", port=8001)
