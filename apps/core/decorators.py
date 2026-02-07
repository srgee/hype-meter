import time
import logging
import functools
from typing import Any, Callable

# Use specific logger for telemetry
logger = logging.getLogger("apps.telemetry")

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
        
        start_time = time.perf_counter()
        
        try:
            result = func(*args, **kwargs)
            duration = (time.perf_counter() - start_time) * 1000
            
            logger.info("telemetry_request_success", extra={
                "telemetry_type": "provider_call",
                "method": method_name,
                "duration_ms": round(duration, 2),
                "status": "success"
            })
            return result
            
        except Exception as e:
            duration = (time.perf_counter() - start_time) * 1000
            logger.error("telemetry_request_error", exc_info=True, extra={
                "telemetry_type": "provider_call",
                "method": method_name,
                "duration_ms": round(duration, 2),
                "error_type": type(e).__name__,
                "status": "error"
            })
            raise
            
    return wrapper