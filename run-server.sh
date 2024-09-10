#!/bin/bash

# Starte das Python-Skript im Hintergrund und speichere die PID
python3 SERVER/app.py > app.log 2>&1 &
APP_PID=$!

# Warte 30 Sekunden
sleep 30

# Prüfe, ob der Prozess noch läuft
if ps -p $APP_PID > /dev/null
then
   # Wenn der Prozess noch läuft, beende ihn
   kill $APP_PID
   wait $APP_PID 2>/dev/null
   echo "Der Prozess wurde nach 30 Sekunden gestoppt."
else
   echo "Der Prozess wurde innerhalb der Zeit erfolgreich abgeschlossen."
fi

# Überprüfe, ob Fehler in der Log-Datei vorhanden sind
if grep -i "error" app.log > /dev/null
then
    echo "Fehler wurden im Python-Skript festgestellt."
    exit 1
else
    echo "Das Python-Skript hat ohne Fehler abgeschlossen."
    exit 0
fi
