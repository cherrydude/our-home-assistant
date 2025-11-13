#!/usr/bin/env python3
# Einfacher TTS HTTP-Service: erzeugt WAV Dateien mit espeak-ng
# Speichere diese Datei in ~/Desktop/our-home-assistant-main/tts_server.py

import os
import uuid
import shlex
import subprocess
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# Pfad wo Home Assistant die Dateien als /local/serves (config/www)
PROJECT_DIR = os.path.expanduser("~/Desktop/our-home-assistant-main")
OUT_DIR = os.path.join(PROJECT_DIR, "config", "www", "tts")
os.makedirs(OUT_DIR, exist_ok=True)

def safe_filename(name: str) -> str:
    # Nur einfache erlaubte Zeichen + fallback UUID
    base = "".join(c for c in name if c.isalnum() or c in ("-", "_")).strip()
    if not base:
        base = str(uuid.uuid4())
    return base + ".wav"

@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json(force=True, silent=True)
    if not data or "text" not in data:
        return abort(400, "JSON mit Feld 'text' erforderlich")
    text = data["text"]
    lang = data.get("lang", "de")
    filename = data.get("filename")
    if filename:
        filename = safe_filename(filename)
    else:
        filename = f"tts_{uuid.uuid4().hex[:8]}.wav"

    out_path = os.path.join(OUT_DIR, filename)

    # espeak-ng Kommando: -v für voice (z.B. de), -w für wav output
    # Escape text sicher
    try:
        cmd = ["espeak-ng", "-v", lang, "-w", out_path, text]
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        return abort(500, f"TTS fehler: {e}")

    # URL, die Home Assistant über /local/ erreichen kann
    url = f"/local/tts/{filename}"
    return jsonify({"file": filename, "url": url})

if __name__ == "__main__":
    # Nur für Entwicklertest: binding auf allen Interfaces
    app.run(host="0.0.0.0", port=5002)
