\# 🔐 LLM Security Fine-tuning \& Classifier



\[!\[Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

\[!\[Groq](https://img.shields.io/badge/LLM-Groq-orange.svg)](https://groq.com/)

\[!\[Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)

\[!\[PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)

\[!\[Hugging Face](https://img.shields.io/badge/🤗-Transformers-yellow.svg)](https://huggingface.co/)



\## 📋 Overview



A \*\*production-ready security alert classifier\*\* that demonstrates two approaches:



1\. \*\*Groq API-based classification\*\* (instant, no training)

2\. \*\*Fine-tuned TinyLlama 1.1B\*\* using LoRA/PEFT (custom training)



The system classifies security alerts with:

\- ✅ Severity (LOW/MEDIUM/HIGH/CRITICAL)

\- ✅ Threat type (Brute Force, SQL Injection, Malware, etc.)

\- ✅ Recommended actions

\- ✅ Explanation of the threat



\## 🎯 Key Features



| Feature | Technology | Description |

|---------|------------|-------------|

| \*\*Real-time Classification\*\* | Groq Llama 3.1 | Instant security alert classification |

| \*\*Fine-tuning Pipeline\*\* | LoRA + PEFT + 4-bit | Custom training on security data |

| \*\*REST API\*\* | Flask | Easy integration with security tools |

| \*\*Structured Output\*\* | JSON | Severity, threat type, recommendations |



\## 🏗️ Architecture



┌─────────────────────────────────────────────────────────────┐

│ SECURITY ALERT │

│ "Failed login attempt from IP 203.0.113.45 - 5 attempts" │

└─────────────────────┬───────────────────────────────────────┘

↓

┌─────────────────────────────────────────────────────────────┐

│ CLASSIFICATION API │

│ POST /classify │

│ ↓ │

│ ┌────────────┴────────────┐ │

│ ↓ ↓ │

│ Groq Llama 3.1 Fine-tuned TinyLlama │

│ (No training) (LoRA/PEFT) │

│ ↓ ↓ │

│ └────────────┬────────────┘ │

│ ↓ │

│ Structured Response │

│ { │

│ "severity": "MEDIUM", │

│ "threat\_type": "Brute Force", │

│ "recommendation": "Block IP after 10 attempts" │

│ } │

└─────────────────────────────────────────────────────────────┘





\## 🔧 Tech Stack



| Component | Technology |

|-----------|------------|

| \*\*Backend\*\* | Python 3.11, Flask |

| \*\*LLM (Primary)\*\* | Groq Llama 3.1 8B |

| \*\*Fine-tuned Model\*\* | TinyLlama 1.1B |

| \*\*Fine-tuning\*\* | LoRA, PEFT, 4-bit Quantization |

| \*\*Training Framework\*\* | PyTorch, Transformers, PEFT |

| \*\*API\*\* | Flask, REST |



\## 📦 Installation



\### Local Development



```bash

\# Clone repository

git clone https://github.com/Aikaksh-Singh-Routela/llm-security-finetuning.git

cd llm-security-finetuning



\# Create virtual environment

python -m venv venv

source venv/bin/activate  # Linux/Mac

\# or

.\\venv\\Scripts\\activate  # Windows



\# Install dependencies

pip install -r requirements.txt



\# Set API key

export OPENAI\_API\_KEY="your-groq-api-key"  # Linux/Mac

\# or

$env:OPENAI\_API\_KEY="your-groq-api-key"  # Windows



\# Run the API

python groq\_security\_api.py





