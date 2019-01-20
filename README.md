# Prometheus MQTT Exporter

A very simple MQTT exporter for Prometheus. This exporter is mostly useful for
pushing retained topics into Prometheus and only a small subset of topics. It
isn't made to push all your topics to Prometheus but for my own needs to
replace a custom Python script and Influxdb.

# Dependencies

* python
* paho-mqtt
* prometheus_client

# Usage

Run the exporter

  python prometheus-mqtt-exporter.py

The default port is 9098, visit metrics [http://localhost:9098/ http://localhost:9098/].

# Configuration

The MQTT server, port and topics to subscribe to are configured in mqtt.yml.
