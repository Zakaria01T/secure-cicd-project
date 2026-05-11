from flask import Flask
import subprocess
import hashlib

app = Flask(__name__)

@app.route('/')
def home():
    return {"message": "Hello from Secure CI/CD Project!", "version": "1.0"}

@app.route('/health')
def health():
    return {"status": "healthy"}

# ⚠️ INTENTIONAL VULNERABILITY 1 — Hardcoded secret
SECRET_KEY = "hardcoded-secret-123"

# ⚠️ INTENTIONAL VULNERABILITY 2 — Weak hash algorithm
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

if __name__ == '__main__':
    # ⚠️ INTENTIONAL VULNERABILITY 3 — Debug mode on
    app.run(host='0.0.0.0', port=5000, debug=True)