# our-home-assistant
repo = basis des home assistant (sprachunterstützung + offline) für den lokalen raspberry pi

```markdown
# Home Assistant Starter für Raspberry Pi 3 (offline, Portainer/Docker)

Dieses Starter‑Projekt richtet Home Assistant (Container), Mosquitto (MQTT)
und Rhasspy (Offline-Sprachassistent) auf einem Raspberry Pi 3 ein. TTS erfolgt lokal über
pico2wave (hostseitig installiert).

Einmalige Internetverbindung wird empfohlen, um Docker‑Images und das Vosk‑ASR‑Modell
herunterzuladen; danach ist der Betrieb offline möglich.

Wichtig:
- Du nutzt Portainer; du kannst docker-compose.yml als Stack importieren (Stacks → Add stack
 → Inhalt einfügen) oder über SSH `docker compose up -d` ausführen.
- Dieses Setup ist auf Ressourcen‑sparenden Betrieb auf einem Pi 3 eingestellt
(plattform: linux/arm/v7 für Home Assistant).

Inhalt
- docker-compose.yml — Stack mit Home Assistant, Mosquitto, Rhasspy
- .env — Zeitzone
- config/configuration.yaml — minimale Home Assistant Konfiguration
(MQTT, TTS via command_line/pico2wave, intent_script)
- config/automations.yaml — Beispielautomation
- mosquitto/config/mosquitto.conf — einfacher Broker
- rhasspy/profiles/de/* — Rhasspy Profil (Deutsch) + sentences.ini
- README.md — diese Datei

Schnellstart (mit einmaligem Internet)
1. Dateien auf Pi kopieren (z.B. /home/pi/hass-offline).
2. Einmalig: Docker + Docker Compose installieren (falls noch nicht):
   sudo apt update
   curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
   sudo apt install -y docker-compose-plugin
   (Portainer nutzt bereits Docker — ggf. Schritt überspringen)

3. Einmalig: pico2wave installieren (für TTS auf dem Host):
   sudo apt update
   sudo apt install -y libttspico-utils

4. Einmalig: Vosk‑Deutsches Modell herunterladen und entpacken (Beispiel: vosk-model-small-de-0.15).
   cd rhasspy/profiles/de
   wget https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip
   unzip vosk-model-small-de-0.15.zip
   mv vosk-model-small-de-0.15 model
   # Prüfe die aktuelle Modellversion auf https://alphacephei.com/vosk/models

5. Portainer: Stack erstellen (oder auf Shell):
   - Portainer: Stacks → Add stack → Stack name → Compose file Inhalt einfügen (docker-compose.yml)
→ Deploy the stack.
   - Shell: docker compose up -d

6. Erste Zugriffe:
   - Home Assistant: http://<raspi-ip>:8123
   - Portainer: http://raspberrypi.local:9000 (wie bei dir)
   - Rhasspy UI: http://<raspi-ip>:12101

Rhasspy Hinweise:
- Profile: deutsches Profil liegt in rhasspy/profiles/de.
- In Rhasspy UI: Profil 'de' auswählen, bei Settings → Speech to Text → Vosk (falls nötig), Intent Handling
→ MQTT (Broker: mosquitto).
- Trainiere Sentence‑Intents in UI oder über die files.

TTS in Home Assistant:
- Home Assistant nutzt tts.command_line mit pico2wave. pico2wave erzeugt WAV‑Dateien in /config/www/tts,
die HA über media_player abspielen kann.

Mikrofon / Sound:
- Wenn du ein USB‑Mikrofon verwendest, stelle sicher, dass der Rhasspy‑Container Zugriff auf
/dev/snd hat (ist in Compose gesetzt).
- Auf Pi3 können ASR‑Erkennungen etwas langsamer sein; das kleine Vosk‑Modell ist für Performance optimiert.

Sicherheit:
- Dieses Setup verwendet allow_anonymous true für Mosquitto (lokal). Für produktiven Einsatz bitte
Benutzer/Passwort und ggf. TLS einrichten.

Wenn du möchtest, passe ich jetzt:
- Die Compose/Stack‑Datei für direkte Portainer‑Importierung an,
- oder erstelle ein kurzes Shell‑Skript, das Vosk‑Modell und Abhängigkeiten automatisch herunterlädt.

Antworte kurz: Darf ich einmalig Internet für das Herunterladen der Images/Modelle voraussetzen?
```
