from flask import Flask
import hashlib
import os

app = Flask(__name__)

@app.route('/')
def home():
    return {"message": "Hello from Secure CI/CD Project!", "version": "1.0"}

@app.route('/health')
def health():
    return {"status": "healthy"}

# ✅ FIX 1 — Use environment variable instead of hardcoded secret
SECRET_KEY = os.environ.get("SECRET_KEY", "default-dev-key")

# ✅ FIX 2 — Use strong hash instead of MD5
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

if __name__ == '__main__':
    # ✅ FIX 3 — Debug mode from environment variable
    debug_mode = os.environ.get("DEBUG", "False") == "True"
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)