"Introduces pytest fixtures that are necessary to run the test suite."

import os
from datetime import timedelta

import pytest  # type: ignore
from hypothesis import settings


@pytest.fixture(scope="session", autouse=True)
def load_env() -> None:
    "Fixtures to load the hypothesis profile inside for all tests"
    settings.register_profile("ci", max_examples=200, deadline=None)
    settings.register_profile(
        "dev", max_examples=10, deadline=timedelta(milliseconds=500)
    )
    settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "dev"))
