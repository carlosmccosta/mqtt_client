# mqtt_client

MqttClient class for easier connect and automatic reconnect.

Place your subscribe calls inside a callback inside your class
with an object of MqttClient named mqtt_client and then
set this class attribute on_connected to your callback method.

Example:

```python
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
```

## Compilation

```
python setup.py bdist_wheel
pip3 install --force-reinstall --upgrade dist/mqtt_client-1.0.0-py3-none-any.whl
```