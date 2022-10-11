from structlog import get_logger
from structlog.types import FilteringBoundLogger

logger: FilteringBoundLogger = get_logger("simple")

# INFO
logger.info("This is info level log. Used for any business process information", method="main")

# WARNING
logger.warning("This is warning level log. Used for any invalid business process", method="main")

# ERROR
logger.error("This is error level log. Used for any unexpected error happened", method="main")

# CRITICAL
logger.error("This is critical level log. Used for error that shouldn't be happened", method="main")