"Module that contains module-specific hypothesis-strategies for object creation"

from typing import Callable, Any

from hypothesis.strategies import (
    booleans,
    composite,
    dictionaries,
    functions,
    integers,
    sampled_from,
    shared,
    text,
    uuids,
    one_of,
    SearchStrategy,
)

from homie_spec.nodes import Node
from homie_spec.devices import Device
from homie_spec.properties import (
    Property,
    BooleanProperty,
    PercentageProperty,
    Datatype,
    RECOMMENDED_UNITS,
)


Drawable = Callable[[SearchStrategy[Any]], Any]  # pylint: disable=invalid-name


@composite
def properties(draw: Drawable) -> Property:
    "Generates Properties objects"
    return Property(
        name=draw(text()),
        datatype=draw(sampled_from(Datatype)),
        get=draw(functions(like=lambda: "4", returns=shared(text(), key="key"))),
        retained=draw(booleans()),
        settable=draw(booleans()),
        unit=draw(sampled_from(RECOMMENDED_UNITS)),
        formatOf=draw(text()),
    )


@composite
def boolean_properties(draw: Drawable) -> Property:
    "Generates BooleanProperty objects"
    return BooleanProperty(
        name=draw(text()),
        get=draw(
            functions(
                like=lambda: "false",
                returns=shared(
                    booleans().map(lambda boolean: str(boolean).lower()), key="key"
                ),
            )
        ),
        retained=draw(booleans()),
        settable=draw(booleans()),
    )


@composite
def percentage_properties(draw: Drawable) -> Property:
    "Generates PercentageProperty objects"
    return PercentageProperty(
        name=draw(text()),
        get=draw(
            functions(
                like=lambda: "4",
                returns=shared(integers(min_value=0, max_value=100).map(str), key="key"),
            )
        ),
        retained=draw(booleans()),
        settable=draw(booleans()),
    )


@composite
def nodes(draw: Drawable) -> Node:
    "Generates Node objects"
    return Node(
        name=draw(text()),
        typeOf=draw(text()),
        properties=draw(
            dictionaries(
                keys=uuids().map(str),
                values=one_of(
                    properties(), boolean_properties(), percentage_properties()
                ),
            )
        ),
    )


@composite
def devices(draw: Drawable) -> Device:
    "Generates Device objects"
    return Device(
        id=draw(text()),
        name=draw(text()),
        implementation=draw(text()),
        prefix=draw(text()),
        nodes=draw(dictionaries(keys=uuids().map(str), values=nodes())),
    )
