# groq_security_api.py - Security classification using Groq (no training needed!)
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

# Initialize Groq
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("⚠️ OPENAI_API_KEY not set!")
    exit(1)

client = Groq(api_key=api_key)

# Security classification prompt template
SYSTEM_PROMPT = """You are a cybersecurity threat classifier. Classify security alerts with:
- SEVERITY: LOW, MEDIUM, HIGH, or CRITICAL
- THREAT_TYPE: (e.g., Brute Force, SQL Injection, Malware, Data Exfiltration, Reconnaissance, etc.)
- RECOMMENDATION: Brief action to take

Respond in JSON format:
{"severity": "...", "threat_type": "...", "recommendation": "...", "explanation": "..."}"""

def classify_alert(alert_text):
    """Classify security alert using Groq"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Classify this security alert: {alert_text}"}
        ],
        temperature=0.1,
        max_tokens=200
    )
    
    result = response.choices[0].message.content
    # Try to parse JSON, fallback to text
    try:
        import json
        return json.loads(result)
    except:
        return {"response": result}

@app.route('/classify', methods=['POST'])
def classify():
    data = request.json
    alert = data.get('alert', '')
    if not alert:
        return jsonify({'error': 'No alert provided'}), 400
    
    result = classify_alert(alert)
    return jsonify({
        'alert': alert,
        'classification': result
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model': 'Groq Llama 3.1'})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🔐 SECURITY CLASSIFIER API (Groq - No Training!)")
    print("="*60)
    app.run(host='0.0.0.0', port=8082, debug=False)