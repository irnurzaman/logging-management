import logging
from structlog import get_logger, configure, PrintLoggerFactory, make_filtering_bound_logger
from structlog.processors import TimeStamper, StackInfoRenderer, add_log_level
from structlog.contextvars import merge_contextvars
from structlog.dev import ConsoleRenderer, set_exc_info
from structlog.types import FilteringBoundLogger

processors = [merge_contextvars, add_log_level, StackInfoRenderer(), set_exc_info, TimeStamper("iso"), ConsoleRenderer(colors=False)]
configure(processors=processors,
          wrapper_class=make_filtering_bound_logger(logging.NOTSET),
          logger_factory=PrintLoggerFactory(),
          context_class=dict)
logger: FilteringBoundLogger = get_logger("simple")

# INFO
logger.info("This is info level log. Used for any business process information", method="main")

# WARNING
logger.warning("This is warning level log. Used for any invalid business process", method="main")

# ERROR
logger.error("This is error level log. Used for any unexpected error happened", method="main")

# CRITICAL
logger.error("This is critical level log. Used for error that shouldn't be happened", method="main")