
import os
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "127.0.0.1"),
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )

@app.route("/health", methods=["GET"])
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({
            "status": "online",
            "database": "connected"
        }), 200
    except Exception:
        return jsonify({
            "status": "error",
            "database": "unavailable"
        }), 503

@app.route("/messages", methods=["GET"])
def get_messages():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, message, created_at
        FROM app_messages
        ORDER BY id DESC
    """)

    rows = cur.fetchall()

    messages = [
        {
            "id": row[0],
            "message": row[1],
            "created_at": row[2].isoformat()
        }
        for row in rows
    ]

    cur.close()
    conn.close()

    return jsonify(messages)

@app.route("/messages", methods=["POST"])
def create_message():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "Message is required"}), 400

    if len(message) > 2000:
        return jsonify({"error": "Message is too long"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO app_messages (message)
        VALUES (%s)
        RETURNING id, message, created_at
    """, (message.strip(),))

    row = cur.fetchone()
    conn.commit()

    result = {
        "id": row[0],
        "message": row[1],
        "created_at": row[2].isoformat()
    }

    cur.close()
    conn.close()

    return jsonify(result), 201

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

