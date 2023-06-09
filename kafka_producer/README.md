# Kafka Consumer

## Description

Der Kafka Consumer ließt die Daten (Wikipedia Changes) aus der Datei `kafka_consumer\input\wikipedia_changes.json` und veröffentlicht diese in mehreren Kafka-Topics. Jeder Wikipedia Change wird IMMER in dem `wikipedia-success` Kafka-Topic veröffentlich. Außerdem wird der Wikpedia Change auch noch in einem Länder spezifischen Kafka-Topic veröffentlich (z.B. `"wikipedia-jawiki-success"`).

## Entwicklung

### Lokales Setup

1. Installiere Docker
2. Installiere Python 3.11
3. Directory Wechseln: `cd kafka_producer`
4. Virtual Env erstellen: `python3 -m venv kafka_consumer_venv`
5. Virtual Env aktivieren: `source kafka_consumer_venv/bin/activate`
6. Installiere die benötigten Python Pakete: `pip install -r requirements.txt`

### Lokale Verwendung

1. Starte den Kafka-Broker and Zookeeper mit `docker-compose up -d`
2. Starte den Kafka Consumer mit `python kafka_consumer.py`

> Jede Nachricht wird in der Konsole ausgegeben. Die zufällige Wartezeit zwischen den Nachrichten wird auch ausgegeben.

### Verwendung mit Docker

Durch das ausführen der docker-compose file wird automatisch auch der Kafka Producer gestartet.

### Tests

Die Tests für den Kafka Consumer liegen im [/tests](kafka_consumer\tests) directory und können mit `pytest` ausgeführt werden.
