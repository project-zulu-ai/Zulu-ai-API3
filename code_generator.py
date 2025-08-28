def generate_app(idea: str) -> dict:
    """
    Generate app starter code based on the idea
    
    Args:
        idea: The app idea description
        
    Returns:
        Dictionary with file paths as keys and code content as values
    """
    
    # React frontend with Tailwind
    frontend_code = '''import React, { useState } from 'react';

function App() {
  const [items, setItems] = useState([]);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-4">
          My App
        </h1>
        <p className="text-gray-600">
          Starter React app with Tailwind CSS
        </p>
      </div>
    </div>
  );
}

export default App;'''

    # FastAPI backend with SQLite
    backend_code = '''from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List

app = FastAPI()

# Database setup
def init_db():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

class Item(BaseModel):
    name: str

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.get("/items")
async def get_items():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    return [{"id": item[0], "name": item[1]} for item in items]

@app.post("/items")
async def create_item(item: Item):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name) VALUES (?)", (item.name,))
    conn.commit()
    conn.close()
    return {"message": "Item created successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)'''

    # README with setup instructions
    readme_content = f'''# {idea}

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
- `POST /items` - Create new item'''

    return {
        "frontend/App.js": frontend_code,
        "backend/main.py": backend_code,
        "README.md": readme_content
    }