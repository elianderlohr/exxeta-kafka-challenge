# Exxeta Kafka Challenge 2023

> Docu in german

## 1. Aufgabe

Entwicklung eines Kafka-Producers und Kafka-Consumers welche mock Wikipedia Daten verarbeiten. Der Kafka-Producer soll die Daten in ein Kafka-Topic schreiben und der Kafka-Consumer soll die Daten aus dem Kafka-Topic lesen und simple aggregationen durchführen.

### **Frage 1**: _Was wäre eine mögliche Datenbank zur Speicherung der Daten? (Vor-/ Nachteile)_

**Min. Throughput Rate:**

- Wikipedia hat aktuell ca. 1.5 mio Changes pro Tag. Das bedeutet ca. 1000 Changes pro Sekunde. Das bedeutet die Datenbank muss eine mindest Throughput von 1000 Changes pro Sekunde einhalten.

**Speicherbedarf:**

- Wikipedia hat aktuell ca. 6 Milliarden Changes (für alle Sprachen und Wikis). Das bedeutet die Datenbank muss ca. 6 Milliarden Changes speichern können. Ein Datensatz benötigt ungefähr 800 Bytes. Das bedeutet die Datenbank muss ca. 4,8 TB speichern können.
- Pro Jahr würde (Stand jetzt) ca. 430 GB an Daten hinzukommen. Die Anzahl der Changes pro Jahr steigt jedoch und damit auch der Speicherbedarf.
- 30 columns \* 6 Milliarden Changes = 180 Milliarden Zellen

**Datenbankschema:**

- Es ist davon auszugehen, dass das Schema eines Datensatzes sich nicht ändert und bei historischen Daten gleich ist. Das bedeutet das Schema muss nicht flexibel sein.

#### **Antwort: Apache Cassandra**

##### **Vorteile:**

- Wide-column Datenbank erlaubt das einfache Speichern der Wikipedia Changes
- cQL sehr ähnlich zu SQL
- Hohe Verfügbarkeit und Skalierbarkeit
- Kein Single Point of Failure
- Azure bietet Cassandra als Managed Service an
- Cassandra ist Open Source
- Gebaut für viele Daten

##### **Nachteile:**

- Keine Joins möglich (sollte aber kein problem sein, da daten in einer Tabelle liegen)
- Keine Subqueries möglich
- Keine Transaktionen möglich (Kein Rollback möglich)
- Cassandra opfert strenge Konsistenz zugunsten von hoher Verfügbarkeit und Partitionstoleranz
- Scanning von Daten wenn der PK nicht bekannt ist ist sehr langsam

> Joins sind nicht nötig da die Daten in einer Tabelle liegen. Konsistenz ist auch nicht relevant da die Anwendung aktuell zur exploration genutzt werden soll (inkonsistens zwischen consumern sind also kein Problem).

### **Frage 2**: _Welches Datenmodell wäre deiner Meinung nach sinnvoll zur Ablage der Events_

Die Changes Events sollten in einer Wide-Column Row gespeichert werden.

**Partition Key:**

- `wiki` (z.B. enwiki)
- `bot` (bot oder kein bot)

Beide Keys sind als Composite Partition Key nützlich um queries auf ein bestimmtes wiki oder auf alle wikis zu ermöglichen. Außerdem ist es nützlich zwischen bot und nicht bot edits zu unterscheiden.

**Clustering Key:**

- `timestamp` (aus dem Event)
- `insert_timestamp` (Zeitpunkt des Einfügens in die Datenbank)

Die Clustering Keys sind nützlich um die Events nach Zeit zu sortieren. Außerdem ist es nützlich die Events nach dem Zeitpunkt des Einfügens in die Datenbank zu sortieren.

### **Frage 3**: _Welche Topics wären sinnvoll? Beschreibe Vor-/Nachteile deiner Topic Struktur in Hinblick auf zum Beispiel Skalierbarkeit._

Mein Vorschlag wäre das ein topic welches alle Changes empfängt und weitere topics pro `wiki` erstellt werden. Aktuell enthalten die test daten 63 wikis. Es könnten weitere Wikis hinzukommen. Außerdem kommt noch DLQ Topic und Topics für failed Events hinzu.

**Vorteile:**

- Bereits nach Wiki partitioniert

**Nachteile:**

- Viele Topics erzeugen Overhead (Partitionierung nötig)
- Daten werden getrennt gesendet aber in einer gemeinsamen Tabelle gesammelt

## 2. Daten

