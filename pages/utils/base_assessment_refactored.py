"""
Base Assessment Module (Refactored)

This module provides common functionality for all assessment types (ICT, IAT, FCT).
Refactored to use the new service layer architecture with proper separation of concerns.

Key improvements:
- Uses StorageService for file operations
- Uses SalesforceService for Salesforce operations
- Better error handling with custom exceptions
- Improved logging
- Cleaner separation of concerns
"""

from datetime import datetime
from typing import Callable, Dict, List, Optional
import streamlit as st

from services.salesforce_service import get_salesforce_service, get_unique_account_dict
from services.storage_service import get_storage_service
from pages.utils.dates_info import get_last_weekday_of_next_month, get_date_after_next_working_days
from pages.utils.global_styles import set_global_styles, load_ibtest_logo, subtitle_h3
from pages.utils.validations import validate_email, validate_fields
from pages.utils.constants import COUNTRIES_DICT, YES_NO
from core.exceptions import ValidationError, SalesforceError, StorageError
from core.logging_config import get_logger
from config import get_settings

logger = get_logger(__name__)


class BaseAssessment:
    """
    Base class for all assessment types.
    
    This class provides common functionality for ICT, IAT, and FCT assessments.
    Refactored to use service layer architecture.
    """
    
    def __init__(self, assessment_type: str, title: str, projects_folder: str):
        """
        Initialize the base assessment.
        
        Args:
            assessment_type: The type of assessment (ICT, IAT, FCT)
            title: The title of the assessment
            projects_folder: The folder name for projects
        """
        self.assessment_type = assessment_type
        self.title = title
        self.projects_folder = projects_folder
        self.info: Dict = {}
        self.year = str(datetime.today().year)
        
        # Initialize services (cached for performance)
        self.settings = get_settings()
        self.salesforce_service = get_salesforce_service()  # Cached connection
        self.storage_service = get_storage_service()  # Cached connection
        
        logger.info(f"Initialized {assessment_type} assessment")
    
    def setup_page(self) -> None:
        """Set up the page configuration and styles."""
        set_global_styles()
        
        col1, col2 = st.columns([8, 1.5])
        with col1:
            st.title(self.title)
        with col2:
            load_ibtest_logo()
    
    def upload_files(self, file_types: Dict[str, bool]) -> tuple:
        """
        Create a file upload section.
        
        Args:
            file_types: Dictionary of file types with required status
            
        Returns:
            Tuple of (uploaded_files, checked_items)
        """
        checked_items = {}
        
        with st.container(border=True):
            subtitle_h3("Are you sharing files?")
            uploaded_files = st.file_uploader(
                ".",
                label_visibility="hidden",
                accept_multiple_files=True
            )
        
            for file_type in file_types:
                checked = file_type.strip().startswith("*")
                checked_items[file_type] = st.checkbox(f"{file_type}", value=checked)
        
        return uploaded_files, checked_items
    
    def create_customer_info_section(self) -> None:
        """Create the customer information section of the form."""
        st.write("(*) Mandatory Fields")
        
        with st.container(border=True):
            col1, col2 = st.columns(2)
            
            with col1:
                self.info["project_name"] = st.text_input(
                    r"*Name or Project Reference",
                    placeholder="Enter the name of the project"
                )
                self.info["contact_name"] = st.text_input(
                    r"*Contact Name",
                    placeholder="Enter your name"
                )
                
                # Get accounts from Salesforce
                all_accounts = get_unique_account_dict()
                accounts_by_name = {name: id for id, name in all_accounts.items()}
                
                self.info["customer_name"] = st.selectbox(
                    r"*Company name",
                    options=list(accounts_by_name.keys()),
                    index=None,
                    placeholder="Select from list"
                )
                self.info['country'] = st.selectbox(
                    r"*Country",
                    options=COUNTRIES_DICT.keys()
                )
            
            with col2:
                self.info["date"] = datetime.today().strftime("%Y-%m-%d")
                self.info["quotation_required_date"] = st.date_input(
                    'When do you need the quote? Select an ideal date',
                    get_date_after_next_working_days(5)
                ).strftime("%Y-%m-%d")
                self.info["contact_email"] = st.text_input(
                    r'*Email',
                    placeholder="Enter your email"
                )
                self.info["customer_name2"] = st.text_input(
                    "Company not listed? Write it here.",
                    placeholder="Enter the customer name"
                )
                self.info["contact_phone"] = st.text_input(
                    'Phone Number',
                    placeholder="Enter your phone number"
                )
            
            self.info["is_duplicated"] = st.radio(
                r'*Duplicated Project?',
                YES_NO,
                index=1,
                horizontal=True
            )
    
    def _validate_form_data(self) -> None:
        """
        Validate form data.
        
        Raises:
            ValidationError: If validation fails.
        """
        # Validate email
        if not validate_email(self.info['contact_email']):
            raise ValidationError(
                "Only corporate emails are valid",
                field="contact_email"
            )
        
        # Validate required fields
        errors = validate_fields(self.info)
        if errors:
            raise ValidationError("\n".join(errors))
    
    def _prepare_customer_data(self) -> Dict:
        """
        Prepare customer data for processing.
        
        Returns:
            Dictionary with prepared customer data.
        """
        customer_data = {
            "country": self.info.get("country", "Mexico"),
            "customer_in_list": True
        }
        
        # Handle customer name
        if self.info["customer_name"] is None or self.info["customer_name"] == "Other":
            customer_data["customer_name"] = self.info["customer_name2"]
            customer_data["customer_in_list"] = False
        else:
            customer_data["customer_name"] = self.info["customer_name"]
        
        return customer_data
    
    def _create_project_structure(
        self,
        customer_data: Dict,
        uploaded_files: List
    ) -> str:
        """
        Create project folder structure and upload files.
        
        Args:
            customer_data: Prepared customer data.
            uploaded_files: List of uploaded files.
            
        Returns:
            Path to the created project folder.
            
        Raises:
            StorageError: If folder creation or file upload fails.
        """
        # Create project folder
        project_path = self.storage_service.create_project_folder(
            assessment_type=self.assessment_type,
            projects_folder=self.projects_folder,
            customer_name=customer_data["customer_name"],
            project_name=self.info["project_name"],
            country=customer_data["country"]
        )
        
        logger.info(f"Created project structure at: {project_path}")
        
        # Upload files if any
        if uploaded_files:
            self.storage_service.upload_assessment_files(
                project_path=project_path,
                assessment_type=self.assessment_type,
                files=uploaded_files
            )
            logger.info(f"Uploaded {len(uploaded_files)} files")
        
        return project_path
    
    def _save_html_report(
        self,
        project_path: str,
        html_converter: Callable
    ) -> None:
        """
        Generate and save HTML report.
        
        Args:
            project_path: Path to the project folder.
            html_converter: Function to convert info to HTML.
            
        Raises:
            StorageError: If save fails.
        """
        html_data = html_converter(self.info)
        
        if html_data:
            self.storage_service.save_assessment_html(
                project_path=project_path,
                assessment_type=self.assessment_type,
                html_content=html_data
            )
            logger.info("Saved HTML report")
    
    def _get_sharepoint_url(self, project_path: str) -> str:
        """
        Generate SharePoint URL for the project folder.
        
        Args:
            project_path: Relative path to the project folder (from StorageService).
                         This path already includes SHAREPOINT_BASE_PATH if configured.
            
        Returns:
            Full SharePoint URL to the project folder.
        """
        # Get base SharePoint URL from settings
        base_url = self.settings.storage.sharepoint_path
        
        # Clean the project path (it already includes base_path from StorageService)
        from pathlib import Path
        project_relative = str(Path(project_path)).replace("\\", "/").lstrip("/")
        
        # Construct full SharePoint URL
        # Note: project_relative already includes SHAREPOINT_BASE_PATH (e.g., "01_2025/1_ICT/...")
        # because SharePointStorageProvider.get_full_path() adds it
        if base_url.endswith("/"):
            sharepoint_url = f"{base_url}{project_relative}"
        else:
            sharepoint_url = f"{base_url}/{project_relative}"
        
        logger.info(f"Generated SharePoint URL: {sharepoint_url}")
        return sharepoint_url
    
    def _create_salesforce_opportunity(
        self,
        customer_data: Dict,
        project_path: str
    ) -> Dict:
        """
        Create Salesforce opportunity.
        
        Args:
            customer_data: Prepared customer data.
            project_path: Path to the created project folder.
            
        Returns:
            Result dictionary from Salesforce.
            
        Raises:
            SalesforceError: If creation fails.
        """
        # Prepare opportunity data
        opportunity_name = self.info["project_name"]
        stage_name = "New Request"
        
        # Get account ID if customer is in list
        account_id = None
        if customer_data["customer_in_list"]:
            all_accounts = get_unique_account_dict()
            accounts_by_name = {name: id for id, name in all_accounts.items()}
            account_id = accounts_by_name.get(customer_data["customer_name"])
        
        # Generate SharePoint URL for this specific project
        sharepoint_url = self._get_sharepoint_url(project_path)
        
        # Create opportunity
        result = self.salesforce_service.create_opportunity(
            name=opportunity_name,
            stage_name=stage_name,
            close_date=get_last_weekday_of_next_month().strftime("%Y-%m-%d"),
            assessment_date=datetime.now().strftime("%Y-%m-%d"),
            path=sharepoint_url,
            bu=self.assessment_type,
            account_id=account_id
        )
        
        return result
    
    def process_form_submission(
        self,
        uploaded_files: List,
        html_converter: Callable
    ) -> bool:
        """
        Process the form submission.
        
        Args:
            uploaded_files: List of uploaded files
            html_converter: Function to convert info to HTML
            
        Returns:
            True if submission was successful, False otherwise.
        """
        try:
            logger.info(f"Processing {self.assessment_type} assessment submission")
            
            # Validate form data
            self._validate_form_data()
            
            # Prepare customer data
            customer_data = self._prepare_customer_data()
            
            # Create project structure and upload files
            project_path = self._create_project_structure(
                customer_data,
                uploaded_files
            )
            
            # Save HTML report
            self._save_html_report(project_path, html_converter)
            
            # Create Salesforce opportunity with project-specific path
            result = self._create_salesforce_opportunity(customer_data, project_path)
            if result.get('success'):
                st.success("✅ Opportunity created successfully!")
                logger.info(f"Successfully created opportunity: {result.get('id')}")
                return True
            else:
                error_messages = result.get('errors', ['Unknown error'])
                st.error("❌ Error creating Opportunity")
                for error in error_messages:
                    st.error(str(error))
                logger.error(f"Failed to create opportunity: {error_messages}")
                return False
        
        except ValidationError as e:
            st.error(f"❌ Validation Error: {e.message}")
            logger.warning(f"Validation error: {e.message}")
            return False
        
        except StorageError as e:
            st.error(f"❌ Storage Error: {e.message}")
            st.error("Please try again or contact the administrator.")
            logger.error(f"Storage error: {e.message}", exc_info=True)
            return False
        
        except SalesforceError as e:
            st.error(f"❌ Salesforce Error: {e.message}")
            st.error("Please try again or contact the administrator.")
            logger.error(f"Salesforce error: {e.message}", exc_info=True)
            return False
        
        except Exception as e:
            st.error(f"❌ Unexpected Error: {str(e)}")
            st.error("Please try again or contact the administrator.")
            logger.error(f"Unexpected error during submission: {e}", exc_info=True)
            return False
    
    def render_form(
        self,
        file_types: Dict[str, bool],
        html_converter: Callable,
        additional_sections: Optional[Callable] = None
    ) -> None:
        """
        Render the complete assessment form.
        
        Args:
            file_types: Dictionary of file types to display
            html_converter: Function to convert info to HTML
            additional_sections: Optional function to render additional form sections
        """
        self.setup_page()
        
        with st.form(key=f'{self.assessment_type.lower()}_assessment'):
            # Create customer info section
            self.create_customer_info_section()
            
            # Upload files
            uploaded_files, checked_items = self.upload_files(file_types)
            self.info["file_types"] = checked_items
            
            # Add additional sections if provided
            if additional_sections:
                additional_sections(self.info)
            
            # Form buttons
            cols = st.columns(6)
            with cols[0]:
                submit = st.form_submit_button('Submit', help='Submit form', type='primary')
            with cols[5]:
                logout = st.form_submit_button("Logout")
            
            # Process form submission
            if submit:
                self.process_form_submission(uploaded_files, html_converter)
            
            if logout:
                from core.auth import AuthService
                AuthService.logout()
                st.switch_page("main.py")
