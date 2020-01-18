"homie-spec is a Python library that handles the v4 Homie Convention."

from homie_spec.devices import Device  # noqa
from homie_spec.nodes import Node  # noqa
from homie_spec.properties import Property  # noqa
from homie_spec.messages import Message  # noqa


def broadcast_message(level: str, payload: str, homie_prefix: str = "homie") -> Message:
    """
    Homie defines a broadcast channel, so a controller is able
    to broadcast a message to all Homie devices.

    >>> broadcast_message("coup", "Goverment detected!").attrs
    {'topic': 'homie/$broadcast/coup', 'payload': 'Goverment detected!', 'retained': True, 'qos': 1}
    """
    return Message(level, payload, prefix=f"{homie_prefix}/$broadcast")
