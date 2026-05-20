# Qalqan AI — XLM-RoBERTa-large Fine-tuning (A100 / Google Colab)
# Model:   xlm-roberta-large (560M params, 100 languages)
# Classes: 5 — safe / phishing / malware / pyramid / gambling
# GPU:     A100 40GB — batch=64, MAX_LEN=256 → ~25 min for 150K URLs
#
# === Google Colab Setup ===
# Runtime → Change runtime type → A100
# Then run:
#   !pip install transformers datasets scikit-learn torch accelerate -q
#   from google.colab import drive; drive.mount('/content/drive')
#   # Upload this file and run it, or paste in a notebook cell

import os
import json
import csv
import io
import time
import math
import requests
import torch
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, matthews_corrcoef, confusion_matrix, classification_report
)
from transformers import (
    XLMRobertaTokenizer,
    XLMRobertaForSequenceClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback,
    DataCollatorWithPadding,
)
from torch.utils.data import Dataset

# ============================================================
# CONFIG
# ============================================================
MODEL_NAME = "xlm-roberta-large"        # upgrade from base
OUTPUT_DIR = "./qalqan_model_v2"
DRIVE_SAVE_DIR = "/content/drive/MyDrive/qalqan_model_v2"  # Colab Drive save

NUM_LABELS = 5
LABEL_NAMES = ["safe", "phishing", "malware", "pyramid", "gambling"]
LABEL2ID = {name: i for i, name in enumerate(LABEL_NAMES)}
ID2LABEL = {i: name for i, name in enumerate(LABEL_NAMES)}

MAX_LEN = 256           # was 128
BATCH_SIZE = 64         # A100 40GB handles this for large model
GRAD_ACCUM = 2          # effective batch = 128
EPOCHS = 5
LR = 1e-5               # smaller LR for large model
WARMUP_RATIO = 0.06
WEIGHT_DECAY = 0.01
MAX_URLS_PER_CLASS = 30_000

print("=" * 60)
print("QALQAN AI v2 — XLM-RoBERTa-large Multi-class Training")
print("=" * 60)
gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
vram = torch.cuda.get_device_properties(0).total_mem / 1e9 if torch.cuda.is_available() else 0
print(f"GPU:    {gpu_name}")
print(f"VRAM:   {vram:.0f} GB")
print(f"Model:  {MODEL_NAME} ({NUM_LABELS} classes: {LABEL_NAMES})")
print(f"Batch:  {BATCH_SIZE} × grad_accum={GRAD_ACCUM} = effective {BATCH_SIZE * GRAD_ACCUM}")
print(f"MaxLen: {MAX_LEN}")
print()

DATA_DIR = Path("./training_data")
DATA_DIR.mkdir(exist_ok=True)

# ============================================================
# 1. DATA LOADERS
# ============================================================

