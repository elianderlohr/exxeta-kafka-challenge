# Kafka Consumer

## Description

Der Kafka Consumer subscribed zwei topics (`wikipedia-success` und `wikipedia-dewiki-success`). Sobald neue Nachrichten in einem der Topics vorhanden sind, werden diese in der Konsole durch einen "." (zum debuggen) ausgegebe. Falls eine nachricht das topic `wikipedia-success` hat wird der counter für die gesamten Nachrichten erhöht. Falls eine Nachricht das topic `wikipedia-dewiki-success` hat wird der counter für die deutschen Nachrichten erhöht. Jede minute wird berechnet wie viele Nachrichten pro Minute gesendet wurden. Diese werden dann in der Konsole ausgegeben und in einer csv Datei gespeichert.

## Entwicklung

### Lokales Setup

1. Installiere Docker
2. Installiere Python 3.11
3. Directory Wechseln: `cd kafka_consumer`
4. Virtual Env erstellen: `python -m venv .kafka_consumer_venv`
5. Virtual Env aktivieren: `source .kafka_consumer_venv/bin/activate` oder `source .kafka_consumer_venv/Scripts/activate`
6. Installiere die benötigten Python Pakete: `pip3 install -r requirements.txt`
7. .env file im root directory /kafka_consumer/.env erstellen mit folgendem Inhalt:

```bash
# Set environment variables
LOG_FILE_PATH = logs/structured.log

AGGREGATION_FILE_PATH = output/aggregation.csv

# kafka
KAFKA_BOOTSTRAP_SERVERS = localhost:9092
```

8. (Optional) Deaktivieren der Virtual Env: `deactivate`

### Lokale Verwendung

1. Starte den Kafka-Broker and Zookeeper mit `docker-compose up -d`
2. Starte den Kafka Consumer mit `python src/kafka_consumer.py`

### Verwendung mit Docker

Durch das ausführen der docker-compose file wird automatisch auch der Kafka Consumer gestartet.

### Tests

Die Tests für den Kafka Consumer liegen im [/tests](kafka_consumer\tests) directory und können mit `pytest` ausgeführt werden.

```bash
cd kafka_consumer
pytest
```
