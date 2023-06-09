# Exxeta Kafka Challenge 2023

> Docu in german

## Aufgabe

Entwicklung eines Kafka-Producers und Kafka-Consumers welche mock Wikipedia Daten verarbeiten. Der Kafka-Producer soll die Daten in ein Kafka-Topic schreiben und der Kafka-Consumer soll die Daten aus dem Kafka-Topic lesen und simple aggregationen durchführen.

## Daten

|     | $schema                       | id         | type | namespace | title                  | comment                                                                                                                                                      | timestamp  | user        | bot   | minor | patrolled | server_url               | server_name      | server_script_path | wiki         | parsedcomment                                                                                                                                                                                                                                                         | meta_domain      | meta_uri                                             | meta_request_id          | meta_stream            | meta_topic                   | meta_dt              | meta_partition | meta_offset | meta_id                              | length_old | length_new | revision_old | revision_new |
| --- | ----------------------------- | ---------- | ---- | --------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------- | ----------- | ----- | ----- | --------- | ------------------------ | ---------------- | ------------------ | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | ---------------------------------------------------- | ------------------------ | ---------------------- | ---------------------------- | -------------------- | -------------- | ----------- | ------------------------------------ | ---------- | ---------- | ------------ | ------------ |
| 0   | /mediawiki/recentchange/1.0.0 | 1389063095 | edit | 0         | Q104971167             | /_ wbeditentity-update-languages-short:0&#124;&#124;nl _/ nl-description, [[User:Edoderoobot/Set-nl-description&#124;python code]] - chemische samenstelling | 1611249080 | Edoderoobot | True  | False | True      | https://www.wikidata.org | www.wikidata.org | /w                 | wikidatawiki | ‎<span dir="auto"><span class="autocomment">Changed label, description and/or aliases in nl: </span></span> nl-description, <a href="/wiki/User:Edoderoobot/Set-nl-description" title="User:Edoderoobot/Set-nl-description">python code</a> - chemische samenstelling | www.wikidata.org | https://www.wikidata.org/wiki/Q104971167             | YAm1uApAIIEAACcb76EAAAAA | mediawiki.recentchange | eqiad.mediawiki.recentchange | 2021-01-21T17:11:20Z | 0              | 2887301727  | a62392d6-25d3-405c-9d6c-54956eb60a52 | 3781       | 3860       | 1345581201   | 1345601868   |
| 0   | /mediawiki/recentchange/1.0.0 | 116494285  | edit | 0         | Acanthastrea erythraea | [[Wikipedia:Geen samenvatting&#124;Verwijst door]] naar [[Lobophyllia erythraea]]                                                                            | 1611249078 | Kvdrgeus    | False | False | False     | https://nl.wikipedia.org | nl.wikipedia.org | /w                 | nlwiki       | <a href="/wiki/Wikipedia:Geen_samenvatting" title="Wikipedia:Geen samenvatting">Verwijst door</a> naar <a href="/wiki/Lobophyllia_erythraea" title="Lobophyllia erythraea">Lobophyllia erythraea</a>                                                                  | nl.wikipedia.org | https://nl.wikipedia.org/wiki/Acanthastrea_erythraea | YAm1tgpAIHwABCtglGIAAADR | mediawiki.recentchange | eqiad.mediawiki.recentchange | 2021-01-21T17:11:18Z | 0              | 2887301728  | f6acf301-d987-4d7b-85fe-d2c3cb486ffb | 866        | 65         | 48016794     | 58091518     |

## Umsetzung

### Kafka Producer

Der Kafka Producer ließt die Daten aus der Datei [de_challenge_sample_data.csv](kafka_producer\data\raw\de_challenge_sample_data.csv) ein und schreibt sie in ein Kafka-Success-Topic und in ein länder spezifisches Kafka-Topic. Die Daten werden dabei in einem zufälligen abstand von 0 bis 1 Sekunde veröffentlicht.

Die ausführliche Dokumentation des Kafka Producers ist [hier](kafka_producer/README.md) zu finden.

### Kafka Consumer

Der Kafka Consumer ließt die Daten aus dem Kafka-Success-Topic und dem Kafka-Topic für Wikipedia Deutschland und führt simple aggregationen durch. Die aggregierten Daten werden in einer Datenbank gespeichert.

Die ausführliche Dokumentation des Kafka Consumers ist [hier](kafka_consumer/README.md) zu finden.

## Docker-Compose

Um die Kafka-Infrastruktur zu starten, kann das Docker-Compose File [docker-compose.yml](docker-compose.yml) verwendet werden. Es startet einen Zookeeper, einen Kafka-Broker, den Producer und den Consumer.

```bash
docker-compose up -d
```

### Zookeeper

Der Zookeeper verwendet das `confluentinc/cp-zookeeper` image und ist über den Port `2181` erreichbar. Die tick time ist auf `2000` gesetzt.

### Kafka-Broker

Der Kafka-Broker bekommt die `KAFKA_BROKER_ID` `1` zugewiesen. Als `KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR`, `KAFKA_TRANSACTION_STATE_LOG_MIN_ISR` und `KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR` wurden alle auf `1` gesetzt, da nur ein Broker verwendet wird. Die `KAFKA_ADVERTISED_LISTENERS` wurden auf `PLAINTEXT://broker:29092,PLAINTEXT_HOST://localhost:9092` gesetzt, damit der Broker sowohl im internen Docker-Netz als auch lokal erreichbar ist. `KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS` wurde auf `0` gesetzt, da in diesem Use-Case nur mit einem Consumer gearbeitet wird und ein rebalance so direkt stattfinden kann/soll.

### Netzwerk

Die Container sind über das Docker Netzwerk `kafka_network` verbunden um untereinander kommunizieren zu können.

> Besonderheit: **Der Kafka-Broker ist im internen Docker-Netz über `broker:29092` erreichbar. Lokal ist der Broker über `localhost:9092` erreichbar.**
