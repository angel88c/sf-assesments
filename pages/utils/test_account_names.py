"""
Test Account Names Module

This module provides functions for retrieving account names from a local file.
"""

import os

# Path to the accounts file
ACCOUNTS_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "accounts.txt")

def get_account_names_from_local_file():
    """
    Read account names from a local file.
    
    Returns:
        list: List of account names, including "Other" if not present
    """
    try:
        with open(ACCOUNTS_FILE_PATH, mode='r') as file:
            account_names = [line.rstrip('\n') for line in file.readlines()]
        
        # Add "Other" option if not present
        if "Other" not in account_names:
            account_names.append("Other")
            
        return account_names
    except Exception as e:
        # Return empty list if file doesn't exist or can't be read
        return []

def get_account_names():
    """
    Get account names, either from Salesforce or from local file.
    
    Returns:
        list: List of account names
    """
    # Try to get accounts from local file first
    account_names = get_account_names_from_local_file()
    
    # If local file is empty, return a default list
    if not account_names:
        return ["Other"]
    
    return account_names

if __name__ == "__main__":
    print(get_account_names())