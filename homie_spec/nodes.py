"Exposes the Node class"

from typing import NamedTuple, Any, Mapping, Optional, Iterable
from functools import partial

from homie_spec.messages import Message


class Node(NamedTuple):
    "Object representation of a node according to the Homie topology"

    name: str
    typeOf: str
    properties: Optional[Mapping[str, Any]] = None

    def messages(self, prefix: str) -> Iterable[Message]:
        """
        Yields the messages from the node attributes and from its properties.
        All its messages are prefixed with its only parameter.

        >>> next(Node("A Node!", "node").messages("/prefix")).payload
        'A Node!'
        """

        msg = partial(Message, prefix=prefix)

        yield msg("$name", self.name)
        yield msg("$type", self.typeOf)

        if self.properties:
            payload_properties = ",".join(self.properties.keys())
            yield msg("$properties", payload_properties.lower())

            for property_name, property_ in self.properties.items():
                prop_prefix = "/".join((prefix, property_name))
                yield from property_.messages(prefix=prop_prefix)
        else:
            yield msg("$properties", "")

    def getter_message(self, prop_name: str, prefix: str = "") -> Message:
        """
        Returns the message corresponding to the getter message
        of a given property.

        The property is identified by the parameter `prop_name`.

        Accepts a prefix that is prepended to the message topic.

        >>> from homie_spec.properties import Datatype, Property
        >>> prop = Property("P", lambda: "4", Datatype.INTEGER)
        >>> node = Node("N", "n", {"p": prop})
        >>> msg = node.getter_message("p", prefix="homie/d/n")
        >>> msg.topic
        'homie/d/n/p'
        >>> msg.payload
        '4'

        Raises a ValueError when the property is not among the
        nodes properties.

        ```

        >>> node = Node("N", "n").getter_message("p")
        Traceback (most recent call last):
        ...
        ValueError: Node has no properties

        ```
        """
        prop_name = prop_name.lower()
        if self.properties is None:
            raise ValueError("Node has no properties")

        prop = self.properties.get(prop_name.lower())
        if prop is None:
            raise ValueError(
                " - ".join(
                    [
                        f"Property name not found: '{prop_name}'",
                        f"Valid property paths are {self.properties.keys()}",
                    ]
                )
            )

        message: Message = prop.getter_message(f"{prefix}/{prop_name}")
        return message


Node.name.__doc__ = "Friendly name of the node."
Node.typeOf.__doc__ = "Type of the node."
Node.properties.__doc__ = "Properties the node exposes, separated by , for multiple ones."
