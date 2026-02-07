import logging
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Validation utility

def validate_inputs(inputs):
    """Validates inputs for the maze solver."""
    if not isinstance(inputs, list):
        logging.error("Inputs must be a list.")
        return False
    for input in inputs:
        if not isinstance(input, (int, float)):
            logging.error(f"Invalid input: {input}. Must be an int or a float.")
            return False
    logging.info("Inputs validated successfully.")
    return True

# Performance monitoring utility

def performance_monitor(func):
    """Decorator to monitor performance of functions."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logging.info(f"Function '{func.__name__}' executed in {execution_time:.4f} seconds.")
        return result
    return wrapper
