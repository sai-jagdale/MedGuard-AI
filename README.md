# 🛡️ MedGuard AI: Real-Time Counterfeit & Expired Medicine Detection

## 💡 Overview

MedGuard AI is an intelligent, **Django-based web application** designed to combat the severe challenge of counterfeit and substandard drugs. It provides a fast, reliable, and multi-modal solution for **real-time drug authentication** directly at the point of care

The system uses an **Agentic AI Workflow** to verify medicine authenticity and automatically check for expiry, empowering consumers and healthcare professionals to make informed, instantaneous decisions

---

## ✨ Key Features

### 1. Tri-Input Verification System 
Users can verify a drug using three flexible input modes:
* **Text Search** (Entering the medicine name)
* **Image Upload** (Uploading a photo of the medicine package) 
* **Barcode/QR Code Scan** (Enabling rapid product identifier retrieval)

### 2. Agentic AI Workflow 
The system is built on specialized, cooperating AI agents orchestrated by the **Intake Agent** (`views.py`)
* **OCR Agent**: Uses **Google Cloud Vision API** to accurately extract text from complex packaging.
* **Barcode Agent**: Decodes 1D/2D barcodes/QR codes and cross-verifies identifiers with `MajorProjectDataset.csv` for authenticity
* **Extraction Agent**: Uses **Regular Expressions (Regex)** to isolate key data: MFG Date, EXP Date, and Price (MRP)
* **Search Agent**: Employs **TheFuzz** library for fuzzy string matching, handling spelling or OCR errors
* **Summary Agent**: Uses a **Local LLM (Ollama - phi-3)** to generate a concise, structured summary (8-point or 5-point) of the verified data

### 3. Automated Safety Check 
* The system automatically compares the extracted Expiry Date against the current date
* If expired, a clear **"⚠️ EXPIRED MEDICINE"** warning is issued

### 4. Multi-User Platform 
* Includes secure **login** and **signup**.
* Offers **personalized search history** management, allowing users to revisit or delete past verifications

---

## 💻 Technologies Used

| Category | Technology | Purpose / Library |
| :--- | :--- | :--- |
| **Backend** | Django Framework (Python 3.10+) | Multi-user web application foundation |
| **OCR / Vision** | Google Vision API | Image-based text detection  |
| **Barcode** | Pyzbar / OpenCV | Decoding 1D/2D Barcodes and QR Codes  |
| **LLM / AI** | Ollama (phi-3-mini) | Local LLM for summary generation and RAG core  |
| **Fuzzy Matching** | TheFuzz | Handling spelling errors and variations  |
| **Data Processing** | Pandas, NumPy, Regex | Data extraction, matching, and manipulation  |
| **Database** | SQLite3 / PostgreSQL | Data storage and history tracking  |
| **Frontend** | HTML, CSS, JavaScript, Bootstrap | User Interface design |

---

## Project File Structure

## 🌳 Project Structure

This project follows a standard Django structure, organized around the main project folder (`medguard_project`) and the primary application (`medicinebot`). The Agentic AI workflow logic is contained within the `medicinebot/agents/` directory.
MEDGUARD_AI/ ├── medguard_project/ # Main Django Project Configuration │ ├── init.py │ ├── asgi.py │ ├── settings.py │ ├── urls.py │ └── wsgi.py ├── medicinebot/ # Primary Django Application (The core logic) │ ├── agents/ # Agentic AI Workflow Implementation │ │ ├── barcode_agent.py # Decodes and verifies barcodes/QR codes │ │ ├── extraction_agent.py # Regex for MFG, EXP, and Price data │ │ ├── ocr_agent.py # Google Cloud Vision API integration │ │ ├── search_agent.py # TheFuzz fuzzy matching logic │ │ └── summary_agent.py # Ollama LLM summarization logic │ ├── management/ │ │ └── commands/ │ ├── migrations/ │ ├── static/ │ │ └── medicinebot/ │ │ └── images/ │ │ └── logo.png │ ├── templates/ │ │ └── medicinebot/ │ │ ├── account-history.html │ │ ├── base.html │ │ ├── home.html # Tri-input interface │ │ ├── login.html │ │ └── signup.html │ ├── admin.py │ ├── apps.py │ ├── forms.py │ ├── models.py # Database schemas (e.g., Search History, User) │ ├── tests.py │ ├── urls.py │ └── views.py # Intake Agent (The Orchestrator) ├── ScreenShots/ # Project output and testing screenshots ├── .gitattributes ├── .gitignore ├── gcloud_key.json # Google Cloud Vision API Credentials ├── MajorProjectDataset.csv # Local knowledge base for verification ├── db.sqlite3 # Local Development Database ├── manage.py # Django Command Utility ├── requirements.txt # Python Dependencies └── venv/ # Python Virtual Environment