def load_phishtank(max_urls: int) -> list[tuple[str, int]]:
    """PhishTank verified phishing URLs → label=1 (phishing)"""
    cache = DATA_DIR / "phishtank.csv"
    urls = []
    if cache.exists():
        with open(cache, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row.get("url", "")
                if url and url.startswith("http"):
                    urls.append((url, LABEL2ID["phishing"]))
                    if len(urls) >= max_urls:
                        break
        print(f"  PhishTank: {len(urls)} URLs (cached)")
        return urls

    print("  PhishTank: downloading...")
    try:
        res = requests.get("http://data.phishtank.com/data/online-valid.csv", timeout=60)
        res.raise_for_status()
        cache.write_bytes(res.content)
        reader = csv.DictReader(io.StringIO(res.text))
        for row in reader:
            u = row.get("url", "")
            if u and u.startswith("http"):
                urls.append((u, LABEL2ID["phishing"]))
                if len(urls) >= max_urls:
                    break
    except Exception as e:
        print(f"  PhishTank failed: {e}")
    return urls


def load_urlhaus(max_urls: int) -> list[tuple[str, int]]:
    """URLhaus malware URLs → label=2 (malware)"""
    cache = DATA_DIR / "urlhaus.csv"
    urls = []
    if cache.exists():
        with open(cache, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                parts = line.split(",")
                if len(parts) >= 3 and parts[2].strip().startswith("http"):
                    urls.append((parts[2].strip().strip('"'), LABEL2ID["malware"]))
                    if len(urls) >= max_urls:
                        break
        print(f"  URLhaus: {len(urls)} URLs (cached)")
        return urls

    print("  URLhaus: downloading...")
    try:
        res = requests.get("https://urlhaus.abuse.ch/downloads/csv_recent/", timeout=60)
        cache.write_bytes(res.content)
        for line in res.text.splitlines():
            if line.startswith("#") or not line.strip():
                continue
            parts = line.split(",")
            if len(parts) >= 3 and parts[2].strip().startswith("http"):
                urls.append((parts[2].strip().strip('"'), LABEL2ID["malware"]))
                if len(urls) >= max_urls:
                    break
    except Exception as e:
        print(f"  URLhaus failed: {e}")
    return urls


def load_tranco(max_urls: int) -> list[tuple[str, int]]:
    """Tranco top domains → label=0 (safe)"""
    cache = DATA_DIR / "tranco.csv"
    urls = []
    if cache.exists():
        with open(cache, "r") as f:
            for line in f:
                if "," in line:
                    domain = line.strip().split(",")[1]
                    urls.append((f"https://{domain}", LABEL2ID["safe"]))
                    if len(urls) >= max_urls:
                        break
        print(f"  Tranco: {len(urls)} URLs (cached)")
        return urls

    print("  Tranco: downloading...")
    try:
        res = requests.get("https://tranco-list.eu/top-1m.csv.zip", timeout=60)
        import zipfile
        with zipfile.ZipFile(io.BytesIO(res.content)) as z:
            with z.open(z.namelist()[0]) as f:
                content = f.read().decode("utf-8")
                cache.write_text(content)
        for line in content.splitlines():
            if "," in line:
                domain = line.split(",")[1]
                urls.append((f"https://{domain}", LABEL2ID["safe"]))
                if len(urls) >= max_urls:
                    break
    except Exception as e:
        print(f"  Tranco failed: {e}. Using fallback.")
        safe_fallback = [
            "google.com", "youtube.com", "facebook.com", "amazon.com", "wikipedia.org",
            "twitter.com", "instagram.com", "linkedin.com", "microsoft.com", "apple.com",
            "github.com", "stackoverflow.com", "netflix.com", "reddit.com", "whatsapp.com",
        ]
        urls = [(f"https://{d}", LABEL2ID["safe"]) for d in safe_fallback]
    return urls


def load_kz_specific() -> list[tuple[str, int]]:
    """Kazakhstan-specific URLs for all classes"""
    data = [
        # Phishing
        ("https://kaspi-login.tk", LABEL2ID["phishing"]),
        ("https://kaspi-verify.ml", LABEL2ID["phishing"]),
        ("https://egov-login.ga", LABEL2ID["phishing"]),
        ("https://halyk-bank.cf", LABEL2ID["phishing"]),
        ("https://kaspi-qr.gq", LABEL2ID["phishing"]),
        ("https://egov-kz.com", LABEL2ID["phishing"]),
        ("https://my-kaspi.xyz", LABEL2ID["phishing"]),
        ("https://kaspi-pay.click", LABEL2ID["phishing"]),
        ("https://egov-verify.top", LABEL2ID["phishing"]),
        ("https://homebank-kz.work", LABEL2ID["phishing"]),
        ("https://sberbank-kz.ru", LABEL2ID["phishing"]),
        ("https://kaspi-bonus.site", LABEL2ID["phishing"]),
        # Pyramid
        ("https://crowd1.com", LABEL2ID["pyramid"]),
        ("https://finiko.com", LABEL2ID["pyramid"]),
        ("https://onecoin.eu", LABEL2ID["pyramid"]),
        ("https://forsage.io", LABEL2ID["pyramid"]),
        ("https://bitconnect.co", LABEL2ID["pyramid"]),
        ("https://qubittech.ai", LABEL2ID["pyramid"]),
        ("https://mmm.ru", LABEL2ID["pyramid"]),
        ("https://cashbery.com", LABEL2ID["pyramid"]),
        # Gambling
        ("https://1xbet.com", LABEL2ID["gambling"]),
        ("https://mostbet.com", LABEL2ID["gambling"]),
        ("https://pin-up.kz", LABEL2ID["gambling"]),
        ("https://melbet.com", LABEL2ID["gambling"]),
        ("https://betmaster.io", LABEL2ID["gambling"]),
        # Safe KZ
        ("https://kaspi.kz", LABEL2ID["safe"]),
        ("https://halykbank.kz", LABEL2ID["safe"]),
        ("https://egov.kz", LABEL2ID["safe"]),
        ("https://kolesa.kz", LABEL2ID["safe"]),
        ("https://krisha.kz", LABEL2ID["safe"]),
        ("https://tengrinews.kz", LABEL2ID["safe"]),
        ("https://nur.kz", LABEL2ID["safe"]),
        ("https://zakon.kz", LABEL2ID["safe"]),
        ("https://jusan.kz", LABEL2ID["safe"]),
        ("https://forte.kz", LABEL2ID["safe"]),
        ("https://bcc.kz", LABEL2ID["safe"]),
        ("https://freedom.kz", LABEL2ID["safe"]),
    ]
    print(f"  KZ-specific: {len(data)} URLs")
    return data


# ============================================================
# 2. LOAD + BALANCE DATASET
# ============================================================
print("Loading datasets...")
phishing_urls = load_phishtank(MAX_URLS_PER_CLASS)
malware_urls = load_urlhaus(MAX_URLS_PER_CLASS)
safe_urls = load_tranco(MAX_URLS_PER_CLASS)
kz_urls = load_kz_specific()

# Separate KZ by class
kz_by_class: dict[int, list] = {}
for url, label in kz_urls:
    kz_by_class.setdefault(label, []).append((url, label))

# Build per-class lists
pyramid_urls = kz_by_class.get(LABEL2ID["pyramid"], [])
gambling_urls = kz_by_class.get(LABEL2ID["gambling"], [])
safe_urls += kz_by_class.get(LABEL2ID["safe"], [])
phishing_urls += kz_by_class.get(LABEL2ID["phishing"], [])

# Balance: smallest class determines max per class
class_counts = [len(safe_urls), len(phishing_urls), len(malware_urls), len(pyramid_urls), len(gambling_urls)]
min_count = max(min(class_counts), 100)  # at least 100 per class
print(f"\nPre-balance counts: {dict(zip(LABEL_NAMES, class_counts))}")
print(f"Balancing to: {min_count} per class")

all_urls = (
    safe_urls[:min_count] +
    phishing_urls[:min_count] +
    malware_urls[:min_count] +
    pyramid_urls[:min(min_count, len(pyramid_urls))] +
    gambling_urls[:min(min_count, len(gambling_urls))]
)

urls = [u for u, _ in all_urls]
labels = [l for _, l in all_urls]

print(f"Total dataset: {len(urls)} URLs")
print()

# ============================================================
# 3. TRAIN / TEST SPLIT + TOKENIZE
# ============================================================
train_urls, test_urls, train_labels, test_labels = train_test_split(
    urls, labels, test_size=0.15, random_state=42, stratify=labels
)
print(f"Train: {len(train_urls)}, Test: {len(test_urls)}")

print("Loading tokenizer...")
tokenizer = XLMRobertaTokenizer.from_pretrained(MODEL_NAME)


class URLDataset(Dataset):
    def __init__(self, urls, labels, tokenizer, max_len):
        self.encodings = tokenizer(
            urls, max_length=max_len, padding=True,
            truncation=True, return_tensors="pt"
        )
        self.labels = torch.tensor(labels, dtype=torch.long)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return {
            "input_ids": self.encodings["input_ids"][idx],
            "attention_mask": self.encodings["attention_mask"][idx],
            "labels": self.labels[idx],
        }


print("Tokenizing...")
train_dataset = URLDataset(train_urls, train_labels, tokenizer, MAX_LEN)
test_dataset = URLDataset(test_urls, test_labels, tokenizer, MAX_LEN)

# ============================================================
# 4. MODEL
# ============================================================
print("Loading model...")
model = XLMRobertaForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=NUM_LABELS,
    id2label=ID2LABEL,
    label2id=LABEL2ID,
)

total_steps = math.ceil(len(train_dataset) / (BATCH_SIZE * GRAD_ACCUM)) * EPOCHS

training_args = TrainingArguments(
    output_dir="./training_output",
    num_train_epochs=EPOCHS,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE * 2,
    gradient_accumulation_steps=GRAD_ACCUM,
    learning_rate=LR,
    weight_decay=WEIGHT_DECAY,
    warmup_ratio=WARMUP_RATIO,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="f1_macro",
    logging_steps=50,
    fp16=torch.cuda.is_available(),
    gradient_checkpointing=True,       # saves VRAM for large model
    dataloader_num_workers=4,
    report_to="none",
    save_total_limit=2,
)


def compute_metrics(pred):
    preds = np.argmax(pred.predictions, axis=1)
    labels = pred.label_ids
    return {
        "accuracy": accuracy_score(labels, preds),
        "f1_macro": f1_score(labels, preds, average="macro"),
        "f1_weighted": f1_score(labels, preds, average="weighted"),
        "precision_macro": precision_score(labels, preds, average="macro", zero_division=0),
        "recall_macro": recall_score(labels, preds, average="macro", zero_division=0),
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

# ============================================================
# 5. TRAIN
# ============================================================
print()
print("=" * 60)
print("TRAINING")
print("=" * 60)
start_time = time.time()
trainer.train()
train_time = time.time() - start_time
print(f"\nTraining done in {train_time / 60:.1f} min")

# ============================================================
# 6. EVALUATE
# ============================================================
print()
print("=" * 60)
print("EVALUATION")
print("=" * 60)
results = trainer.evaluate()
for k, v in results.items():
    if isinstance(v, float):
        print(f"  {k}: {v:.4f}")

preds_out = trainer.predict(test_dataset)
pred_labels = np.argmax(preds_out.predictions, axis=1)

print("\nClassification Report:")
print(classification_report(test_labels, pred_labels, target_names=LABEL_NAMES))

cm = confusion_matrix(test_labels, pred_labels)
print("Confusion Matrix:")
print(cm)

# ============================================================
# 7. SAVE
# ============================================================
os.makedirs(OUTPUT_DIR, exist_ok=True)
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

metrics = {
    "model": MODEL_NAME,
    "num_labels": NUM_LABELS,
    "label_names": LABEL_NAMES,
    "accuracy": results.get("eval_accuracy", 0),
    "f1_macro": results.get("eval_f1_macro", 0),
    "f1_weighted": results.get("eval_f1_weighted", 0),
    "precision_macro": results.get("eval_precision_macro", 0),
    "recall_macro": results.get("eval_recall_macro", 0),
    "mcc": results.get("eval_mcc", 0),
    "train_samples": len(train_urls),
    "test_samples": len(test_urls),
    "max_len": MAX_LEN,
    "batch_size": BATCH_SIZE,
    "grad_accum": GRAD_ACCUM,
    "epochs": EPOCHS,
    "training_time_minutes": round(train_time / 60, 1),
    "gpu": gpu_name,
}
with open(os.path.join(OUTPUT_DIR, "training_metrics.json"), "w") as f:
    json.dump(metrics, f, indent=2)

# Save to Google Drive (Colab)
try:
    import shutil
    if os.path.exists("/content/drive"):
        shutil.copytree(OUTPUT_DIR, DRIVE_SAVE_DIR, dirs_exist_ok=True)
        print(f"\nSaved to Google Drive: {DRIVE_SAVE_DIR}")
except Exception as e:
    print(f"Drive save skipped: {e}")

print()
print("=" * 60)
print("DONE")
print("=" * 60)
print(f"  Model:      {OUTPUT_DIR}/")
print(f"  Accuracy:   {metrics['accuracy']:.4f}")
print(f"  F1 macro:   {metrics['f1_macro']:.4f}")
print(f"  MCC:        {metrics['mcc']:.4f}")
print(f"  Train time: {metrics['training_time_minutes']} min")
print()
print("Next: copy qalqan_model_v2/ to api/ml/ and update serve_model.py")
