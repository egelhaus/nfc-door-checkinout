from flask import Flask, render_template
from dotenv import load_dotenv
import os
import mysql.connector

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

@app.route("/")
def show_logs():
    """Zeigt alle Logs (Check-ins/Check-outs) in einer Tabelle an"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM logs ORDER BY id DESC")
    logs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("logs.html", logs=logs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
