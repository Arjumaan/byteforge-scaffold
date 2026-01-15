# ByteForge Scaffold

**Enterprise-Grade Automated Penetration Testing Framework**

ByteForge is a comprehensive security suite designed for automated reconnaissance, vulnerability scanning, and reporting. It operates in two modes: a high-performance **CLI** for direct terminal usage and a modern **Web Dashboard** for managing campaigns and visualization.

---

## 🚀 Features

### 🛡️ Core Security Capabilities

- **Full Spectrum Scanning**: One-click execution of the entire kill chain (Recon $\rightarrow$ Crawl $\rightarrow$ Vulnerability Analysis).
- **Reconnaissance**: Automated subdomain enumeration using **Subfinder**.
- **Spidering/Crawling**: Deep web crawling to map assets and endpoints using **Katana**.
- **Vulnerability Scanning**: CVE and vulnerability detection using **Nuclei** templates.
- **Active Scanning**: Custom payload injection logic for detecting critical flaws (SQLi, XSS).

### 🖥️ CLI Tool (`byteforge`)

- "Bash-style" cyber security tool.
- Instant scan execution (e.g., `byteforge scan -t example.com`).
- Manage targets and view reports directly from the terminal.
- Supports Windows (`.bat`) and Linux/Mac.

### 🌐 Web Dashboard

- **Targets Management**: Add and organize scopes securely.
- **Live Job Terminal**: Monitor scans in real-time.
- **Network Map**: Visual topology of discovered assets.
- **Findings & Remediation**: AI-assisted remediation suggestions.
- **Dark/Light Mode**: Beautiful, professional UI.

---

## 🛠️ Installation & Setup

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **Go** (required for Nuclei/Subfinder/Katana engine integration)

### One-Click Setup (Windows)

```powershell
.\install_system.bat
```

This script will:

1. Set up the Python backend environment.
2. Install all Python dependencies (`FastAPI`, `SQLAlchemy`, etc.).
3. Install Frontend dependencies (`React`, `Vite`).
4. Configure the SQLite database.

---

## 🎮 Usage

### Option 1: Web Interface

Start the backend and frontend servers:

```powershell
.\run_system.bat
```

- **Dashboard**: Open [http://localhost:5173](http://localhost:5173) in your browser.
- **Workflow**: Go to `Targets` $\rightarrow$ Click **Full Scan**.

### Option 2: Command Line Interface (CLI)

Use the wrapper script for instant access:

**Scan a Target:**

```powershell
.\byteforge.bat scan -t example.com --type full_scan
```

**List Targets:**

```powershell
.\byteforge.bat targets
```

**View Help:**

```powershell
.\byteforge.bat -h
```

---

## 📂 Project Structure

```
ByteForge-Scaffold/
├── backend/                # Python FastAPI Backend
│   ├── app/                # Core Application Logic
│   │   ├── services/       # Security Engines (Nuclei, Recon, Crawl)
│   │   ├── routers/        # API Endpoints
│   │   └── models.py       # Database Schemas (Encrypted)
│   ├── byteforge.db        # Local Database (Ignored in Git)
│   └── worker.py           # Task Runner (Threaded/Celery)
├── frontend/               # React TypeScript Frontend
│   ├── src/                # UI Components & Pages
│   └── public/             # Static Assets
├── byteforge.py            # CLI Tool Entry Point
├── byteforge.bat           # Windows CLI Wrapper
├── install_system.bat      # Installer Script
└── run_system.bat          # Launcher Script
```

---

## 🔒 Security & License

**Proprietary Software**
Copyright (c) 2026 Arjumaan.M. All Rights Reserved.

This software is the confidential and proprietary information of Arjumaan.M. Unauthorized reproduction, distribution, or use is strictly prohibited.

---
*Built with ❤️ by ByteForge Team for Advanced Security Testing.*
