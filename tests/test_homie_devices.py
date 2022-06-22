"Device testing module"

from hypothesis import example, given

from homie_spec.devices import HOMIE_VERSION, Device
from homie_spec.nodes import Node

from .common import MessagesAssert
from .generic import devices
from .test_homie_nodes import node_messages_count, test_generic_node_messages

EXAMPLE_DEVICE = Device(id="mock", name="Mock Device")

NODE1 = Node(name="light", typeOf="switch")
NODE2 = Node(name="socket", typeOf="power")
EXAMPLE_DEVICE_W_NODES = Device(
    id="mock", name="Mock Device", nodes={"Light": NODE1, "Socket": NODE2}
)


@given(devices())
@example(device=EXAMPLE_DEVICE)
def test_device_messages(device: Device) -> None:
    """
    Assert multiple properties given a device.

    The properties tested within can hold even
    with devices where its validation fail.
    """

    prefix = (device.prefix + "/" + device.id).lower()
    messages = list(device.messages())
    msg = MessagesAssert(messages=messages)

    def number_of_device_messages_match() -> None:
        "Assert that the message count match the expected number"
        assert len(messages) == number_of_messages_for_device(device)

    def message_prefix_match() -> None:
        "Assert that all messages start with the expected topic prefix"
        for msg in messages:
            assert msg.topic.startswith(prefix)

    def required_attributes_match() -> None:
        """
        Assert that all required attributes are present
        and that their payload match the expected value
        """
        assert msg.exists(topic_parts=[prefix, "$name"], exact_payload=device.name)
        assert msg.exists(topic_parts=[prefix, "$homie"], exact_payload=HOMIE_VERSION)
        assert msg.exists(
            topic_parts=[prefix, "$implementation"], exact_payload=device.implementation
        )

        if device.nodes:
            for node in device.nodes:
                assert msg.exists(
                    topic_parts=[prefix, "$nodes"], matches_substring=node
                )
        else:
            assert msg.exists(topic_parts=[prefix, "$nodes"], exact_payload="")

    def optional_attributes_match() -> None:
        """
        Assert that ther payload match the expected value
        for the optional attributes that are present
        """
        assert msg.exists(
            topic_parts=[prefix, "$extensions"],
            exact_payload=str(device.extensions),
            optional=True,
        )

    def state_change_match() -> None:
        "Assert that the state attribute changes as expected"

        assert messages[0].topic == f"{prefix}/$state"
        assert messages[-1].topic == f"{prefix}/$state"
        assert messages[-1].payload == "ready"
        assert msg.exists(
            topic_parts=[prefix, "$state"], exact_payload="init", unique=False
        )

    def getter_message_match() -> None:
        "Assert that the getter messages of all properties matches"

        if not device.nodes:
            return None

        n_properties = 0
        for node_name, node in device.nodes.items():
            if not node.properties:
                continue

            for prop_name, prop in node.properties.items():
                n_properties += 1
                path = f"{node_name}/{prop_name}"
                msg = device.getter_message(path)

                assert msg.topic == f"{prefix}/{node_name}/{prop_name}".lower()
                assert msg.payload == str(prop.get())
                assert msg.qos == 1
                assert msg.retained == prop.retained

        return None

    def nodes_valid() -> None:
        "Call test_generic_node_messages to test children nodes"
        check_property = test_generic_node_messages.hypothesis.inner_test  # type: ignore
        if device.nodes:
            for node in device.nodes.values():
                check_property(node, prefix)

    number_of_device_messages_match()
    message_prefix_match()
    required_attributes_match()
    optional_attributes_match()
    state_change_match()
    nodes_valid()
    getter_message_match()


def number_of_messages_for_device(device: Device) -> int:
    "Counts the number of messages a certain device will send for broadcasting"
    count = len(["$state", "$name", "$homie", "$implementation", "$nodes", "$state"])
    if device.extensions:
        count += 1
    if device.nodes:
        count += sum(node_messages_count(node) for node in device.nodes.values())
    return count


@given(devices())
@example(device=EXAMPLE_DEVICE_W_NODES)
def test_node_path_inside_device(device: Device) -> None:
    """check if the device nodes have the correct path

    expects a certain amount of messages
    for the path of the given nodes
    """
    prefix = device.prefix + "/" + device.id
    messages = list(device.messages())

    nodes = []
    # this test makes only sense if the device has nodes
    if device.nodes:
        for (node, contens) in device.nodes.items():
            nodes.append({"count": 0, "path": f"{prefix}/{node}", "obj": contens})

        for msg in messages:
            for node in nodes:
                if msg.prefix.startswith(node["path"]):
                    node["count"] += 1

        for node in nodes:
            print(f"current path: {node['path']}")
            assert node["count"] == node_messages_count(node=node["obj"])


@given(devices())
@example(device=EXAMPLE_DEVICE_W_NODES)
def test_nodes_lowercase(device: Device) -> None:
    """check if $nodes are in lowercase"""
    messages = list(device.messages())

    for msg in messages:
        if msg.topic.endswith("$nodes") and msg.payload:
            assert msg.payload.islower()
            # device.messages has only one $nodes topic
            break
