"""
Salesforce Service Module

This module provides a service layer for Salesforce operations.
It encapsulates all Salesforce API interactions with proper error handling.
"""

import time
import requests
import functools
import streamlit as st
from datetime import datetime
from typing import Dict, Optional, List, Callable, Any
from simple_salesforce import Salesforce
from requests.exceptions import Timeout, ConnectionError, RequestException

from config import get_settings
from core.exceptions import SalesforceError
from core.logging_config import get_logger

logger = get_logger(__name__)


def retry_on_timeout(max_retries: int = 3, base_delay: float = 2.0, max_delay: float = 30.0):
    """
    Decorator to retry function on timeout/connection errors with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts (default: 3).
        base_delay: Base delay in seconds between retries (default: 2.0).
        max_delay: Maximum delay in seconds between retries (default: 30.0).
    
    Returns:
        Decorated function with retry logic.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                    
                except (Timeout, ConnectionError) as e:
                    last_exception = e
                    
                    if attempt < max_retries:
                        # Calculate delay with exponential backoff
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        
                        logger.warning(
                            f"Timeout/Connection error on {func.__name__} "
                            f"(attempt {attempt + 1}/{max_retries + 1}). "
                            f"Retrying in {delay:.1f} seconds... Error: {e}"
                        )
                        
                        time.sleep(delay)
                    else:
                        logger.error(
                            f"Failed after {max_retries + 1} attempts on {func.__name__}. "
                            f"Last error: {e}"
                        )
                        
                except Exception as e:
                    # For other exceptions, don't retry
                    logger.error(f"Non-retryable error in {func.__name__}: {e}")
                    raise
            
            # If we exhausted all retries, raise the last exception
            raise last_exception
        
        return wrapper
    return decorator


class SalesforceService:
    """
    Service class for Salesforce operations.
    
    This class handles all interactions with Salesforce API including
    authentication, querying, and creating records.
    """
    
    def __init__(self):
        """Initialize the Salesforce service."""
        self.settings = get_settings()
        self._sf_client: Optional[Salesforce] = None
    
    @property
    def client(self) -> Salesforce:
        """
        Get Salesforce client instance.
        
        Returns:
            Authenticated Salesforce client.
            
        Raises:
            SalesforceError: If connection fails.
        """
        if self._sf_client is None:
            self._sf_client = self._connect()
        return self._sf_client
    
    def _connect(self) -> Salesforce:
        """
        Connect to Salesforce using credentials from settings.
        
        Returns:
            Authenticated Salesforce instance.
            
        Raises:
            SalesforceError: If connection fails.
        """
        try:
            logger.info("Connecting to Salesforce...")
            
            sf_config = self.settings.salesforce
            
            # Create session with timeout
            session = requests.Session()
            session.request = functools.partial(
                session.request,
                timeout=sf_config.timeout
            )
            
            # Connect to Salesforce
            sf = Salesforce(
                username=sf_config.username,
                password=sf_config.password,
                security_token=sf_config.security_token,
                consumer_key=sf_config.consumer_key,
                consumer_secret=sf_config.consumer_secret,
                session=session
            )
            
            # Get OAuth token for validation
            payload = {
                'grant_type': 'password',
                'client_id': sf_config.consumer_key,
                'client_secret': sf_config.consumer_secret,
                'username': sf_config.username,
                'password': sf_config.password + sf_config.security_token
            }
            
            response = requests.post(
                sf_config.token_url,
                data=payload,
                timeout=sf_config.timeout
            )
            
            if response.status_code != 200:
                raise SalesforceError(f"Token request failed: {response.text}")
            
            logger.info("Successfully connected to Salesforce")
            return sf
            
        except Exception as e:
            logger.error(f"Failed to connect to Salesforce: {e}")
            raise SalesforceError(f"Failed to connect to Salesforce: {e}")
    
    @retry_on_timeout(max_retries=3, base_delay=2.0, max_delay=30.0)
    def get_accounts(self) -> Dict[str, str]:
        """
        Get all Salesforce accounts.
        
        This method includes automatic retry logic for handling network issues.
        
        Returns:
            Dictionary mapping account IDs to account names.
            
        Raises:
            SalesforceError: If query fails after all retries.
        """
        try:
            logger.debug("Fetching Salesforce accounts...")
            
            query = "SELECT Id, Name FROM Account ORDER BY Name ASC"
            result = self.client.query(query)
            
            accounts_dict = {}
            seen_names = set()
            
            for record in result["records"]:
                name = record["Name"]
                
                # Only add unique names
                if name not in seen_names:
                    accounts_dict[record["Id"]] = name
                    seen_names.add(name)
            
            # Add "Other" option
            if "Other" not in seen_names:
                accounts_dict["other"] = "Other"
            
            logger.info(f"Retrieved {len(accounts_dict)} unique accounts")
            return accounts_dict
            
        except Exception as e:
            logger.error(f"Failed to fetch accounts: {e}")
            raise SalesforceError(f"Failed to fetch accounts: {e}")
    
    @retry_on_timeout(max_retries=3, base_delay=2.0, max_delay=30.0)
    def create_opportunity(
        self,
        name: str,
        stage_name: str,
        close_date: str,
        assessment_date: str,
        path: str,
        bu: str,
        account_id: Optional[str] = None
    ) -> Dict:
        """
        Create a new opportunity in Salesforce.
        
        This method includes automatic retry logic with exponential backoff
        for handling network timeouts and connection issues.
        
        Args:
            name: Opportunity name.
            stage_name: Stage of the opportunity.
            close_date: Expected close date (YYYY-MM-DD).
            assessment_date: Assessment date (YYYY-MM-DD).
            path: SharePoint path.
            bu: Business unit (ICT, FCT, IAT).
            account_id: Optional account ID to link the opportunity.
            
        Returns:
            Dictionary with creation result.
            
        Raises:
            SalesforceError: If creation fails after all retries.
        """
        try:
            logger.info(f"Creating opportunity: {name}")
            
            opportunity_data = {
                "Name": name,
                "StageName": stage_name,
                "CloseDate": close_date,
                "Assessment_Date__c": assessment_date,
                "Path__c": path,
                "BU__c": bu
            }
            
            # Add account ID if provided
            if account_id:
                opportunity_data["AccountId"] = account_id
            
            # Create opportunity (will retry on timeout)
            result = self.client.Opportunity.create(opportunity_data)
            
            if result.get('success'):
                logger.info(f"Successfully created opportunity: {result.get('id')}")
            else:
                logger.error(f"Failed to create opportunity: {result.get('errors')}")
            
            return result
            
        except (Timeout, ConnectionError) as e:
            # This will be caught by the retry decorator
            raise
        except Exception as e:
            logger.error(f"Failed to create opportunity: {e}")
            raise SalesforceError(f"Failed to create opportunity: {e}")


# Cached functions for Streamlit
@st.cache_resource
def get_salesforce_service() -> SalesforceService:
    """
    Get cached Salesforce service instance.
    
    Returns:
        SalesforceService instance.
    """
    return SalesforceService()


@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_unique_account_dict() -> Dict[str, str]:
    """
    Get cached dictionary of unique Salesforce accounts.
    
    Cached for 10 minutes to improve performance while allowing updates.
    Use st.cache_data instead of cache_resource because this is data, not a connection.
    
    Returns:
        Dictionary mapping account IDs to account names.
    """
    try:
        service = get_salesforce_service()
        return service.get_accounts()
    except SalesforceError as e:
        logger.error(f"Failed to get accounts: {e}")
        return {"other": "Other"}
