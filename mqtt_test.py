import time

from umqtt.robust import MQTTClient


class TestMQTT:

    def __init__(self, client_id, server, topic=None, **kwargs):
        self.client = MQTTClient(client_id, server, **kwargs)
        if not topic:
            self.topic = 'test/%s/hello' % self.client.client_id
        else:
            self.topic = topic

        self.client.connect()

    def sayHello(self):
        self.client.publish(self.topic, "World")

    def start(self, interval=60):
        while True:
            self.sayHello()
            time.sleep(interval)

