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
            yield msg("$properties", ",".join(self.properties.keys()))

            for property_name, property_ in self.properties.items():
                prefix = "/".join((prefix, property_name))
                yield from property_.messages(prefix=prefix)
        else:
            yield msg("$properties", "")


Node.name.__doc__ = "Friendly name of the node."
Node.typeOf.__doc__ = "Type of the node."
Node.properties.__doc__ = "Properties the node exposes, separated by , for multiple ones."
