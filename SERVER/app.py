from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import mysql.connector
from datetime import datetime

# Lade die Umgebungsvariablen aus der .env Datei
load_dotenv()

# Konfiguration der MySQL-Datenbank über Umgebungsvariablen
db_config = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME")
}

def get_db_connection():
    """Stellt eine Verbindung zur MySQL-Datenbank her"""
    return mysql.connector.connect(**db_config)

app = Flask(__name__)

def log_event(uid):
    """Prozessiert einen NFC Scan, indem ein Check-in oder Check-out vermerkt wird"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Überprüfe, ob es einen offenen Check-in für diese UID gibt
    cursor.execute(
        "SELECT * FROM logs WHERE uid = %s ORDER BY id DESC LIMIT 1", (uid,)
    )
    last_entry = cursor.fetchone()

    if last_entry and last_entry['checkout_time'] is None:
        # Wenn ein Check-in gefunden wurde, Check-out durchführen
        checkout_time = datetime.now()
        cursor.execute(
            "UPDATE logs SET checkout_time = %s WHERE id = %s",
            (checkout_time, last_entry['id'])
        )
        conn.commit()
        duration = checkout_time - last_entry['checkin_time']
        return {"status": "checked out", "duration": str(duration)}
    else:
        # Wenn kein Check-in gefunden wurde, Check-in durchführen
        checkin_time = datetime.now()
        cursor.execute(
            "INSERT INTO logs (uid, checkin_time) VALUES (%s, %s)", (uid, checkin_time)
        )
        conn.commit()
        return {"status": "checked in", "checkin_time": str(checkin_time)}

    cursor.close()
    conn.close()

@app.route("/nfc-scan", methods=["POST"])
def nfc_scan():
    """Verarbeitet einen NFC Scan vom Raspberry Pi"""
    data = request.get_json()
    uid = data.get("uid")
    
    if uid:
        result = log_event(uid)
        return jsonify(result)
    
    return jsonify({"status": "error", "message": "No UID received"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
