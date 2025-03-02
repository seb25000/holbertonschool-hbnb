import re
from functools import wraps

class ValidationError(Exception):
    """Exception raised for validation errors."""
    pass

class Validator:
    """Centralized validation service for the application."""
    
    @staticmethod
    def validate_required_fields(data, required_fields):
        """Validate that all required fields are present in the data.
        
        Args:
            data (dict): The data to validate
            required_fields (list): List of required field names
            
        Raises:
            ValidationError: If any required field is missing
        """
        missing = [field for field in required_fields if field not in data]
        if missing:
            raise ValidationError(f"Missing required fields: {', '.join(missing)}")
    
    @staticmethod
    def validate_string(value, field_name, min_length=1, max_length=None):
        """Validate a string field.
        
        Args:
            value: The value to validate
            field_name (str): Name of the field for error messages
            min_length (int): Minimum length of the string
            max_length (int): Maximum length of the string
            
        Raises:
            ValidationError: If validation fails
        """
        if not value or not isinstance(value, str):
            raise ValidationError(f"{field_name} is required and must be a string")
        
        if len(value) < min_length:
            raise ValidationError(f"{field_name} must be at least {min_length} characters long")
            
        if max_length and len(value) > max_length:
            raise ValidationError(f"{field_name} must not exceed {max_length} characters")
    
    @staticmethod
    def validate_email(email):
        """Validate email format.
        
        Args:
            email (str): The email to validate
            
        Raises:
            ValidationError: If validation fails
        """
        if not email or not isinstance(email, str):
            raise ValidationError("Email is required and must be a string")
        
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email):
            raise ValidationError("Invalid email format")
    
    @staticmethod
    def validate_password(password, min_length=8):
        """Validate password strength.
        
        Args:
            password (str): The password to validate
            min_length (int): Minimum length of the password
            
        Raises:
            ValidationError: If validation fails
        """
        if not password or not isinstance(password, str):
            raise ValidationError("Password is required and must be a string")
        
        if len(password) < min_length:
            raise ValidationError(f"Password must be at least {min_length} characters long")
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter")
        
        if not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain at least one digit")
    
    @staticmethod
    def validate_number(value, field_name, min_value=None, max_value=None, integer=False):
        """Validate a numeric field.
        
        Args:
            value: The value to validate
            field_name (str): Name of the field for error messages
            min_value: Minimum allowed value
            max_value: Maximum allowed value
            integer (bool): Whether the value must be an integer
            
        Raises:
            ValidationError: If validation fails
        """
        try:
            if integer:
                value = int(value)
            else:
                value = float(value)
        except (TypeError, ValueError):
            raise ValidationError(f"{field_name} must be a {'integer' if integer else 'number'}")
        
        if min_value is not None and value < min_value:
            raise ValidationError(f"{field_name} must be at least {min_value}")
            
        if max_value is not None and value > max_value:
            raise ValidationError(f"{field_name} must not exceed {max_value}")
        
        return value
    
    @staticmethod
    def validate_coordinates(latitude, longitude):
        """Validate geographic coordinates.
        
        Args:
            latitude (float): The latitude to validate
            longitude (float): The longitude to validate
            
        Raises:
            ValidationError: If validation fails
        """
        try:
            lat = float(latitude)
            lon = float(longitude)
            
            if not (-90.0 <= lat <= 90.0):
                raise ValidationError("Latitude must be between -90 and 90")
                
            if not (-180.0 <= lon <= 180.0):
                raise ValidationError("Longitude must be between -180 and 180")
                
            return lat, lon
        except (TypeError, ValueError):
            raise ValidationError("Coordinates must be valid numbers")

def validate_request(required_fields=None):
    """Decorator for validating request data.
    
    Args:
        required_fields (list): List of required field names
        
    Returns:
        function: Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract request data from the function arguments
            # This assumes the request data is passed as the first argument after 'self'
            if len(args) > 1:
                data = args[1]
            else:
                data = kwargs.get('data', {})
            
            # Validate required fields
            if required_fields:
                Validator.validate_required_fields(data, required_fields)
            
            # Call the original function
            return func(*args, **kwargs)
        return wrapper
    return decorator 
