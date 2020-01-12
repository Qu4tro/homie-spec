"Common tools for testing"

from typing import List, NamedTuple, Optional

from homie_spec.messages import Message


class MessagesAssert(NamedTuple):
    "Set of methods to assert different properties over a list of messages"
    messages: List[Message]

    def exists(
        self,
        topic_parts: List[str],
        matches_payload: Optional[str] = None,
        matches_substring: Optional[str] = None,
        optional: bool = False,
        unique: bool = True,
    ) -> bool:
        """
        Given a list of topic parts, compose it into a proper topic
        and assert if that topic appears in the message list only once.

        If `matches_payload` is provided, check with the *first* message
        with the matching topic, if the payload also matches.

        If `matches_substring` is provided, check with the *first* message
        with the matching topic, if the payload contains said substring.

        If `optional` is True (default False),
        allow for the topic to be missing.

        If `unique` is True (default True), assert that
        no other message has the same topic.
        """
        composed_topic = self.compose_topic(topic_parts)
        found_once = False
        for message in self.messages:
            if message.topic == composed_topic:
                if found_once and unique:
                    return False

                found_once = True
                if matches_payload is not None:
                    return message.payload == matches_payload
                if matches_substring is not None:
                    return matches_substring in message.payload

        if not optional and not found_once:
            return False

        return True

    @staticmethod
    def compose_topic(topic_parts: List[str]) -> str:
        "Creates a topic out of a list of parts, putting a slash when necessary"
        return "/".join((part for part in topic_parts if part))
