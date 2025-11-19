# 🛡️ MedGuard AI: Real-Time Counterfeit & Expired Medicine Detection

## 💡 Overview

[cite_start]MedGuard AI is an intelligent, **Django-based web application** designed to combat the severe challenge of counterfeit and substandard drugs[cite: 95, 138, 145]. [cite_start]It provides a fast, reliable, and multi-modal solution for **real-time drug authentication** directly at the point of care[cite: 96, 145].

[cite_start]The system uses an **Agentic AI Workflow** to verify medicine authenticity and automatically check for expiry, empowering consumers and healthcare professionals to make informed, instantaneous decisions[cite: 98, 104, 150].

---

## ✨ Key Features

### [cite_start]1. Tri-Input Verification System [cite: 146, 161]
Users can verify a drug using three flexible input modes:
* [cite_start]**Text Search** (Entering the medicine name) [cite: 147]
* [cite_start]**Image Upload** (Uploading a photo of the medicine package) [cite: 97, 148]
* [cite_start]**Barcode/QR Code Scan** (Enabling rapid product identifier retrieval) [cite: 97, 149]

### [cite_start]2. Agentic AI Workflow [cite: 98, 160, 170]
[cite_start]The system is built on specialized, cooperating AI agents orchestrated by the **Intake Agent** (`views.py`)[cite: 150, 151, 175]:
* [cite_start]**OCR Agent**: Uses **Google Cloud Vision API** to accurately extract text from complex packaging[cite: 99, 152, 196].
* [cite_start]**Barcode Agent**: Decodes 1D/2D barcodes/QR codes and cross-verifies identifiers with `MajorProjectDataset.csv` for authenticity[cite: 99, 153, 199].
* [cite_start]**Extraction Agent**: Uses **Regular Expressions (Regex)** to isolate key data: MFG Date, EXP Date, and Price (MRP)[cite: 100, 154, 200].
* [cite_start]**Search Agent**: Employs **TheFuzz** library for fuzzy string matching, handling spelling or OCR errors[cite: 101, 155, 212, 213].
* [cite_start]**Summary Agent**: Uses a **Local LLM (Ollama - phi-3)** to generate a concise, structured summary (8-point or 5-point) of the verified data[cite: 102, 156, 215].

### [cite_start]3. Automated Safety Check [cite: 100, 165]
* [cite_start]The system automatically compares the extracted Expiry Date against the current date[cite: 202].
* [cite_start]If expired, a clear **"⚠️ EXPIRED MEDICINE"** warning is issued[cite: 154, 203].

### [cite_start]4. Multi-User Platform [cite: 157, 167]
* Includes secure **login** and **signup**.
* [cite_start]Offers **personalized search history** management, allowing users to revisit or delete past verifications[cite: 158].

---

## 💻 Technologies Used

| Category | Technology | Purpose / Library |
| :--- | :--- | :--- |
| **Backend** | Django Framework (Python 3.10+) | [cite_start]Multi-user web application foundation [cite: 302] |
| **OCR / Vision** | Google Vision API | [cite_start]Image-based text detection [cite: 305] |
| **Barcode** | Pyzbar / OpenCV | [cite_start]Decoding 1D/2D Barcodes and QR Codes [cite: 305] |
| **LLM / AI** | Ollama (phi-3-mini) | [cite_start]Local LLM for summary generation and RAG core [cite: 305, 215] |
| **Fuzzy Matching** | TheFuzz | [cite_start]Handling spelling errors and variations [cite: 305, 155] |
| **Data Processing** | Pandas, NumPy, Regex | [cite_start]Data extraction, matching, and manipulation [cite: 305] |
| **Database** | SQLite3 / PostgreSQL | [cite_start]Data storage and history tracking [cite: 304] |
| **Frontend** | HTML, CSS, JavaScript, Bootstrap | [cite_start]User Interface design [cite: 303] |
