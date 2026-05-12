# 🔐 Secure CI/CD Pipeline with DevSecOps

![Pipeline Status](https://github.com/Zakaria01T/secure-cicd-project/actions/workflows/cicd.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![Security](https://img.shields.io/badge/Security-DevSecOps-red?logo=shield)
![License](https://img.shields.io/badge/License-MIT-green)

> A production-grade secure CI/CD pipeline implementing **DevSecOps** practices with **Shift-Left Security** methodology. Every code push automatically triggers a full security scanning suite before deployment.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Security Tools](#-security-tools)
- [Pipeline Flow](#-pipeline-flow)
- [SDLC Methodologies](#-sdlc-methodologies)
- [Shift-Left Security](#-shift-left-security)
- [Project Structure](#-project-structure)
- [How to Run Locally](#-how-to-run-locally)
- [Run with Docker](#-run-with-docker)
- [Pipeline Results](#-pipeline-results)
- [Key Concepts](#-key-concepts-demonstrated)
- [Author](#-author)

---

## 🎯 Overview

This project demonstrates the implementation of a **secure CI/CD pipeline** that integrates security at every stage of the software development lifecycle. Rather than treating security as an afterthought, this pipeline enforces security checks automatically on every commit — a practice known as **Shift-Left Security**.

### What makes this project special?

- 🔄 **Fully automated** — every push triggers 5 jobs automatically
- 🛡️ **4 security layers** — SAST, Secret Scanning, SCA, and DAST
- ⚡ **Parallel execution** — security jobs run simultaneously to save time
- ❌ **Fail-fast** — pipeline stops immediately on critical findings
- 📊 **Detailed reports** — every scan generates a downloadable artifact

---

## 🏗️ Architecture

```
Developer Push / Pull Request
            │
            ▼
┌───────────────────────────────────────────┐
│              GitHub Actions               │
│                                           │
│  ┌─────────────────────────────────────┐  │
│  │         JOB 1: Build & Test         │  │
│  │  ✅ Install Python dependencies     │  │
│  │  ✅ Run pytest unit tests           │  │
│  │  ✅ Build Docker image              │  │
│  └──────────────┬──────────────────────┘  │
│                 │ (only if Job 1 passes)   │
│        ┌────────┼────────┐                │
│        ▼        ▼        ▼                │
│  ┌──────────┐ ┌───────┐ ┌──────────────┐  │
│  │  JOB 2   │ │ JOB 3 │ │    JOB 4     │  │
│  │  SAST    │ │Secrets│ │    SCA       │  │
│  │ (Bandit) │ │(Truff)│ │  (Safety)    │  │
│  └──────────┘ └───────┘ └──────────────┘  │
│        │        │              │           │
│        └────────┴──────────────┘           │
│                 │ (all 3 must pass)        │
│                 ▼                          │
│  ┌─────────────────────────────────────┐  │
│  │       JOB 5: DAST - OWASP ZAP      │  │
│  │  🔥 Starts Flask app               │  │
│  │  🔥 Attacks running application    │  │
│  │  🔥 Generates HTML security report │  │
│  └─────────────────────────────────────┘  │
│                 │                          │
└─────────────────┼──────────────────────────┘
                  ▼
        ✅ Code is Safe to Deploy
```

---

## 🛡️ Security Tools

| Tool | Type | What it Scans | Blocks Pipeline? |
|------|------|---------------|-----------------|
| **Bandit** | SAST | Python source code for security anti-patterns | ✅ On HIGH severity |
| **Trufflehog** | Secret Scanning | Entire Git history for leaked credentials & API keys | ✅ On verified secrets |
| **Safety** | SCA | Python dependencies for known CVEs | ⚠️ Reports findings |
| **OWASP ZAP** | DAST | Running application via simulated attacks | ⚠️ Configurable via rules |

### What Each Tool Finds

#### 🔍 Bandit (SAST)
- Hardcoded passwords and secrets
- Use of weak cryptographic algorithms (MD5, SHA1)
- Debug mode enabled in production
- SQL injection vulnerabilities
- Use of dangerous functions (`eval`, `exec`)

#### 🔑 Trufflehog (Secret Scanning)
- AWS Access Keys & Secret Keys
- GitHub tokens & API keys
- Database connection strings
- Private SSH keys
- Any pattern matching known secret formats

#### 📦 Safety (SCA)
- Known CVEs in installed packages
- Outdated dependencies with security patches
- License compliance issues
- Supply chain vulnerabilities

#### 🔥 OWASP ZAP (DAST)
- Cross-Site Scripting (XSS)
- SQL Injection at runtime
- Security header misconfigurations
- Authentication bypass vulnerabilities
- Sensitive data exposure

---

## 🔄 Pipeline Flow

```
⏱️  Timeline of a typical pipeline run:

0:00  ──► Job 1 starts (Build & Test)
0:44  ──► Job 1 passes ✅
0:44  ──► Job 2 (SAST) starts      ─┐
0:44  ──► Job 3 (Secrets) starts    ├── Run in PARALLEL
0:44  ──► Job 4 (SCA) starts       ─┘
1:01  ──► Job 3 passes ✅ (9s)
1:02  ──► Job 2 passes ✅ (17s)
1:13  ──► Job 4 passes ✅ (29s)
1:13  ──► Job 5 (DAST) starts
4:57  ──► Job 5 passes ✅
         ────────────────────
         Total: ~5 minutes for full security scan
```

---

## 🔄 SDLC Methodologies Applied

### 🌊 Waterfall
Clear sequential phases where each must complete before the next begins:
```
Plan → Design → Code → Security Scan → Test → Deploy
```
The pipeline enforces this order — code cannot deploy without passing all security gates.

### 🔁 Agile
- Security integrated into every sprint cycle
- Fast feedback loop via automated pipeline (~5 min total)
- Iterative improvement of security rules in `.zap/rules.tsv`
- PR-based workflow enables continuous code review

### 🌀 Spiral
- Risk-driven approach — highest risk scanned first
- SAST & Secret scanning run before the expensive DAST
- Continuous risk assessment at each pipeline stage
- Each iteration adds more security coverage

---

## ⬅️ Shift-Left Security

### Traditional Approach (Security at the End)
```
Code ──► Build ──► Test ──► Deploy ──► [Security] ──► Fix
                                           ↑
                              Too late! Bug is in production
                              Fixing costs 100x more here
```

### This Project (Shift-Left)
```
[Security] ──► Code ──► Build ──► Test ──► Deploy
     ↑
Security checked at EVERY commit
Bugs caught when they are cheapest to fix
```

**Cost of fixing a bug by phase:**

| Phase | Relative Cost |
|-------|--------------|
| Development (our approach) | 1x |
| Testing | 10x |
| Production | 100x |

---

## 📁 Project Structure

```
secure-cicd-project/
│
├── .github/
│   └── workflows/
│       └── cicd.yml          # 🔧 Full pipeline definition (5 jobs)
│
├── .zap/
│   └── rules.tsv             # ⚙️  OWASP ZAP scan configuration
│                             #     Controls which alerts FAIL/WARN/IGNORE
│
├── app.py                    # 🐍 Flask web application
├── test_app.py               # 🧪 pytest unit tests
├── requirements.txt          # 📦 Python dependencies
├── Dockerfile                # 🐳 Container definition
└── README.md                 # 📖 This file
```

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.9+
- Docker Desktop
- Git

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/Zakaria01T/secure-cicd-project.git
cd secure-cicd-project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run unit tests
pytest test_app.py -v

# 4. Start the application
python app.py
```

The app will be available at `http://localhost:5000`

### API Endpoints

| Endpoint | Method | Response |
|----------|--------|----------|
| `/` | GET | `{"message": "Hello from Secure CI/CD Project!", "version": "1.0"}` |
| `/health` | GET | `{"status": "healthy"}` |

### Run Security Scans Locally

```bash
# SAST - Scan for code vulnerabilities
pip install bandit
bandit -r . --severity-level high

# SCA - Check dependencies for CVEs
pip install safety
safety check -r requirements.txt

# Secret Scanning (requires Docker)
docker run --rm -v "$PWD:/pwd" \
  trufflesecurity/trufflehog:latest \
  filesystem /pwd --only-verified
```

---

## 🐳 Run with Docker

```bash
# Build the Docker image
docker build -t secure-cicd-project:latest .

# Run the container
docker run -p 5000:5000 secure-cicd-project:latest

# Test the running container
curl http://localhost:5000/health
# Expected: {"status": "healthy"}

# Run with environment variables (secure approach)
docker run -p 5000:5000 \
  -e SECRET_KEY=your-secret-key \
  -e DEBUG=False \
  secure-cicd-project:latest
```

---

## 📊 Pipeline Results

| Job | Tool | Duration | Status |
|-----|------|----------|--------|
| Build & Test | pytest + Docker | ~44s | ✅ Passing |
| SAST | Bandit | ~17s | ✅ No High Severity Issues |
| Secret Scanning | Trufflehog | ~9s | ✅ No Verified Secrets Found |
| SCA | Safety | ~29s | ✅ No Critical CVEs |
| DAST | OWASP ZAP | ~3m 44s | ✅ Baseline Scan Passed |

### Downloadable Security Reports

Every pipeline run generates 3 downloadable security reports:
- 📄 `bandit-security-report.json` — SAST findings
- 📄 `safety-dependency-report.json` — Dependency CVEs
- 📄 `zap-security-report.html` — DAST attack results

---

## 💡 Key Concepts Demonstrated

### 🔐 Defense in Depth
Multiple independent security layers — if one tool misses something, another catches it:
```
SAST catches bad code patterns
    + Secret scanning catches leaked credentials
        + SCA catches vulnerable dependencies
            + DAST catches runtime vulnerabilities
= Comprehensive security coverage ✅
```

### ⚡ Fail Fast
```yaml
needs: build-and-test  # Job only runs if previous job passes
```
Pipeline stops at the first critical issue — no wasted time scanning code that doesn't even build.

### 🔀 Parallel Execution
Jobs 2, 3, and 4 run simultaneously — cutting total scan time by ~60% compared to sequential execution.

### 🎯 Principle of Least Privilege
```yaml
permissions:
  contents: read        # Only read access to code
  issues: write         # Only ZAP job needs this
  security-events: write
```

### 📋 Security as Code
All security rules, configurations, and thresholds are version-controlled alongside the application code — fully auditable and reproducible.

---

## 🔧 Configuration

### ZAP Rules (`.zap/rules.tsv`)

```tsv
# Format: RULE_ID   ACTION   DESCRIPTION
10015   IGNORE   (Incomplete Cache-control Header)
10096   IGNORE   (Timestamp Disclosure)
10036   IGNORE   (Server Leaks Version Information)
```

Actions: `FAIL` = breaks pipeline | `WARN` = reports only | `IGNORE` = silent

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `default-dev-key` | Application secret key |
| `DEBUG` | `False` | Enable debug mode |

---

## 👤 Author

**Zakaria** — DevSecOps Enthusiast

[![GitHub](https://img.shields.io/badge/GitHub-Zakaria01T-181717?logo=github)](https://github.com/Zakaria01T)



---

*Built with ❤️ and secured with 🔐*