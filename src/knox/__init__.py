__version__ = '0.0.2'
from loguru import logger

from .knox import Knox  # noqa: F401

logger.debug(f'Invoking __init__.py for {__name__}')
