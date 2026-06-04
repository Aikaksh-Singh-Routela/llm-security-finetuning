# 🔐 LLM Security Fine-tuning & Classifier

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Groq](https://img.shields.io/badge/LLM-Groq-orange.svg)](https://groq.com/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![Hugging Face](https://img.shields.io/badge/🤗-Transformers-yellow.svg)](https://huggingface.co/)

## 📋 Overview

A **production-ready security alert classifier** that demonstrates two approaches:

1. **Groq API-based classification** (instant, no training)
2. **Fine-tuned TinyLlama 1.1B** using LoRA/PEFT (custom training)

The system classifies security alerts with:
- ✅ Severity (LOW/MEDIUM/HIGH/CRITICAL)
- ✅ Threat type (Brute Force, SQL Injection, Malware, etc.)
- ✅ Recommended actions
- ✅ Explanation of the threat

## 🎯 Key Features

| Feature | Technology | Description |
|---------|------------|-------------|
| **Real-time Classification** | Groq Llama 3.1 | Instant security alert classification |
| **Fine-tuning Pipeline** | LoRA + PEFT + 4-bit | Custom training on security data |
| **REST API** | Flask | Easy integration with security tools |
| **Structured Output** | JSON | Severity, threat type, recommendations |

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Aikaksh-Singh-Routela/llm-security-finetuning.git
cd llm-security-finetuning

# Install dependencies
pip install -r requirements.txt

# Set your API key
export OPENAI_API_KEY="your-groq-api-key"

# Run the API
python groq_security_api.py

# Classify a security alert
curl -X POST http://localhost:8082/classify \
  -H "Content-Type: application/json" \
  -d '{"alert": "Failed login attempt from IP 203.0.113.45 - 5 attempts in 30 seconds"}'

{
  "severity": "MEDIUM",
  "threat_type": "Brute Force Attack",
  "recommendation": "Block IP after 10 failed attempts",
  "explanation": "Multiple failed logins indicate automated brute force"
}






