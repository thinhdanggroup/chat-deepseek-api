class NotLoggedInError(Exception):
    """Exception raised when the user is not logged in."""
    def __init__(self, message="You are not logged in. Please login first"):
        self.message = message
        super().__init__(self.message)

class EmptyEmailOrPasswordError(Exception):
    """Exception raised when the email or password is empty."""
    def __init__(self, message="Email or password cannot be empty"):
        self.message = message
        super().__init__(self.message)
        
class MissingHeaderConfigError(Exception):
    """Exception raised when the custom_headers is missing."""
    def __init__(self, message="custom_headers is missing. Please provide custom_headers"):
        self.message = message
        super().__init__(self.message)