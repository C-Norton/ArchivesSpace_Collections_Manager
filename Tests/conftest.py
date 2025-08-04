import logging
import pytest


@pytest.fixture(autouse=True)
def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG, format="%(levelname)s:%(name)s:%(message)s"
    )
