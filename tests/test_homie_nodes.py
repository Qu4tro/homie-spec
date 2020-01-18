"Node testing module"

from hypothesis import given, example
from hypothesis.strategies import text

from homie_spec.nodes import Node

from .generic import nodes
from .common import MessagesAssert
from .test_homie_properties import test_generic_property_messages, property_message_count


@given(nodes(), text())
@example(node=Node(name="Mock Node", typeOf="mock"), prefix="/homie/device")
def test_generic_node_messages(node: Node, prefix: str) -> None:
    "Assert multiple properties given a generic node and a topic prefix"

    prefix = prefix.lower()
    messages = list(node.messages(prefix))
    msg = MessagesAssert(messages=messages)

    def number_of_node_messages_match() -> None:
        "Assert that the message count match the expected number"
        assert len(messages) == node_messages_count(node)

    def message_prefix_match() -> None:
        "Assert all messages start with the expected topic prefix"
        for msg in messages:
            assert msg.topic.startswith(prefix)

    def required_attributes_match() -> None:
        """
        Assert that all required attributes are present
        and that their payload match the expected value
        """
        assert msg.exists(topic_parts=[prefix, "$name"], exact_payload=node.name)
        assert msg.exists(topic_parts=[prefix, "$type"], exact_payload=node.typeOf)
        if node.properties:
            for prop in node.properties:
                assert msg.exists(
                    topic_parts=[prefix, "$properties"], matches_substring=prop
                )
        else:
            assert msg.exists(topic_parts=[prefix, "$properties"], exact_payload="")

    def getter_message_match() -> None:
        "Assert that the getter messages of all properties matches"

        if not node.properties:
            return None

        for prop_name, prop in node.properties.items():
            path = f"{prefix}/{node.name}"
            msg = node.getter_message(prop_name, prefix=path)

            assert msg.topic == f"{prefix}/{node.name}/{prop_name}".lower()
            assert msg.payload == str(prop.get())
            assert msg.qos == 1
            assert msg.retained == prop.retained

        return None

    def properties_valid() -> None:
        "Call test_generic_property_messages to test children properties"
        check_property = (
            test_generic_property_messages.hypothesis.inner_test  # type: ignore
        )
        if node.properties:
            for prop in node.properties.values():
                check_property(prop, prefix)

    number_of_node_messages_match()
    message_prefix_match()
    required_attributes_match()
    getter_message_match()
    properties_valid()


def node_messages_count(node: Node) -> int:
    "Counts the number of messages a certain node will send for broadcasting"
    count = len(["$name", "$type", "$properties"])
    if node.properties:
        count += sum(property_message_count(prop) for prop in node.properties.values())
    return count
