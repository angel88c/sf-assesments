"""
Dates Information Module

This module provides functions for date calculations and manipulations.
"""

from datetime import datetime, timedelta

def get_date_after_next_working_days(working_days, initial_date=None):
    
    if initial_date is None:
        initial_date = datetime.now()
        
    
    future_date = initial_date
    added_days = 0
    
    while added_days < working_days:
        future_date += timedelta(days=1)
        
        # Check if its a working day (Monday=0 a Friday=4)
        if future_date.weekday() < 5:
            added_days += 1
        
    return future_date

def get_last_weekday_of_next_month():
    """
    Calculate the last weekday (Monday-Friday) of the next month.
    
    Returns:
        datetime: The last weekday of the next month
    """
    # Get today's date
    today = datetime.today()
    
    # Calculate the first day of the next month
    next_month = today.month + 1 if today.month < 12 else 1
    next_year = today.year if today.month < 12 else today.year + 1
    first_day_next_month = datetime(next_year, next_month, 1)
    
    # Get the last day of next month
    if next_month == 12:
        last_day_next_month = datetime(next_year, next_month, 31)
    else:
        last_day_next_month = datetime(next_year, next_month + 1, 1) - timedelta(days=1)

    # Adjust to the last weekday (Monday to Friday)
    while last_day_next_month.weekday() > 4:  # 5=Saturday, 6=Sunday
        last_day_next_month -= timedelta(days=1)
    
    return last_day_next_month



def get_formatted_date(date_obj=None, format_str="%Y-%m-%d"):
    """
    Format a date object as a string.
    
    Args:
        date_obj (datetime, optional): The date to format. Defaults to today.
        format_str (str, optional): The format string. Defaults to "%Y-%m-%d".
        
    Returns:
        str: The formatted date string
    """
    if date_obj is None:
        date_obj = datetime.today()
    
    return date_obj.strftime(format_str)

# Example usage
last_weekday = get_last_weekday_of_next_month()

future_day = get_date_after_next_working_days(6)
print(future_day)