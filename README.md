# GenAI Headhunter  
**AI‑Driven Job Intelligence & Automated Role Analysis**

GenAI Headhunter este o soluție enterprise orientată către automatizarea proceselor de analiză a anunțurilor de angajare. Platforma utilizează agenți AI specializați pentru a extrage informații critice, a valida acuratețea datelor și a genera o evaluare structurată a rolului, optimizând astfel procesul de recrutare tehnică.

---

## 1. Overview

Organizațiile moderne gestionează volume mari de anunțuri de joburi, iar analiza manuală consumă timp și introduce variații în calitatea evaluărilor.  
GenAI Headhunter oferă:

- **Standardizare** în evaluarea rolurilor tehnice  
- **Reducerea timpului de analiză** prin automatizare  
- **Creșterea acurateței** prin validare multi‑agent  
- **Recomandări acționabile** pentru candidați sau recrutori  

---

## 2. Core Capabilities

### 2.1 Extraction Engine  
Agentul Extractor identifică și structurează informațiile esențiale dintr-un anunț de job:
- Tehnologii și competențe
- Cerințe obligatorii și opționale
- Locație și tip de lucru (remote/hybrid/on‑site)
- Interval salarial (dacă este disponibil)
- Beneficii și responsabilități

### 2.2 Validation Layer  
Agentul Validator asigură integritatea datelor extrase:
- Confirmă consistența cu textul original
- Semnalează incongruențe sau lipsuri
- Asigură conformitatea cu schema internă

### 2.3 Job Analysis Engine  
Agentul de analiză generează o evaluare completă a rolului:
- Titlul poziției și compania
- Seniority estimat
- Match score (0–100)
- Red flags operaționale sau tehnice
- Sumar executiv al rolului

### 2.4 Advisory Module  
Agentul Counselor oferă recomandări personalizate:
- Direcții de îmbunătățire pentru candidat
- Riscuri potențiale
- Alinierea profilului la cerințele rolului

---

## 3. System Architecture
GenAI-Headhunter/ │ ├── agents/ │   ├── extractor.py │   ├── validator.py │   └── counselor.py │ ├── models/ │   ├── extraction_models.py │   └── job_models.py │ ├── utils/ │   ├── ai_client.py │   └── scraper.py │ ├── ui_job_analyzer.py ├── job_analyzer.py ├── monitoring.py ├── requirements.txt └── .gitignore

Arhitectura este modulară, permițând extinderea facilă a agenților sau integrarea cu sisteme ATS existente.

---

## 4. Installation & Setup

### 4.1 Create Virtual Environment

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
License
Acest proiect este furnizat în scop educațional și poate fi extins sau adaptat în funcție de cerințele organizaționale.

