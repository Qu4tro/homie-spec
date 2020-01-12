"Entrypoint for homie-spec tests"

import os
from datetime import timedelta
from hypothesis import settings

settings.register_profile("ci", max_examples=1000)
settings.register_profile("dev", max_examples=100, deadline=timedelta(milliseconds=500))
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "dev"))
