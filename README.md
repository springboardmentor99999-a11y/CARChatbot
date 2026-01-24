# Car Lease/Loan Contract Analyzer

An AI-powered web application for analyzing car lease and loan contracts, providing SLA extraction, fairness scoring, and negotiation assistance.

## Features

- PDF text extraction with OCR fallback
- Dual SLA extraction (rule-based + LLM)
- Fairness scoring with market comparison
- AI-generated negotiation points
- VIN decoding with estimated market price
- Contract comparison tool
- Web app interface with Streamlit
- RESTful API with FastAPI

## Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd <repo-dir>
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the backend folder with:
```
OPENAI_API_KEY=your_key_here
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe  # If on Windows
```

5. Initialize the database:
```bash
python backend/init_db.py
```

## Running the Application

### Backend API
Start the FastAPI server:
```bash
uvicorn backend.main:app --reload
```
API available at `http://localhost:8000`

### Web App
Start the Streamlit app:
```bash
streamlit run app/app.py
```
App available at `http://localhost:8501`

## API Endpoints

- `GET /` - Health check
- `POST /analyze` - Upload PDF and get analysis (SLA, fairness, negotiation points)
- `POST /compare` - Upload two PDFs and compare them
- `GET /vin/{vin}` - Decode VIN with vehicle details and price estimate

## Usage

1. Upload a contract PDF via the web app or API.
2. Receive structured SLA data, fairness score, and personalized negotiation tips.
3. Use VIN lookup for vehicle info.

## Git Commands

### To push changes:
```bash
git add .
git commit -m "Your commit message"
git push origin HEAD:J_Lokeshprabu
```

### Branch Information
- Local branch: main
- Remote branch: J_Lokeshprabu
- Repository: https://github.com/springboardmentor99999-a11y/CARChatbot

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI application
│   ├── contract_analyzer.py # Contract analysis logic
│   ├── pdf_reader.py        # PDF text extraction
│   ├── db.py                # Database operations
│   └── requirements.txt     # Python dependencies
├── uploads/                 # Uploaded PDF files
├── models/                  # ML models
└── data/                    # Training data
```
