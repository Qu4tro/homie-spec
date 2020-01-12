"Property testing module"

from hypothesis import given, example
from hypothesis.strategies import text

from homie_spec.properties import Datatype, Property, BooleanProperty, PercentageProperty

from .generic import properties, boolean_properties, percentage_properties
from .common import MessagesAssert


@given(properties(), text())
@example(
    prop=Property(name="Mock Property", datatype=Datatype.INTEGER, get=lambda: "4"),
    prefix="/homie/device/node/property",
)
def test_generic_property_messages(prop: Property, prefix: str) -> None:
    "Assert multiple properties given a generic property and a topic prefix"

    prefix = prefix.lower().rstrip("/")
    messages = list(prop.messages(prefix))
    msg = MessagesAssert(messages=messages)

    def number_of_property_messages_match() -> None:
        "Assert that the message count match the expected number"
        assert len(messages) == property_message_count(prop)

    def message_prefix_match() -> None:
        "Assert all messages start with the expected topic prefix"
        for msg in messages:
            assert msg.topic.startswith(prefix)

    def required_properties_attributes_match() -> None:
        """
        Assert that all required attributes are present
        and that their payload match the expected value
        """
        assert msg.exists(topic_parts=[prefix, "$name"], matches_payload=prop.name)

        datatype = prop.datatype.name.lower()
        assert msg.exists(topic_parts=[prefix, "$datatype"], matches_payload=datatype)
        assert datatype in ["integer", "float", "boolean", "string", "enum", "color"]

    def optional_properties_attributes_match() -> None:
        """
        Assert that ther payload match the expected value
        for the optional attributes that are present
        """
        assert msg.exists(
            topic_parts=[prefix, "$retained"],
            matches_payload=str(prop.retained).lower(),
            optional=True,
        )

        assert msg.exists(
            topic_parts=[prefix, "$settable"],
            matches_payload=str(prop.settable).lower(),
            optional=True,
        )

        assert msg.exists(
            topic_parts=[prefix, "$unit"], matches_payload=prop.unit, optional=True
        )
        assert msg.exists(
            topic_parts=[prefix, "$format"], matches_payload=prop.formatOf, optional=True
        )

    def getter_message_match() -> None:
        "Assert that the getter message has the expected topic and payload"
        assert MessagesAssert(messages=[prop.getter_message(prefix)]).exists(
            topic_parts=[prefix], matches_payload=prop.get()
        )

    def setter_message_match() -> None:
        "Assert that the setter message has the expected topic and payload"
        payload = str(prop.get())
        message = prop.setter_message(prefix, payload)
        if prop.settable is True:
            assert message is not None
            if not (
                MessagesAssert(messages=[message]).exists(
                    topic_parts=[prefix, "set"], matches_payload=payload
                )
            ):
                __import__("pdb").set_trace()
        else:
            assert message is None

    number_of_property_messages_match()
    message_prefix_match()
    required_properties_attributes_match()
    optional_properties_attributes_match()
    getter_message_match()
    setter_message_match()


@given(boolean_properties(), text())
@example(
    prop=BooleanProperty(name="Mock Property", get=lambda: "true"),
    prefix="/homie/device/node/property",
)
def test_generic_boolean_properties(prop: Property, prefix: str) -> None:
    "Use test_generic_property_messages to test BooleanProperty"
    test_generic_property_messages.hypothesis.inner_test(  # type: ignore
        prop, prefix
    )


@given(percentage_properties(), text())
@example(
    prop=PercentageProperty(name="Mock Property", get=lambda: "0"),
    prefix="/homie/device/node/property",
)
def test_generic_percentage_properties(prop: Property, prefix: str) -> None:
    "Use test_generic_property_messages to test PercentageProperty"
    test_generic_property_messages.hypothesis.inner_test(  # type: ignore
        prop, prefix
    )


def property_message_count(prop: Property) -> int:
    "Counts the number of messages a certain property will send for broadcasting"
    count = len(["$name", "$datatype"])
    if prop.retained is not None:
        count += 1
    if prop.settable is not None:
        count += 1
    if prop.unit is not None:
        count += 1
    if prop.formatOf is not None:
        count += 1
    return count
