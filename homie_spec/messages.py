"""
Exposes the Message class, that can be used to create MQTT styled messages.
"""

from typing import NamedTuple, Union, Mapping, Optional


class Message(NamedTuple):
    "Simplified object representation of a MQTT message."

    topic_: str
    payload: str
    retained: bool = True
    qos: int = 1
    prefix: Optional[str] = None

    @property
    def topic(self) -> str:
        """
        Consolidates the prefix and the topic into an absolute topic

        >>> Message("topic", payload="", prefix="/homie/device").topic
        '/homie/device/topic'
        """
        if self.prefix:
            topic = f"{self.prefix}/{self.topic_}"
        else:
            topic = self.topic_
        return topic.lower().rstrip("/")

    @property
    def attrs(self) -> Mapping[str, Union[str, bool, int]]:
        """
        Serializes the object conforming it to be used as a MQTT payload

        >>> Message("subject", "body").attrs
        {'topic': 'subject', 'payload': 'body', 'retained': True, 'qos': 1}
        """
        return {
            "topic": self.topic,
            "payload": self.payload,
            "retained": self.retained,
            "qos": self.qos,
        }


Message.topic.__doc__ = "MQTT topic for where the message should be published."
Message.payload.__doc__ = "Attribute used as payload when publishing the message."
Message.retained.__doc__ = (
    "Flag indicating if the message should be retained within the topic."
)
Message.qos.__doc__ = "MQTT Quality of Service for the message."
Message.prefix.__doc__ = (
    "The topic prefix. It's prefixed to the message topic and separated by a slash."
)