|     | $schema                       | id         | type | namespace | title                  | comment                                                                                                                                                      | timestamp  | user        | bot   | minor | patrolled | server_url               | server_name      | server_script_path | wiki         | parsedcomment                                                                                                                                                                                                                                                         | meta_domain      | meta_uri                                             | meta_request_id          | meta_stream            | meta_topic                   | meta_dt              | meta_partition | meta_offset | meta_id                              | length_old | length_new | revision_old | revision_new |
| --- | ----------------------------- | ---------- | ---- | --------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------- | ----------- | ----- | ----- | --------- | ------------------------ | ---------------- | ------------------ | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | ---------------------------------------------------- | ------------------------ | ---------------------- | ---------------------------- | -------------------- | -------------- | ----------- | ------------------------------------ | ---------- | ---------- | ------------ | ------------ |
| 0   | /mediawiki/recentchange/1.0.0 | 1389063095 | edit | 0         | Q104971167             | /_ wbeditentity-update-languages-short:0&#124;&#124;nl _/ nl-description, [[User:Edoderoobot/Set-nl-description&#124;python code]] - chemische samenstelling | 1611249080 | Edoderoobot | True  | False | True      | https://www.wikidata.org | www.wikidata.org | /w                 | wikidatawiki | ‎<span dir="auto"><span class="autocomment">Changed label, description and/or aliases in nl: </span></span> nl-description, <a href="/wiki/User:Edoderoobot/Set-nl-description" title="User:Edoderoobot/Set-nl-description">python code</a> - chemische samenstelling | www.wikidata.org | https://www.wikidata.org/wiki/Q104971167             | YAm1uApAIIEAACcb76EAAAAA | mediawiki.recentchange | eqiad.mediawiki.recentchange | 2021-01-21T17:11:20Z | 0              | 2887301727  | a62392d6-25d3-405c-9d6c-54956eb60a52 | 3781       | 3860       | 1345581201   | 1345601868   |
| 0   | /mediawiki/recentchange/1.0.0 | 116494285  | edit | 0         | Acanthastrea erythraea | [[Wikipedia:Geen samenvatting&#124;Verwijst door]] naar [[Lobophyllia erythraea]]                                                                            | 1611249078 | Kvdrgeus    | False | False | False     | https://nl.wikipedia.org | nl.wikipedia.org | /w                 | nlwiki       | <a href="/wiki/Wikipedia:Geen_samenvatting" title="Wikipedia:Geen samenvatting">Verwijst door</a> naar <a href="/wiki/Lobophyllia_erythraea" title="Lobophyllia erythraea">Lobophyllia erythraea</a>                                                                  | nl.wikipedia.org | https://nl.wikipedia.org/wiki/Acanthastrea_erythraea | YAm1tgpAIHwABCtglGIAAADR | mediawiki.recentchange | eqiad.mediawiki.recentchange | 2021-01-21T17:11:18Z | 0              | 2887301728  | f6acf301-d987-4d7b-85fe-d2c3cb486ffb | 866        | 65         | 48016794     | 58091518     |

## 3. Umsetzung

### 3.1 Kafka Producer

Der Kafka Producer ließt die Daten aus der Datei [de_challenge_sample_data.csv](kafka_producer\data\raw\de_challenge_sample_data.csv) ein und schreibt sie in ein Kafka-Success-Topic und in ein länder spezifisches Kafka-Topic. Die Daten werden dabei in einem zufälligen abstand von 0 bis 1 Sekunde veröffentlicht.

Die ausführliche Dokumentation des Kafka Producers ist [hier](kafka_producer/README.md) zu finden.

### 3.2 Kafka Consumer

Der Kafka Consumer ließt die Daten aus dem Kafka-Success-Topic und dem Kafka-Topic für Wikipedia Deutschland und führt simple aggregationen durch. Die aggregierten Daten werden in einer Datenbank gespeichert.

Die ausführliche Dokumentation des Kafka Consumers ist [hier](kafka_consumer/README.md) zu finden.

## 3.3 Docker-Compose

Um die Kafka-Infrastruktur zu starten, kann das Docker-Compose File [docker-compose.yml](docker-compose.yml) verwendet werden. Es startet einen Zookeeper, einen Kafka-Broker, den Producer und den Consumer.

```bash
docker-compose up -d
```

### 3.4 Zookeeper

Der Zookeeper verwendet das `confluentinc/cp-zookeeper` image und ist über den Port `2181` erreichbar. Die tick time ist auf `2000` gesetzt.

### 3.5 Kafka-Broker

Der Kafka-Broker bekommt die `KAFKA_BROKER_ID` `1` zugewiesen. Als `KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR`, `KAFKA_TRANSACTION_STATE_LOG_MIN_ISR` und `KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR` wurden alle auf `1` gesetzt, da nur ein Broker verwendet wird. Die `KAFKA_ADVERTISED_LISTENERS` wurden auf `PLAINTEXT://broker:29092,PLAINTEXT_HOST://localhost:9092` gesetzt, damit der Broker sowohl im internen Docker-Netz als auch lokal erreichbar ist. `KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS` wurde auf `0` gesetzt, da in diesem Use-Case nur mit einem Consumer gearbeitet wird und ein rebalance so direkt stattfinden kann/soll.

### 3.6 Netzwerk

Die Container sind über das Docker Netzwerk `kafka_network` verbunden um untereinander kommunizieren zu können.

> Besonderheit: **Der Kafka-Broker ist im internen Docker-Netz über `broker:29092` erreichbar. Lokal ist der Broker über `localhost:9092` erreichbar.**
