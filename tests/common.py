"Common tools for testing"

from typing import List, NamedTuple, Optional

from homie_spec.messages import Message


class MessagesAssert(NamedTuple):
    "Set of methods to assert different properties over a list of messages"
    messages: List[Message]

    def exists(
        self,
        topic_parts: List[str],
        exact_payload: Optional[str] = None,
        matches_substring: Optional[str] = None,
        retained: Optional[bool] = None,
        optional: bool = False,
        unique: bool = True,
    ) -> bool:
        """
        Given a list of topic parts, compose it into a proper topic
        and assert if that topic appears in the message list only once.

        If `exact_payload` is provided, check with the *first* message
        with the matching topic, if the payload also matches.

        If `matches_substring` is provided, check with the *first* message
        with the matching topic, if the payload contains said substring.

        If `retained` is provided, check with the *first* message
        with the matching topic, if the payload is retained

        If `optional` is True (default False),
        allow for the topic to be missing.

        If `unique` is True (default True), assert that
        no other message has the same topic.
        """
        composed_topic = self.compose_topic(topic_parts)

        topic_matching_messages = (
            message for message in self.messages if message.topic == composed_topic
        )
        try:
            first_match = next(topic_matching_messages)
        except StopIteration:
            return optional

        if unique:
            try:
                next(topic_matching_messages)
                return False
            except StopIteration:
                ...

        content_match = True
        if retained is not None:
            content_match &= retained == first_match.retained
        if exact_payload is not None:
            content_match &= exact_payload == first_match.payload
        if matches_substring is not None:
            content_match &= matches_substring in first_match.payload
        return content_match

    @staticmethod
    def compose_topic(topic_parts: List[str]) -> str:
        "Creates a topic out of a list of parts, putting a slash when necessary"
        return "/".join((part for part in topic_parts if part))
