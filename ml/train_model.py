# клауд Елдоса N1 — Qalqan AI v5.0
# XLM-RoBERTa Fine-tuning for Phishing/Scam URL Detection
# GPU: RTX 3070 Ti (8GB) — ~20 min for 50K URLs, ~2h for 200K
# Saves model to ./qalqan_model/

import os
import json
import csv
import io
import time
import requests
import torch
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, matthews_corrcoef, confusion_matrix
from transformers import (
    XLMRobertaTokenizer,
    XLMRobertaForSequenceClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback,
)
from torch.utils.data import Dataset

# ============================================================
# CONFIG
# ============================================================
MODEL_NAME = "xlm-roberta-base"
OUTPUT_DIR = "./qalqan_model"
MAX_LEN = 128
BATCH_SIZE = 32
EPOCHS = 5
LR = 2e-5
MAX_PHISHING_URLS = 50000  # Set higher for better accuracy (100K = ~1h, 200K = ~2h)
MAX_SAFE_URLS = 50000

print("=" * 60)
print("QALQAN AI — XLM-RoBERTa URL Classifier Training")
print("=" * 60)
print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")
print(f"VRAM: {torch.cuda.get_device_properties(0).total_mem / 1e9:.1f} GB" if torch.cuda.is_available() else "")
print(f"Model: {MODEL_NAME}")
print(f"Max URLs: {MAX_PHISHING_URLS} phishing + {MAX_SAFE_URLS} safe")
print()

# ============================================================
# 1. DOWNLOAD DATASETS
# ============================================================
DATA_DIR = Path("./training_data")
DATA_DIR.mkdir(exist_ok=True)

def download_phishtank():
    """Download PhishTank verified phishing URLs."""
    cache = DATA_DIR / "phishtank.csv"
    if cache.exists():
        print(f"  PhishTank: using cached {cache}")
        urls = []
        with open(cache, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row.get("url", "")
                if url and url.startswith("http"):
                    urls.append(url)
                    if len(urls) >= MAX_PHISHING_URLS:
                        break
        return urls

    print("  PhishTank: downloading...")
    url = "http://data.phishtank.com/data/online-valid.csv"
    try:
        res = requests.get(url, timeout=60)
        res.raise_for_status()
        cache.write_bytes(res.content)
        urls = []
        reader = csv.DictReader(io.StringIO(res.text))
        for row in reader:
            u = row.get("url", "")
            if u and u.startswith("http"):
                urls.append(u)
                if len(urls) >= MAX_PHISHING_URLS:
                    break
        return urls
    except Exception as e:
        print(f"  PhishTank download failed: {e}")
        return []

def download_tranco():
    """Download Tranco top safe domains."""
    cache = DATA_DIR / "tranco.csv"
    if cache.exists():
        print(f"  Tranco: using cached {cache}")
        with open(cache, "r") as f:
            lines = f.readlines()
        return [f"https://{line.strip().split(',')[1]}" for line in lines[1:MAX_SAFE_URLS+1] if "," in line]

    print("  Tranco: downloading top 100K...")
    try:
        res = requests.get("https://tranco-list.eu/top-1m.csv.zip", timeout=60)
        import zipfile
        with zipfile.ZipFile(io.BytesIO(res.content)) as z:
            with z.open(z.namelist()[0]) as f:
                content = f.read().decode("utf-8")
                cache.write_text(content)
        lines = content.splitlines()
        return [f"https://{line.split(',')[1]}" for line in lines[:MAX_SAFE_URLS] if "," in line]
    except Exception as e:
        print(f"  Tranco download failed: {e}")
        # Fallback: generate from common domains
        safe = ["google.com","youtube.com","facebook.com","amazon.com","wikipedia.org",
                "twitter.com","instagram.com","linkedin.com","microsoft.com","apple.com",
                "github.com","stackoverflow.com","netflix.com","reddit.com","whatsapp.com"]
        return [f"https://{d}" for d in safe]

def get_kz_urls():
    """Our own KZ-specific URLs."""
    phishing = [
        "https://kaspi-login.tk", "https://kaspi-verify.ml", "https://egov-login.ga",
        "https://halyk-bank.cf", "https://kaspi-qr.gq", "https://egov-kz.com",
        "https://my-kaspi.xyz", "https://kaspi-pay.click", "https://egov-verify.top",
        "https://homebank-kz.work", "https://crowd1.com", "https://finiko.com",
        "https://onecoin.eu", "https://forsage.io", "https://bitconnect.co",
        "https://qubittech.ai", "https://1xbet.com", "https://mostbet.com",
        "https://pin-up.kz", "https://melbet.com",
    ]
    safe = [
        "https://kaspi.kz", "https://halykbank.kz", "https://egov.kz",
        "https://kolesa.kz", "https://krisha.kz", "https://tengrinews.kz",
        "https://nur.kz", "https://zakon.kz", "https://jusan.kz",
        "https://forte.kz", "https://bcc.kz", "https://freedom.kz",
    ]
    return phishing, safe

print("Downloading datasets...")
phishing_urls = download_phishtank()
safe_urls = download_tranco()
kz_phishing, kz_safe = get_kz_urls()

# Combine
all_phishing = phishing_urls + kz_phishing
all_safe = safe_urls + kz_safe

# Balance
min_count = min(len(all_phishing), len(all_safe))
all_phishing = all_phishing[:min_count]
all_safe = all_safe[:min_count]

print(f"  Phishing: {len(all_phishing)} URLs")
print(f"  Safe: {len(all_safe)} URLs")
print(f"  Total: {len(all_phishing) + len(all_safe)} URLs")
print()

# ============================================================
# 2. PREPARE DATASET
# ============================================================
urls = all_phishing + all_safe
labels = [1] * len(all_phishing) + [0] * len(all_safe)  # 1 = phishing, 0 = safe

train_urls, test_urls, train_labels, test_labels = train_test_split(
    urls, labels, test_size=0.15, random_state=42, stratify=labels
)

print(f"Train: {len(train_urls)}, Test: {len(test_urls)}")
print()

# Tokenizer
print("Loading tokenizer...")
tokenizer = XLMRobertaTokenizer.from_pretrained(MODEL_NAME)

class URLDataset(Dataset):
    def __init__(self, urls, labels, tokenizer, max_len):
        self.urls = urls
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.urls)

    def __getitem__(self, idx):
        url = str(self.urls[idx])
        encoding = self.tokenizer(
            url, max_length=self.max_len, padding="max_length",
            truncation=True, return_tensors="pt"
        )
        return {
            "input_ids": encoding["input_ids"].squeeze(),
            "attention_mask": encoding["attention_mask"].squeeze(),
            "labels": torch.tensor(self.labels[idx], dtype=torch.long),
        }

