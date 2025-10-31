import logging
import logging.config

import structlog
import yaml
from opentelemetry import trace

# Имя сервиса в логах и метриках
SERVICE_NAME = "aioffice"

def _add_trace_ids(logger, method_name, event_dict):
    span = trace.get_current_span()
    ctx = span.get_span_context()
    if ctx is not None and ctx.is_valid:
        event_dict["trace_id"] = format(ctx.trace_id, "032x")
        event_dict["span_id"] = format(ctx.span_id, "016x")
    else:
        event_dict["trace_id"] = None
        event_dict["span_id"] = None

    event_dict["service"] = SERVICE_NAME
    return event_dict

def configure_logging():
    # загрузить logging.yaml и применить dictConfig
    with open("observability/logging.yaml", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    logging.config.dictConfig(cfg)

    structlog.configure(
        processors=[
            _add_trace_ids,
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso", utc=True, key="ts"),
            structlog.stdlib.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger("aioffice")
