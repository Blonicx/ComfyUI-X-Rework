import traceback
from datetime import datetime

class ErrorHandler:
    def __init__(self):
        self.error_log = []  # Initialize an error log to store error messages
        self.suppressed_errors = set()  # Set of error types to suppress
    
    # Error handling methods#
    def log_error(self, error):
        """Logs the error message with timestamp and traceback."""
        error_message = f"{datetime.now()}: {type(error).__name__}: {error}"
        traceback_details = ''.join(traceback.format_exception(None, error, error.__traceback__))
        self.error_log.append((error_message, traceback_details))
        print(error_message)  # Print error for real-time feedback
    
    def raise_and_log(self, error):
        """Logs the error and raises it unless it's suppressed."""
        if type(error) not in self.suppressed_errors:
            self.log_error(error)
            raise error  # Re-raise the error after logging
        else:
            print(f"Suppressed: {type(error).__name__}: {error}")
    
    def suppress_error(self, error_type):
        """Add an error type to the suppression list."""
        self.suppressed_errors.add(error_type)
    
    def unsuppress_error(self, error_type):
        """Remove an error type from the suppression list."""
        self.suppressed_errors.discard(error_type)
    
    def handle_error(self, error_type, message, retry=False, retries=1):
        """
        Handle errors by logging, retrying, and raising specific errors.
        
        Parameters:
        - error_type: Type of error to raise.
        - message: Error message to log and raise.
        - retry: If True, retries the action upon failure.
        - retries: Number of retries if retry is enabled.
        """
        error_classes = {
            "model": self.Errors.ModelError,
            "utils": self.Errors.UtilsError,
            "image": self.Errors.ImageError,
            "unknown": self.Errors.UnknownError
        }
        
        error_class = error_classes.get(error_type.lower(), self.Errors.UnknownError)
        error = error_class(message)
        
        attempt = 0
        while attempt < retries:
            try:
                if retry and attempt > 0:
                    print(f"Retrying ({attempt}/{retries}) for error: {type(error).__name__}")
                self.raise_and_log(error)
                break
            except error_class as e:
                attempt += 1
                if attempt >= retries:
                    print(f"Failed after {retries} attempts.")
                    self.log_error(e)
                    break

    def get_error_log(self):
        """Returns the list of logged errors with timestamps and tracebacks."""
        return self.error_log
    
    def clear_error_log(self):
        """Clears the error log."""
        self.error_log.clear()
    
    class Errors:
        class ModelError(Exception):
            """Raised when the Node misses a Model."""
            pass
        
        class ImageError(Exception):
            """Raised when an error happens while loading an Image."""
            pass
        
        class UtilsError(Exception):
            """Raised when an error happens in a UtilsNode."""
            pass
        class UnknownError(Exception):
            """Raised when an unknown error occurs."""
            pass