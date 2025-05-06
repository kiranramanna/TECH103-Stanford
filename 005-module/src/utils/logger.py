"""
Utility functions for logging and timing.
"""
import time
import functools
import logging
from typing import Callable, Any
from datetime import datetime

# Configure colored logging
class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors."""
    
    COLORS = {
        'DEBUG': '\033[94m',  # Blue
        'INFO': '\033[92m',   # Green
        'WARNING': '\033[93m', # Yellow
        'ERROR': '\033[91m',   # Red
        'CRITICAL': '\033[91m\033[1m', # Bold Red
        'RESET': '\033[0m'    # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with colors."""
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)

# Set up logger
logger = logging.getLogger('hotel_search')
logger.setLevel(logging.INFO)

# Add console handler with colored formatter
console_handler = logging.StreamHandler()
console_handler.setFormatter(ColoredFormatter(
    '%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))
logger.addHandler(console_handler)

def timeit(func: Callable) -> Callable:
    """Decorator to time function execution.
    
    Args:
        func: Function to time
        
    Returns:
        Wrapped function that logs execution time
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        # Log execution time
        duration = end_time - start_time
        logger.info(f"{func.__name__} took {duration:.2f} seconds")
        
        return result
    return wrapper

def log_errors(func: Callable) -> Callable:
    """Decorator to log errors.
    
    Args:
        func: Function to wrap
        
    Returns:
        Wrapped function that logs errors
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper 