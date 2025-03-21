from datetime import datetime, timedelta

def get_last_weekday_of_next_month():
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

# Example usage
last_weekday = get_last_weekday_of_next_month()