train_dataset = URLDataset(train_urls, train_labels, tokenizer, MAX_LEN)
test_dataset = URLDataset(test_urls, test_labels, tokenizer, MAX_LEN)

# ============================================================
# 3. TRAIN MODEL
# ============================================================
print("Loading model...")
model = XLMRobertaForSequenceClassification.from_pretrained(
    MODEL_NAME, num_labels=2,
    id2label={0: "SAFE", 1: "DANGEROUS"},
    label2id={"SAFE": 0, "DANGEROUS": 1},
)

training_args = TrainingArguments(
    output_dir="./training_output",
    num_train_epochs=EPOCHS,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE * 2,
    learning_rate=LR,
    weight_decay=0.01,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="f1",
    logging_steps=100,
    fp16=torch.cuda.is_available(),  # Mixed precision for speed
    dataloader_num_workers=4,
    report_to="none",
)

def compute_metrics(pred):
    preds = np.argmax(pred.predictions, axis=1)
    labels = pred.label_ids
    return {
        "accuracy": accuracy_score(labels, preds),
        "precision": precision_score(labels, preds),
        "recall": recall_score(labels, preds),
        "f1": f1_score(labels, preds),
        "mcc": matthews_corrcoef(labels, preds),
    }

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=compute_metrics,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],
)

print()
print("=" * 60)
print("TRAINING STARTED")
print("=" * 60)
start_time = time.time()

trainer.train()

train_time = time.time() - start_time
print(f"\nTraining completed in {train_time / 60:.1f} minutes")

# ============================================================
# 4. EVALUATE
# ============================================================
print()
print("=" * 60)
print("EVALUATION")
print("=" * 60)

results = trainer.evaluate()
for k, v in results.items():
    if isinstance(v, float):
        print(f"  {k}: {v:.4f}")

# Confusion matrix
preds = trainer.predict(test_dataset)
pred_labels = np.argmax(preds.predictions, axis=1)
cm = confusion_matrix(test_labels, pred_labels)
print(f"\nConfusion Matrix:")
print(f"  TN={cm[0][0]}  FP={cm[0][1]}")
print(f"  FN={cm[1][0]}  TP={cm[1][1]}")

# ============================================================
# 5. SAVE MODEL
# ============================================================
print()
print(f"Saving model to {OUTPUT_DIR}/...")
os.makedirs(OUTPUT_DIR, exist_ok=True)

model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

# Save metrics
metrics = {
    "accuracy": results.get("eval_accuracy", 0),
    "precision": results.get("eval_precision", 0),
    "recall": results.get("eval_recall", 0),
    "f1": results.get("eval_f1", 0),
    "mcc": results.get("eval_mcc", 0),
    "train_samples": len(train_urls),
    "test_samples": len(test_urls),
    "epochs": EPOCHS,
    "training_time_minutes": round(train_time / 60, 1),
    "model": MODEL_NAME,
    "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU",
}

with open(os.path.join(OUTPUT_DIR, "training_metrics.json"), "w") as f:
    json.dump(metrics, f, indent=2)

print()
print("=" * 60)
print("DONE!")
print("=" * 60)
print(f"  Model saved: {OUTPUT_DIR}/")
print(f"  Accuracy: {metrics['accuracy']:.4f}")
print(f"  F1 Score: {metrics['f1']:.4f}")
print(f"  Training time: {metrics['training_time_minutes']} min")
print()
print("Next step: run serve_model.py to start local API")
