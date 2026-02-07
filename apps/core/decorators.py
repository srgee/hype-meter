import time
import logging
import functools
import inspect
from typing import Any, Callable

# Use specific logger for telemetry
logger = logging.getLogger("apps.telemetry")

# Define slowness threshold for provider's API calls
SLA_THRESHOLD_MS = 2000

def trace_provider_call(func: Callable) -> Callable:
    """
    Decorator to trace provider calls. It logs the duration of the call,
    along with the class and method name. If the call raises an exception,
    it logs the error type and sets the status to "error".
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Identify the class and method e.g GoogleProvider.fetch_score
        class_name = args[0].__class__.__name__ if args else "Unknown"
        method_name = f"{class_name}.{func.__name__}"

        # Smart argument parsing for logging
        # Filter out sensitive keywords such as key, password, token or secret
        filtered_args = ["key", "password", "token", "secret", "self", "cls"]
        try:
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            params = {k: v for k, v in bound_args.arguments.items() if k not in filtered_args}
        except Exception:
            params = {"error": "failed_to_parse_arguments"}


        start_time = time.perf_counter()
        
        try:
            result = func(*args, **kwargs)
            duration = (time.perf_counter() - start_time) * 1000

            log_data = {
                "telemetry_type": "provider_call",
                "method": method_name,
                "params": params,
                "duration_ms": round(duration, 2),
                "status": "success"
            }
            
            if duration > SLA_THRESHOLD_MS:
                log_data["sla_threshold_ms"] = SLA_THRESHOLD_MS
                logger.warning("provider_request_slow", extra=log_data)
            else:
                logger.info("provider_request_success", extra=log_data)
            
            return result
            
        except Exception as e:
            duration = (time.perf_counter() - start_time) * 1000
            logger.error("telemetry_request_error", exc_info=True, extra={
                "telemetry_type": "provider_call",
                "method": method_name,
                "params": params,
                "duration_ms": round(duration, 2),
                "error_type": type(e).__name__,
                "status": "error"
            })
            raise
            
    return wrapper