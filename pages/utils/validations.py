"""
Validation Module

This module provides validation functions for form data.
It includes email validation and field validation for different assessment types.
"""

from pages.utils.constants import INVALID_EMAILS

def validate_email(email):
    """
    Validate if an email is a corporate email (not a personal email).
    
    Args:
        email (str): The email address to validate
        
    Returns:
        bool: True if the email is valid (corporate), False otherwise
    """
    if not email:
        return False
        
    for invalid_domain in INVALID_EMAILS:
        if invalid_domain in email:
            return False
    
    return True

def validate_required_fields(fields, required_fields):
    """
    Validate that all required fields are filled.
    
    Args:
        fields (dict): Dictionary containing form fields
        required_fields (list): List of required field names
        
    Returns:
        list: List of error messages, empty if all validations pass
    """
    error_messages = []
    
    for field_name in required_fields:
        if field_name not in fields:
            error_messages.append(f"The field {field_name} is required.")
            continue
            
        if field_name == "contact_email":
            if not fields[field_name]:
                error_messages.append("The email field is required.")
            elif not validate_email(fields[field_name]):
                error_messages.append("Invalid email, only corporate emails accepted")
        elif not fields[field_name]:
            error_messages.append(f"The field {field_name} is required.")
    
    return error_messages

def validate_fields(fields):
    """
    Validate ICT and FCT assessment fields.
    
    Args:
        fields (dict): Dictionary containing form fields
        
    Returns:
        list: List of error messages, empty if all validations pass
    """
    required_fields = [
        "project_name",
        "contact_name",
        "date",
        "contact_email"
    ]
    
    return validate_required_fields(fields, required_fields)

def validate_fields_iat(fields):
    """
    Validate IAT assessment fields.
    
    Args:
        fields (dict): Dictionary containing form fields
        
    Returns:
        list: List of error messages, empty if all validations pass
    """
    required_fields = [
        "project_name",
        "contact_name",
        "contact_email",
        "customer_name",
        "date"
    ]
    
    return validate_required_fields(fields, required_fields)