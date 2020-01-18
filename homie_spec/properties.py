"""
Exposes the Property class, Datatype and multiple partial constructors
"""

from enum import Enum, auto
from typing import NamedTuple, Callable, Optional, Iterable
from functools import partial

from homie_spec.messages import Message


class Datatype(Enum):
    "Enum representation of the different values, the `$datatype` attribute can take"

    INTEGER = auto()
    FLOAT = auto()
    BOOLEAN = auto()
    STRING = auto()
    ENUM = auto()
    COLOR = auto()

    @property
    def payload(self) -> str:
        """
        Serializes the object conforming it to be used inside a MQTT payload

        >>> Datatype.INTEGER.payload
        'integer'

        >>> Datatype.FLOAT.payload
        'float'
        """
        return self.name.lower()  # pylint: disable=no-member


__pdoc__ = {
    "Datatype.INTEGER": "Integer type.",
    "Datatype.FLOAT": "Float type.",
    "Datatype.BOOLEAN": "Boolean type.",
    "Datatype.STRING": "String type.",
    "Datatype.ENUM": "Enum type.",
    "Datatype.COLOR": "Color type.",
}


class Property(NamedTuple):
    "Object representation of a property according to the Homie topology"

    name: str
    get: Callable[[], str]

    datatype: Datatype = Datatype.STRING
    set: Optional[Callable[[str], None]] = None

    retained: Optional[bool] = None
    settable: Optional[bool] = None

    unit: Optional[str] = None
    formatOf: Optional[str] = None

    def messages(self, prefix: str) -> Iterable[Message]:
        """
        Yields the messages from the property attributes.
        All its messages are prefixed with its only parameter.

        >>> prop = Property("A Property!", get=lambda: "hello world")
        >>> next(prop.messages("/prefix")).payload
        'A Property!'
        """
        msg = partial(Message, prefix=prefix)

        yield msg("$name", self.name)
        yield msg("$datatype", self.datatype.payload)

        if self.retained is not None:
            retained = "true" if self.retained else "false"
            yield msg("$retained", retained)

        if self.settable is not None:
            settable = "true" if self.settable else "false"
            yield msg("$settable", settable)

        if self.unit is not None:
            yield msg("$unit", self.unit)
        if self.formatOf is not None:
            yield msg("$format", self.formatOf)

    def getter_message(self, prefix: str) -> Message:
        """
        Calls the property getter and returns its respective message

        >>> prop = Property("P", get=lambda: "4", datatype=Datatype.INTEGER)
        >>> msg = prop.getter_message("homie/device/node/prop")
        >>> msg.topic
        'homie/device/node/prop'
        >>> msg.payload
        '4'
        """
        msg = partial(Message, prefix=prefix)
        retained = True if self.retained is None else self.retained

        return msg("", self.get(), retained=retained)

    def setter_message(self, prefix: str, payload: str = "") -> Optional[Message]:
        """
        Creates the necessary message to call the property setter.
        Returns None if the property is not settable.

        >>> prop = Property("P", get=lambda: "4", datatype=Datatype.INTEGER, settable=False)
        >>> prop.setter_message("homie/device/node/prop", "2") is None
        True

        >>> prop = Property("P", get=lambda: "4", datatype=Datatype.INTEGER, settable=True)
        >>> msg = prop.setter_message("homie/device/node/prop", "2")
        >>> msg.topic
        'homie/device/node/prop/set'
        >>> msg.payload
        '2'
        """
        if self.settable is not True:
            return None

        msg = partial(Message, prefix=prefix)

        return msg("set", payload)


PercentageProperty = partial(  # pylint: disable=invalid-name
    Property, datatype=Datatype.INTEGER, formatOf="0:100", unit="%"
)
BooleanProperty = partial(  # pylint: disable=invalid-name
    Property, datatype=Datatype.BOOLEAN
)


Property.name.__doc__ = "Friendly name of the property."
Property.datatype.__doc__ = "The property's datatype."
Property.formatOf.__doc__ = "Specifies restrictions or options for the given data type"
Property.settable.__doc__ = "Settable (true). Default is read-only (false)"
Property.retained.__doc__ = "Non-retained (false). The spec Default is Retained (true)."
Property.unit.__doc__ = "Optional unit of this property. Should follow a accepted value."


RECOMMENDED_UNITS = [
    "°C",
    "°F",
    "°",
    "L",
    "gal",
    "V",
    "W",
    "A",
    "%",
    "m",
    "ft",
    "Pa",
    "psi",
    "#",
]
