import os
from datetime import datetime, timezone
import psycopg
from flask import Flask, jsonify

app = Flask(__name__)
APP_VERSION = os.getenv('APP_VERSION', '3.0.0')
DB_HOST = os.getenv('DB_HOST', 'postgres')
DB_PORT = int(os.getenv('DB_PORT', '5432'))
DB_NAME = os.getenv('POSTGRES_DB', 'swiftcart')
DB_USER = os.getenv('POSTGRES_USER', 'swiftcart')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'swiftcartpass')

def get_connection():
    return psycopg.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
                           user=DB_USER, password=DB_PASSWORD, connect_timeout=3)

@app.get('/')
def home():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, visited_at TIMESTAMPTZ NOT NULL DEFAULT NOW())')
            cur.execute('INSERT INTO visits DEFAULT VALUES')
            cur.execute('SELECT COUNT(*) FROM visits')
            visits = cur.fetchone()[0]
            conn.commit()
    return f'''<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>SwiftCart | Kubernetes Lab</title><style>body{{font-family:Arial;background:#f4f7fb;margin:0}}.wrap{{max-width:900px;margin:60px auto;padding:20px}}.card{{background:#fff;border-radius:16px;padding:36px;box-shadow:0 8px 30px #0001}}.ok{{color:#16803c;font-weight:700}}code{{background:#eef2f7;padding:3px 7px;border-radius:6px}}</style></head><body><div class="wrap"><div class="card"><h1>SwiftCart Logistics</h1><p class="ok">✓ Application running on Kubernetes / Minikube</p><p>Deployed from the Docker image used in the previous labs.</p><hr><p><strong>Application version:</strong> {APP_VERSION}</p><p><strong>Database service:</strong> {DB_HOST}:{DB_PORT}</p><p><strong>Persistent visits recorded:</strong> {visits}</p><p><strong>Health:</strong> <code>/health</code></p><p><strong>Database test:</strong> <code>/api/db-check</code></p></div></div></body></html>'''

@app.get('/health')
def health():
    return jsonify(status='healthy', service='swiftcart-api', version=APP_VERSION)

@app.get('/api/db-check')
def db_check():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT version()')
            version = cur.fetchone()[0]
    return jsonify(database='postgresql', connected=True, server_version=version)

@app.get('/api/status')
def api_status():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM visits')
            visits = cur.fetchone()[0]
    return jsonify(application='SwiftCart Logistics', status='running', containerized=True,
                   orchestrated_by='Kubernetes', version=APP_VERSION, database_host=DB_HOST,
                   visits=visits, timestamp=datetime.now(timezone.utc).isoformat())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
