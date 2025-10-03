# main.py
import os, json, re
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
import google.generativeai as genai

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# Flask
app = Flask(__name__)

# DB
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# One-table schema we told the model about:
# products(id, name, category, price, units_sold)

SYSTEM_PROMPT = """
Return ONLY a JSON object with one key: "sql".
The value must be a SINGLE PostgreSQL SELECT statement (no semicolon).
Target schema: products(id, name, category, price, units_sold).
Examples:
- Top 5 products by sales -> SELECT name, (price*units_sold) AS revenue FROM products ORDER BY revenue DESC LIMIT 5
- Total revenue by category -> SELECT category, SUM(price*units_sold) AS revenue FROM products GROUP BY category ORDER BY revenue DESC
"""

@app.post("/ask")
def ask():
    body = request.get_json(silent=True) or {}
    question = (body.get("question") or "").strip()
    if not question:
        return jsonify({"error": "Provide 'question'."}), 400

    prompt = f"{SYSTEM_PROMPT}\nUser question: {question}\nJSON:"
    resp = model.generate_content(prompt)
    raw = (resp.text or "").strip()

    # strip code fences if present
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.DOTALL)

    obj = json.loads(raw)          # expect: {"sql": "..."}
    sql = obj["sql"].strip()

    # run query
    with Session(engine) as s:
        result = s.execute(text(sql))
        cols = result.keys()
        rows = [dict(zip(cols, r)) for r in result.fetchall()]

    return jsonify({"question": question, "sql": sql, "rows": rows})

if __name__ == "__main__":
    # Run: python main.py  -> POST http://127.0.0.1:8000/ask
    app.run(host="0.0.0.0", port=8000, debug=True)
