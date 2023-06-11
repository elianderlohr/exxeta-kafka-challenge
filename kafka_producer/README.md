# Kafka Consumer

## Description

Der Kafka Consumer ließt die Daten (Wikipedia Changes) aus der Datei `kafka_consumer\input\wikipedia_changes.json` und veröffentlicht diese in mehreren Kafka-Topics. Jeder Wikipedia Change wird IMMER in dem `wikipedia-success` Kafka-Topic veröffentlich. Außerdem wird der Wikpedia Change auch noch in einem Länder spezifischen Kafka-Topic veröffentlich (z.B. `"wikipedia-jawiki-success"`).

## Entwicklung

### Lokales Setup

1. Installiere Docker
2. Installiere Python 3.11
3. Directory Wechseln: `cd kafka_producer`
4. Virtual Env erstellen: `python -m venv .kafka_producer_venv`
5. Virtual Env aktivieren: `source .kafka_producer_venv/bin/activate` oder `source .kafka_producer_venv/Scripts/activate`
6. Installiere die benötigten Python Pakete: `pip3 install -r requirements.txt`
7. (Optional) Deaktivieren der Virtual Env: `deactivate`

### Lokale Verwendung

1. Starte den Kafka-Broker and Zookeeper mit `docker-compose up -d`
2. Starte den Kafka Consumer mit `python src/kafka_consumer.py`

> Jede Nachricht wird in der Konsole ausgegeben. Die zufällige Wartezeit zwischen den Nachrichten wird auch ausgegeben.

### Verwendung mit Docker

Durch das ausführen der docker-compose file wird automatisch auch der Kafka Producer gestartet.

### Tests

Die Tests für den Kafka Consumer liegen im [/tests](kafka_consumer\tests) directory und können mit `pytest` ausgeführt werden.

```bash
cd kafka_producer
pytest
```
