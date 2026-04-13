# Qalqan AI — ML Model (XLM-RoBERTa)

## Quick Start

```bash
cd ml/

# 1. Install dependencies
pip install -r requirements.txt

# 2. Train model (~20 min on RTX 3070 Ti)
python train_model.py

# 3. Start local API
python serve_model.py
# → http://localhost:8001
```

## API Endpoints

```bash
# Health check
curl http://localhost:8001/

# Single URL prediction (<50ms)
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://kaspi-login.tk"}'

# Batch prediction
curl -X POST http://localhost:8001/batch \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://google.com", "https://crowd1.com"]}'
```

## Files After Training

```
qalqan_model/
├── model.safetensors      (~1.1GB)
├── config.json
├── tokenizer.json
├── special_tokens_map.json
├── sentencepiece.bpe.model
└── training_metrics.json
```
