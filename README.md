# Zulu AI App Generator API

A FastAPI service that generates app starter code based on user ideas.

## Setup

1. Install dependencies:
```bash
pip install fastapi uvicorn
```

2. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:5000`

## Usage

### Generate App Code

**Endpoint:** `POST /generate_app`

**Request:**
```json
{
  "idea": "Your app idea description"
}
```

**Response:**
```json
{
  "frontend": {
    "App.js": "// React code placeholder"
  },
  "backend": {
    "main.py": "# FastAPI backend placeholder"
  },
  "readme": "# Your app idea\n\nGenerated app starter by Zulu AI"
}
```

### Health Check

**Endpoint:** `GET /`

Returns API status information.

## API Documentation

Once running, visit `http://localhost:5000/docs` for interactive API documentation.