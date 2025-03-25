import logging
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


def handle_exception(exception, error_message, raise_exception=True):
    logger.error(f"{error_message}: {str(exception)}")
    if raise_exception:
        raise ValidationError(detail=error_message)