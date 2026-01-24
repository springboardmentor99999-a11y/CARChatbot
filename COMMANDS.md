# Commands Guide

This document contains useful commands for working with the Contract Analyzer project.

## Environment Setup

1. Activate the virtual environment:
   ```
   & .venv\Scripts\Activate.ps1
   ```

2. Install dependencies:
   ```
   pip install -r backend/requirements.txt
   ```

## Running the Application

To start the FastAPI server with auto-reload:
```
python -m uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`

## Git Commands

### Check status
```
git status
```

### Add and commit changes
```
git add .
git commit -m "Your commit message"
```

### Push to remote branch
```
git push origin HEAD:J_Lokeshprabu
```

### Pull latest changes
```
git pull origin J_Lokeshprabu
```

## Database Initialization

To initialize the database (if needed):
```
python backend/init_db.py
```

## Testing the API

You can test the `/analyze` endpoint by uploading a PDF file to `http://localhost:8000/analyze`

## Other Useful Commands

- View git log: `git log --oneline`
- View differences: `git diff`
- Create a new branch: `git checkout -b new-branch-name`