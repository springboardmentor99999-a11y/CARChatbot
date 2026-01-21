# CARChatbot Setup Guide

## 🚀 Quick Start

This guide will help you set up and run the CARChatbot API for car loan/lease contract analysis.

## 📋 Prerequisites

- **Python 3.8 or higher** (Python 3.11 recommended)
- **pip** (Python package manager)
- **Poppler** (for PDF to image conversion)
- **Tesseract OCR** (optional, for scanned PDFs)
- **OpenAI API Key** (for LLM-based features)

---

## 🔧 Installation Steps

### Step 1: Install Python Dependencies

Open PowerShell/Command Prompt in the project directory and run:

```powershell
pip install -r requirements.txt
```

### Step 2: Install Poppler (Required for PDF Processing)

**Windows:**
1. Download Poppler from: https://github.com/oschwartz10612/poppler-windows/releases
2. Extract the zip file (e.g., to `C:\poppler`)
3. Add the `bin` folder to your system PATH:
   - `C:\poppler\Library\bin`

**Alternative (using Chocolatey):**
```powershell
choco install poppler
```

### Step 3: Install Tesseract OCR (Optional - for scanned PDFs)

**Windows:**
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (default location: `C:\Program Files\Tesseract-OCR`)
3. Note the installation path for the next step

### Step 4: Configure Environment Variables

1. Copy the example environment file:
```powershell
Copy-Item .env.example .env
```

2. Edit `.env` file and add your configuration:
```env
OPENAI_API_KEY=your_actual_openai_api_key_here
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
```

**Get OpenAI API Key:**
- Sign up at https://platform.openai.com/
- Go to API Keys section
- Create a new API key

---

## ▶️ Running the Application

### Method 1: Using the Startup Script (Recommended)

Simply run:
```powershell
python run.py
```

This will:
- Initialize the database
- Check your configuration
- Start the API server at http://127.0.0.1:8000

### Method 2: Manual Start

1. Initialize the database:
```powershell
python backend/init_db.py
```

2. Start the server:
```powershell
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📚 API Documentation

Once the server is running, access:

- **Interactive API Docs**: http://127.0.0.1:8000/docs
- **Alternative Docs**: http://127.0.0.1:8000/redoc
- **Health Check**: http://127.0.0.1:8000/health

---

## 🧪 Testing the API

### 1. Health Check

```powershell
curl http://127.0.0.1:8000/health
```

### 2. Analyze a Contract (Upload PDF)

Using PowerShell:
```powershell
$form = @{
    file = Get-Item -Path "path\to\contract.pdf"
}
Invoke-RestMethod -Uri "http://127.0.0.1:8000/analyze" -Method Post -Form $form
```

### 3. VIN Lookup

```powershell
curl http://127.0.0.1:8000/vin/1HGBH41JXMN109186
```

### 4. Get Negotiation Points

```powershell
$body = @{
    sla = @{
        apr_percent = 15
        fees = @{
            documentation_fee = 6000
        }
    }
    fairness = @{
        fairness_score = 65
    }
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/negotiate" -Method Post -Body $body -ContentType "application/json"
```

---

## 📁 Project Structure

```
CARChatbot/
├── backend/
│   ├── __init__.py              # Package initializer
│   ├── main.py                  # FastAPI application & endpoints
│   ├── db.py                    # Database operations
│   ├── pdf_reader.py            # PDF text extraction
│   ├── contract_analyser.py     # Rule-based contract analysis
│   ├── llm_sla_extractor.py     # AI-powered SLA extraction
│   ├── fairness_engine.py       # Contract fairness scoring
│   ├── negotiation_assistant.py # Negotiation suggestions
│   ├── vin_service.py           # Vehicle VIN lookup
│   ├── sla_schema.py            # SLA data schema
│   ├── init_db.py               # Database initialization
│   └── database.db              # SQLite database (auto-created)
├── app/                         # Frontend (empty for now)
├── data/                        # Training data
├── models/                      # ML models
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .env                         # Your actual environment config (create this)
├── run.py                       # Startup script
├── SETUP.md                     # This file
└── README.md                    # Project overview
```

---

## 🔍 Available API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/analyze` | Upload and analyze contract PDF |
| GET | `/vin/{vin}` | Lookup vehicle details by VIN |
| POST | `/negotiate` | Get negotiation suggestions |

---

## 🐛 Troubleshooting

### Issue: "No module named 'backend'"
**Solution:** Make sure you're running from the project root directory:
```powershell
cd "D:\CAR LOAN BOT\CARChatbot"
python run.py
```

### Issue: PDF processing fails
**Solution:** Ensure Poppler is installed and in your PATH. Restart your terminal after adding to PATH.

### Issue: Tesseract not found
**Solution:** Either:
1. Set `TESSERACT_PATH` in `.env` file
2. Add Tesseract to system PATH
3. Ignore (only needed for scanned PDFs)

### Issue: OpenAI API errors
**Solution:** 
1. Check your API key in `.env`
2. Verify you have credits in your OpenAI account
3. Check your internet connection

### Issue: "Port 8000 already in use"
**Solution:** Either:
1. Stop the other process using port 8000
2. Change the port in `run.py` (line 59)

---

## 💡 Features

✅ **PDF Analysis**: Upload car loan/lease contracts and extract key terms
✅ **Fairness Scoring**: Get an objective fairness score (0-100)
✅ **Red Flag Detection**: Identifies potentially unfair terms
✅ **Negotiation Assistant**: Suggests specific points to negotiate
✅ **VIN Lookup**: Decode Vehicle Identification Numbers
✅ **OCR Support**: Works with both digital and scanned PDFs

---

## 🔐 Security Notes

- Never commit your `.env` file to version control
- Keep your OpenAI API key secure
- The database stores uploaded contract text - ensure proper access controls in production

---

## 📞 Support

For issues or questions:
1. Check this SETUP.md file
2. Review the API documentation at `/docs`
3. Contact the project mentor

---

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Configure environment variables
3. ✅ Run the application
4. 📄 Test with a sample PDF contract
5. 🔧 Customize for your use case

Happy analyzing! 🚗✨
