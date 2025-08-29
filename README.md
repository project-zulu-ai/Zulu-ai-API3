# Task management app

Generated app starter by Zulu AI

## Project Structure

```
frontend/          # React frontend
├── App.js        # Main React component
backend/          # FastAPI backend  
├── main.py       # API server
README.md         # This file
```

## Setup Instructions

### Backend Setup

1. Install Python dependencies:
```bash
pip install fastapi uvicorn sqlite3
```

2. Run the API server:
```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd frontend
npm install react react-dom
npm install -D tailwindcss
```

2. Start the development server:
```bash
npm start
```

The app will be available at `http://localhost:3000`

## API Endpoints

- `GET /` - Health check
- `GET /items` - Get all items
- `POST /items` - Create new item