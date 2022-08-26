from time import sleep
from typing import Callable
import paho.mqtt.client as mqtt

class MqttClient:
    """
    MqttClient class for easier connect and automatic reconnect.

    Place your subscribe calls inside a callback inside your class
    with an object of MqttClient named mqtt_client and then
    set this class attribute on_connected to your callback method.

    Example:

    from mqtt_client import MqttClient

    class ClassName:
        def __init__(self, host: str, port: int) -> None:
            self.__mqtt_client = MqttClient(host, port)
            self.__mqtt_client.on_connected = self.__subscribe_topics
            self.__mqtt_client.connect()

        def __subscribe_topics(self):
            self.__mqtt_client.subscribe("/topic", self.__handler)

        def __handler(self, client, userdata, message) -> None:
            pass
    """

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

        self.mqtt_client = None
        self.is_connected = None
        self.on_connected : Callable = None

        self.reconnect_delay = 10
        self.client_keep_alive_time = 10
        self.polling_delay = 1

    def print(self, msg):
        print(f'[MqttClient]: {msg}')

    def connect(self) -> bool:
        self.print(f'Connecting to MQTT broker (host: {self.host} | port: {self.port})')

        try:
            self.is_connected = None

            if self.mqtt_client is None:
                self.mqtt_client = mqtt.Client(reconnect_on_failure=True)

            self.mqtt_client.on_connect = self.on_connect
            self.mqtt_client.on_disconnect = self.on_disconnect
            self.mqtt_client.reconnect_delay_set(min_delay=1, max_delay=self.reconnect_delay)
            self.mqtt_client.connect(self.host, self.port, self.client_keep_alive_time)
            self.mqtt_client.loop_start()

            while self.is_connected is None:
                sleep(self.polling_delay)
            
            if not self.is_connected:
                sleep(self.reconnect_delay)
                self.connect()
            
            self.print("Connected to mqtt-broker")
            return True
        except Exception:
            sleep(self.reconnect_delay)
            self.print(f'Retrying to connect with mqtt-broker')
            self.connect()

    def on_connect(self, client, userdata, flags, rc):
        self.print(f'Received connect() status [{rc}]')
        self.is_connected = rc == mqtt.MQTT_ERR_SUCCESS
        if self.is_connected and self.on_connected:
            self.on_connected()

    def on_disconnect(self, client, userdata, rc):
        self.print("Client disconnected from mqtt-broker")
        self.is_connected = None

    def publish(self, topic: str, data: str) -> None:
        if self.mqtt_client.is_connected:
            message = self.mqtt_client.publish(topic, data, qos=2)
            message.wait_for_publish()

    def subscribe(self, topic: str, handler: Callable) -> None:
        if self.mqtt_client.is_connected:
            self.mqtt_client.subscribe(topic)
            self.mqtt_client.message_callback_add(topic, handler)
