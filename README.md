# Car Loan/Lease Contract Review and Negotiation AI Assistant

## 🚗 Project Overview

The Car Lease or Loan Contract Review and Negotiation App is an AI-driven application designed to assist consumers in understanding, reviewing, and negotiating their car lease or loan contracts. The application leverages Large Language Models (LLMs) for SLA extraction, identifies key contract terms, and provides transparency by cross-verifying vehicle pricing and history.

## ✨ Key Features

### 1. Contract Review and SLA Extraction
- Upload PDF or image of your contract
- AI-powered extraction of key terms:
  - Interest rate / APR
  - Lease term duration
  - Monthly payment
  - Down payment
  - Mileage allowance
  - Early termination clause
  - And more...
- **Contract Fairness Score** (0-100)

### 2. VIN-Based Car Information
- Vehicle details lookup via NHTSA API
- Recall history
- Manufacturer information

### 3. Negotiation Assistant
- AI chatbot for negotiation guidance
- Suggested questions to ask dealers
- Email draft generation
- Personalized negotiation tips

### 4. Price Estimation
- Fair market value benchmarks
- Price range estimation

### 5. Contract Comparison
- Side-by-side comparison of multiple offers
- Visual comparison dashboard

## 🏗️ Project Structure

```
CAR LOAN BOT/
├── app/                          # Flutter Mobile App
│   └── car_loan_assistant/
│       └── lib/
│           ├── config/           # App configuration
│           ├── models/           # Data models
│           ├── providers/        # State management
│           ├── screens/          # UI screens
│           ├── services/         # API services
│           └── widgets/          # Reusable widgets
├── backend/                      # Python FastAPI Backend
│   ├── main.py                   # API endpoints
│   ├── contract_analyzer.py      # Contract analysis
│   ├── llm_sla_extractor.py     # LLM integration
│   ├── vin_service.py           # VIN lookup
│   ├── negotiation_assistant.py # Negotiation tips
│   ├── fairness_engine.py       # Fairness scoring
│   └── db.py                    # Database operations
├── data/                         # Sample contracts
├── models/                       # ML models
└── samples/                      # Sample data
```

## 🚀 Getting Started

### Backend Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export OPENAI_API_KEY=your_api_key_here
```

4. Run the server:
```bash
uvicorn backend.main:app --reload --port 8000
```

### Flutter App Setup

1. Navigate to app directory:
```bash
cd app/car_loan_assistant
```

2. Install dependencies:
```bash
flutter pub get
```

3. Run the app:
```bash
flutter run
```

## 📱 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/analyze` | POST | Upload and analyze contract (regex-based) |
| `/analyze-llm` | POST | Analyze contract using LLM (GPT-4) |
| `/analyze-text` | POST | Analyze raw contract text |
| `/contracts` | GET | List all analyzed contracts |
| `/contracts/{id}` | GET | Get specific contract details |
| `/contracts/{id}` | DELETE | Delete a contract |
| `/compare?ids=1,2,3` | GET | Compare multiple contracts |
| `/vin/{vin}` | GET | VIN lookup with vehicle details |
| `/vin/{vin}/recalls` | GET | Get recall information for VIN |
| `/vin/{vin}/validate` | GET | Validate VIN checksum |
| `/negotiate` | POST | Get negotiation tips |
| `/negotiate/email` | POST | Generate negotiation email |
| `/negotiate/questions` | GET | Get dealer questions list |
| `/price-estimate` | GET | Get price estimate |
| `/health` | GET | API health check |
| `/api-info` | GET | List all available endpoints |

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **OpenAI GPT** - LLM for contract analysis
- **SQLite** - Local database
- **NHTSA API** - Vehicle data

### Frontend (Flutter)
- **Provider** - State management
- **Dio** - HTTP client
- **Google Fonts** - Typography
- **FL Chart** - Data visualization

## 📊 Fairness Score Calculation

The fairness score (0-100) is calculated based on:
- Interest rate comparison to market average
- Presence of early termination penalties
- Documentation fees
- Red flags in contract terms

## 👥 Team

**Mentor:** Mahaprasad Jena

---

CARChatbot Project

Repository: https://github.com/springboardmentor99999-a11y/CARChatbot

🔒 Branch Rules for Interns
❗ DO NOT push anything to the main branch.

All interns must work ONLY inside their assigned branch.

Example branch names:

khushisu192-branch

harshithboyina-branch

kanhaiyagupta6773-branch

…and so on.

If you don't know your branch name, ask the mentor.

🛠️ How Interns Should Work
1️⃣ Clone the repository
git clone https://github.com/springboardmentor99999-a11y/CARChatbot.git
cd CARChatbot

2️⃣ Create your branch
git checkout -b <your-branch-name>

3️⃣ Add your project files

Place your:

Python scripts

Models

Datasets

Images

Jupyter Notebooks

Documentation

4️⃣ Commit and push
git add .
git commit -m "My first commit"
git push origin <your-branch-name>

📁 Recommended Folder Structure
CARChatbot/
│
├── app/               # Main backend code
├── models/            # ML models
├── data/              # Training data
├── notebooks/         # Jupyter notebooks
├── images/            # Reference images or documentation visuals
├── docs/              # Documentation files
└── README.md

✔️ Pull Request Process

Once work is ready:

Push to your branch

Create a Pull Request to main

Mentor will review and approve or request changes

🙌 Contributing

Follow guidelines in CONTRIBUTING.md (to be added soon).
