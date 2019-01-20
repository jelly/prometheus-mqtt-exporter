#!/usr/bin/python

import argparse

from wsgiref.simple_server import make_server

from yaml import safe_load
from paho.mqtt import subscribe
from prometheus_client import make_wsgi_app, Metric, REGISTRY


PORT = 9098
CONF = '/etc/prometheus/mqtt.yaml'
CLIENT_ID = 'prometheus-mqtt-exporter'
KEEPALIVE = 5


class MQTTCollector():

    def __init__(self, data):
        self.server = data['server']
        self.port = data['port']
        if not data['topics']:
            self.topics = ['#']
        else:
            self.topics = data['topics']

    def collect(self):
        messages = subscribe.simple(self.topics, hostname=self.server, port=self.port,
                                    retained=True, msg_count=len(self.topics), keepalive=KEEPALIVE)
        for message in messages:
            if message.topic.startswith('/'):
                topic = message.topic[1:]
            topic = topic.replace('/', '_')
            metric = Metric(topic, f'mqtt topic {message.topic}', 'gauge')
            # TODO: not everything is an float
            metric.add_sample(topic, value=float(message.payload), labels={})
            yield metric


def main():
    parser = argparse.ArgumentParser(description='MQTT exporter for Prometheus')
    parser.add_argument('-p', '--port', help=f'exporter exposed port (default {PORT})', type=int, default=PORT)
    parser.add_argument('-c', '--conf', help=f'configuration file (default {CONF}', type=argparse.FileType('r'), default=CONF)
    args = parser.parse_args()

    data = safe_load(args.conf)

    REGISTRY.register(MQTTCollector(data))

    app = make_wsgi_app()
    httpd = make_server('', args.port, app)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
