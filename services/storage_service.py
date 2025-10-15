"""
Storage Service Module

This module provides a service layer for storage operations.
It abstracts the storage provider and provides high-level operations.
"""

import os
import streamlit as st
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

from config import get_settings
from storage import StorageProvider, LocalStorageProvider, SharePointStorageProvider
from core.exceptions import StorageError
from core.logging_config import get_logger
from pages.utils.constants import COUNTRIES_DICT

logger = get_logger(__name__)


class StorageService:
    """
    Service class for storage operations.
    
    This class provides high-level storage operations for assessments,
    abstracting the underlying storage provider.
    """
    
    def __init__(self, storage_provider: Optional[StorageProvider] = None):
        """
        Initialize the storage service.
        
        Args:
            storage_provider: Optional storage provider. If None, auto-detects from config.
        """
        self.settings = get_settings()
        
        if storage_provider is None:
            # Auto-detect provider based on configuration
            storage_provider = self._create_provider_from_config()
        
        self.provider = storage_provider
        logger.info(f"Initialized StorageService with {type(storage_provider).__name__}")
    
    def _create_provider_from_config(self) -> StorageProvider:
        """
        Create storage provider based on configuration.
        
        Returns:
            StorageProvider instance (LocalStorageProvider or SharePointStorageProvider)
        """
        provider_type = getattr(self.settings.storage, 'provider', 'local').lower()
        
        if provider_type == 'sharepoint':
            # Create SharePoint provider
            logger.info("Creating SharePoint storage provider")
            
            # For SharePoint, base_path should be a folder prefix within SharePoint
            # (e.g., "01_2025"), not a local filesystem path
            sharepoint_base_path = os.getenv('SHAREPOINT_BASE_PATH', '')
            
            return SharePointStorageProvider(
                tenant_id=self.settings.azure.tenant_id,
                client_id=self.settings.azure.client_id,
                client_secret=self.settings.azure.client_secret,
                site_id=self.settings.sharepoint.site_id,
                drive_id=self.settings.sharepoint.drive_id,
                base_path=sharepoint_base_path
            )
        else:
            # Default to local storage
            logger.info("Creating Local storage provider")
            return LocalStorageProvider(self.settings.storage.base_path)
    
    def get_template_path(self, assessment_type: str) -> Path:
        """
        Get the template path for an assessment type.
        
        Args:
            assessment_type: Type of assessment (ICT, FCT, IAT).
            
        Returns:
            Path to the template folder.
            
        Raises:
            ValueError: If assessment type is invalid.
        """
        template_map = {
            "ICT": self.settings.storage.template_ict,
            "FCT": self.settings.storage.template_fct,
            "IAT": self.settings.storage.template_iat
        }
        
        if assessment_type not in template_map:
            raise ValueError(f"Invalid assessment type: {assessment_type}")
        
        return template_map[assessment_type]
    
    def create_project_folder(
        self,
        assessment_type: str,
        projects_folder: str,
        customer_name: str,
        project_name: str,
        country: str
    ) -> str:
        """
        Create a project folder structure for an assessment.
        
        Args:
            assessment_type: Type of assessment (ICT, FCT, IAT).
            projects_folder: Base projects folder name.
            customer_name: Customer name.
            project_name: Project name.
            country: Country name.
            
        Returns:
            Full path to the created project folder.
            
        Raises:
            StorageError: If folder creation fails or project already exists.
        """
        try:
            # Build project folder path
            country_code = COUNTRIES_DICT.get(country, "OTHER")
            project_path = self.provider.get_full_path(
                projects_folder,
                country_code,
                customer_name,
                project_name
            )
            
            logger.info(f"Creating project folder: {project_path}")
            
            # Check if project already exists
            # Use _folder_exists_raw for SharePoint to avoid double base_path
            if hasattr(self.provider, '_folder_exists_raw'):
                # SharePoint provider - use raw method
                exists = self.provider._folder_exists_raw(project_path)
            else:
                # Local provider - use normal method
                exists = self.provider.folder_exists(project_path)
            
            if exists:
                raise StorageError(
                    f"Project '{project_name}' already exists. "
                    "Please contact Sales Manager to update your requirement."
                )
            
            # Create project folder
            # Use _create_folder_raw for SharePoint to avoid double base_path
            # project_path already includes base_path from get_full_path()
            if hasattr(self.provider, '_create_folder_raw'):
                # SharePoint provider - use raw method
                self.provider._create_folder_raw(project_path)
            else:
                # Local provider - use normal method
                self.provider.create_folder(project_path)
            
            # Copy template
            template_path = str(self.get_template_path(assessment_type))
            self.provider.copy_template(template_path, project_path)
            
            logger.info(f"Successfully created project folder: {project_path}")
            return project_path
            
        except StorageError:
            raise
        except Exception as e:
            logger.error(f"Failed to create project folder: {e}")
            raise StorageError(f"Failed to create project folder: {e}")
    
    def upload_assessment_files(
        self,
        project_path: str,
        assessment_type: str,
        files: List
    ) -> List[str]:
        """
        Upload assessment files to the project folder.
        
        Args:
            project_path: Path to the project folder.
            assessment_type: Type of assessment (ICT, FCT, IAT).
            files: List of uploaded files from Streamlit.
            
        Returns:
            List of uploaded file paths.
            
        Raises:
            StorageError: If upload fails.
        """
        try:
            # Determine destination folder based on assessment type
            if assessment_type == "ICT":
                destination = str(Path(project_path) / "1_Customer_Info" / "7_ALL_Info_Shared")
            else:
                destination = str(Path(project_path) / "1_Customer_Info" / "3_ALL_Info_Shared")
            
            logger.info(f"Uploading {len(files)} files to {destination}")
            
            # Prepare files for upload
            files_to_upload = [(file.name, file) for file in files]
            
            # Upload files
            uploaded_paths = self.provider.upload_files(files_to_upload, destination)
            
            logger.info(f"Successfully uploaded {len(uploaded_paths)} files")
            return uploaded_paths
            
        except Exception as e:
            logger.error(f"Failed to upload files: {e}")
            raise StorageError(f"Failed to upload files: {e}")
    
    def save_assessment_html(
        self,
        project_path: str,
        assessment_type: str,
        html_content: str
    ) -> str:
        """
        Save the assessment HTML report.
        
        Args:
            project_path: Path to the project folder.
            assessment_type: Type of assessment (ICT, FCT, IAT).
            html_content: HTML content to save.
            
        Returns:
            Path to the saved HTML file.
            
        Raises:
            StorageError: If save fails.
        """
        try:
            filename = f"{assessment_type}_Assessment.html"
            
            logger.info(f"Saving assessment HTML: {filename}")
            
            self.provider.write_file(html_content, project_path, filename)
            
            file_path = str(Path(project_path) / filename)
            logger.info(f"Successfully saved HTML file: {file_path}")
            
            return file_path
            
        except Exception as e:
            logger.error(f"Failed to save HTML file: {e}")
            raise StorageError(f"Failed to save HTML file: {e}")


# Cached function for Streamlit
@st.cache_resource
def get_storage_service() -> StorageService:
    """
    Get cached StorageService instance with persistent connection.
    
    This improves performance by reusing the storage provider connection,
    especially important for SharePoint which has connection overhead.
    
    Returns:
        StorageService instance with initialized provider.
    """
    return StorageService()
