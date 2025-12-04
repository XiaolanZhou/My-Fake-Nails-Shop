import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/api/debug')
def debug():
    return jsonify({
        "has_database_url": bool(os.getenv("DATABASE_URL")),
        "has_postgres_url": bool(os.getenv("POSTGRES_URL")),
        "env_keys": [k for k in os.environ.keys() if 'PG' in k or 'DATABASE' in k or 'POSTGRES' in k]
    })

@app.route('/api/products')
def products():
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        
        database_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL")
        if not database_url:
            return jsonify({"error": "No DATABASE_URL", "items": [], "total_pages": 1})
        
        conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        cur.execute("SELECT * FROM products LIMIT 10")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        return jsonify({
            "items": [dict(r) for r in rows],
            "total_pages": 1
        })
    except Exception as e:
        return jsonify({"error": str(e), "items": [], "total_pages": 1})
