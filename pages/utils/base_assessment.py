"""
Base Assessment Module

This module provides common functionality for all assessment types (ICT, IAT, FCT).
It contains shared utilities, form handling, and file upload functionality.
"""

import json
import os
import shutil
from datetime import datetime
import streamlit as st
from decouple import config

from pages.utils.salesforce_access import connect_to_salesforce, get_unique_account_dict
from pages.utils.dates_info import get_last_weekday_of_next_month, get_date_after_next_working_days
from pages.utils.global_styles import set_global_styles, load_ibtest_logo, subtitle_h3
from pages.utils.validations import validate_email, validate_fields
from pages.utils.constants import COUNTRIES_DICT, YES_NO


class BaseAssessment:
    """
    Base class for all assessment types.
    
    This class provides common functionality for ICT, IAT, and FCT assessments.
    """
    
    def __init__(self, assessment_type, title, projects_folder):
        """
        Initialize the base assessment.
        
        Args:
            assessment_type (str): The type of assessment (ICT, IAT, FCT)
            title (str): The title of the assessment
            projects_folder (str): The folder name for projects
        """
        self.assessment_type = assessment_type
        self.title = title
        self.projects_folder = projects_folder
        self.info = {}
        self.year = str(datetime.today().year)
        
        # Initialize session state for Salesforce connection
        if "salesforce" not in st.session_state:
            st.session_state.salesforce = connect_to_salesforce()
    
    def setup_page(self):
        """Set up the page configuration and styles."""
        # Note: set_page_config() is now called in each assessment page
        set_global_styles()
        
        col1, col2 = st.columns([8, 1.5])
        with col1:
            st.title(self.title)
        with col2:
            load_ibtest_logo()
        
    def upload_files(self, file_types):
        """
        Create a file upload section.
        
        Args:
            file_types (list): List of file types to display
            
        Returns:
            list: List of uploaded files
        """
        checked_items = {}
        with st.container(border=True):
            subtitle_h3("Are you sharing files?")
            uploaded_files = st.file_uploader(".", label_visibility="hidden", accept_multiple_files=True)
        
            for file_type in file_types:
                #st.markdown(f'<p style="margin-bottom: 1px;">{file_type}</p>', unsafe_allow_html=True)
                checked = True if file_type.strip().startswith("*") else False
                checked_items[file_type] = st.checkbox(f"{file_type}", value=checked)
                
        return uploaded_files, checked_items
    
    def create_customer_info_section(self):
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
                    'When do you need the quote? Select an ideal date', get_date_after_next_working_days(5)
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
    
    def process_form_submission(self, uploaded_files, html_converter):
        """
        Process the form submission.
        
        Args:
            uploaded_files (list): List of uploaded files
            html_converter (function): Function to convert info to HTML
            
        Returns:
            bool: True if submission was successful, False otherwise
        """
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        #st.write(self.info)
        
        # Validate email
        valid_email = validate_email(self.info['contact_email'])
        if not valid_email:
            st.error("Error!! Only Corporate emails are valid")
            return False
        
        # Validate required fields
        errors_validation = validate_fields(self.info)
        if errors_validation:
            for error in errors_validation:
                st.error(error)
            return False
        
        try:
            
            # Process customer information
            country = self.info.get("country", "Mexico")
            customer_in_list = True
            if self.info["customer_name"] is None or self.info["customer_name"] == "Other":
                self.info["customer_name"] = self.info["customer_name2"]
                customer_in_list = False
            
            # Create project folder
            upload_files_folder = os.path.join(
                config("PATH_FILE"),
                self.projects_folder, 
                COUNTRIES_DICT[country], 
                f"{self.info['customer_name']}",
                f"{self.info['project_name']}"
            )
            
            # Check if project already exists
            if os.path.exists(upload_files_folder):
                st.error(f"Opportunity with name {self.info['project_name']} already created, please contact Sales Manager to update your requirement.")
                return False
            
            # Create project folder and copy template
            os.makedirs(upload_files_folder, exist_ok=True)
            template_folder = config(f"TEMPLATE_{self.assessment_type}")
            shutil.copytree(template_folder, upload_files_folder, dirs_exist_ok=True)
            
            # Save uploaded files
            all_info_shared_path = os.path.join(upload_files_folder, "1_Customer_Info", "3_ALL_Info_Shared")
            
            #For ICT, the folder is different
            if self.assessment_type == "ICT":
                all_info_shared_path = os.path.join(upload_files_folder, "1_Customer_Info", "7_ALL_Info_Shared")
            
            if uploaded_files:
                for file in uploaded_files:
                    save_path = os.path.join(all_info_shared_path, file.name)
                    with open(save_path, "wb") as f:
                        f.write(file.getbuffer())
            
            # Generate HTML report
            html_data = html_converter(self.info)
            
            if html_data:
                path_html = os.path.join(upload_files_folder, f"{self.assessment_type}_Assessment.html")
                with open(path_html, 'w') as file:
                    file.write(html_data)
            
            # Create Salesforce opportunity
            opportunity_name = self.info["project_name"]
            stage_name = "New Request"
            
            new_opp = {
                "Name": opportunity_name,
                "StageName": stage_name,
                "CloseDate": get_last_weekday_of_next_month().strftime("%Y-%m-%d"),
                "Assessment_Date__c": datetime.now().strftime("%Y-%m-%d"),
                "Path__c": config("PATH_TO_SHAREPOINT"),                        
                "BU__c": self.assessment_type
            }
            
            # Add account ID if customer is in the list
            if customer_in_list:
                all_accounts = get_unique_account_dict()
                accounts_by_name = {name: id for id, name in all_accounts.items()}
                new_opp["AccountId"] = accounts_by_name.get(self.info["customer_name"], "")
            
            #st.write(new_opp)
            #raise ValueError("Not sending to Salesforce yet!")
        
            # Create opportunity in Salesforce
            result = st.session_state.salesforce.__getattr__('Opportunity').create(new_opp)
            
            if result['success']:
                st.success("Opportunity created successfully!")
                return True
            else:
                st.error("Error creating Opportunity")
                st.error("\n".join(result['errors']))
                return False
                
        except Exception as e:
            st.error(f'Error submitting the form! {e}')
            st.error('Please try again.')
            st.error('If the problem persists, contact the administrator.')
            return False
    
    def render_form(self, file_types, html_converter, additional_sections=None):
        """
        Render the complete assessment form.
        
        Args:
            file_types (list): List of file types to display
            html_converter (function): Function to convert info to HTML
            additional_sections (function, optional): Function to render additional form sections
        """
        self.setup_page()
        
        with st.form(key=f'{self.assessment_type.lower()}_assessment'):
            
            # Create customer info section
            self.create_customer_info_section()
            
            # Upload files
            uploaded_files, checked_items = self.upload_files(file_types)
            self.info["file_types"] = checked_items
            #for (item, value) in checked_items.items():
            #    st.info[item] = value
            
            # Add additional sections if provided
            if additional_sections:
                additional_sections(self.info)
            
            cols = st.columns(6)
            with cols[0]:
                # Submit button
                submit = st.form_submit_button('Submit', help='Submit form', type='primary')
            with cols[5]:
                logout = st.form_submit_button("Logout")
                                
            # Process form submission
            if submit:
                self.process_form_submission(uploaded_files, html_converter) 
            
            if logout:
                st.session_state['authenticated'] = False
                st.switch_page("main.py")

