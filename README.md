# AI → SQL Query Interface

Ask questions in natural language, get SQL queries and results instantly using Google Gemini AI and PostgreSQL.

## Setup

1. **Install dependencies**
```bash
cd backend
pip install -r requirements.txt
```

2. **Configure environment** - Create `backend/.env`:
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
GEMINI_API_KEY=your_gemini_key
```

3. **Seed database**
```bash
python seed_db.py
```

4. **Run server**
```bash
python main.py
```

5. **Open** `frontend/index.html` in your browser

## Usage

Type questions like:
- "Top 5 products by sales"
- "Total revenue by category"
- "Products under 20 sorted by price"

## API

**POST** `/ask`
```json
{"question": "Top 5 products by sales"}
```

## Stack

Backend: Flask, SQLAlchemy, PostgreSQL, Google Gemini  
Frontend: Vanilla JS, HTML, CSS

## Note

⚠️ Demo project only - add proper security for production use.