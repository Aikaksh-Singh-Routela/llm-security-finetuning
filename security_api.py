# security_api.py - API for fine-tuned security model
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch
import os

app = Flask(__name__)
CORS(app)

print("🚀 Loading fine-tuned security model...")

# Load base model and adapter
MODEL_PATH = "./security-llm-final"
device = "cuda" if torch.cuda.is_available() else "cpu"

try:
    model = AutoModelForCausalLM.from_pretrained(
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        torch_dtype=torch.float16,
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    
    # Load fine-tuned adapter
    model = PeftModel.from_pretrained(model, MODEL_PATH)
    print("✅ Fine-tuned model loaded!")
except Exception as e:
    print(f"⚠️ Model not found, using fallback: {e}")
    model = None
    tokenizer = None

def classify_alert(input_text):
    """Classify security alert using fine-tuned model"""
    if model is None:
        # Fallback logic
        if "failed login" in input_text.lower():
            return "MEDIUM - Possible brute force"
        elif "sql injection" in input_text.lower():
            return "HIGH - SQL injection attempt"
        elif "malware" in input_text.lower():
            return "CRITICAL - Malware detected"
        elif "port scan" in input_text.lower():
            return "MEDIUM - Network reconnaissance"
        else:
            return "LOW - Routine activity"
    
    prompt = f"""### Instruction: Classify this security alert

### Input: {input_text}

### Output:"""
    
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=50,
        temperature=0.1,
        do_sample=True,
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Extract only the output part
    if "### Output:" in response:
        response = response.split("### Output:")[-1].strip()
    return response

@app.route('/classify', methods=['POST'])
def classify():
    data = request.json
    alert = data.get('alert', '')
    if not alert:
        return jsonify({'error': 'No alert provided'}), 400
    
    classification = classify_alert(alert)
    return jsonify({
        'alert': alert,
        'classification': classification
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🔐 SECURITY LLM API READY")
    print("="*60)
    app.run(host='0.0.0.0', port=8082, debug=False)