"""
SharePoint Storage Provider Module

This module implements the StorageProvider interface for Microsoft SharePoint
using Microsoft Graph API.

NOTE: This is a template/skeleton implementation. You'll need to:
1. Install required packages: pip install msal requests
2. Register an Azure AD application and get credentials
3. Configure appropriate permissions in Azure AD
4. Test with your SharePoint environment
"""

from pathlib import Path
from typing import List, BinaryIO, Optional
import requests
from .base import StorageProvider
from core.exceptions import StorageError
from core.logging_config import get_logger

logger = get_logger(__name__)


class SharePointStorageProvider(StorageProvider):
    """
    SharePoint storage provider using Microsoft Graph API.
    
    This provider implements file operations using Microsoft Graph API
    to interact with SharePoint Online.
    
    Prerequisites:
    - Azure AD app registration with appropriate permissions
    - Microsoft Graph API access
    - SharePoint site URL and configuration
    """
    
    def __init__(
        self,
        tenant_id: str,
        client_id: str,
        client_secret: str,
        site_id: str,
        drive_id: str,
        base_path: str = ""
    ):
        """
        Initialize the SharePoint storage provider.
        
        Args:
            tenant_id: Azure AD tenant ID
            client_id: Azure AD application client ID
            client_secret: Azure AD application client secret
            site_id: SharePoint site ID
            drive_id: SharePoint drive (document library) ID
            base_path: Base path within the drive for all operations
        """
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.site_id = site_id
        self.drive_id = drive_id
        self.base_path = base_path
        
        self.graph_url = "https://graph.microsoft.com/v1.0"
        self._access_token: Optional[str] = None
        
        logger.info(f"Initialized SharePointStorageProvider for site: {site_id}")
    
    def _get_access_token(self) -> str:
        """
        Get OAuth access token for Microsoft Graph API.
        
        Returns:
            Access token string.
            
        Raises:
            StorageError: If authentication fails.
        """
        if self._access_token:
            return self._access_token
        
        try:
            # Use MSAL to get token (requires: pip install msal)
            from msal import ConfidentialClientApplication
            
            authority = f"https://login.microsoftonline.com/{self.tenant_id}"
            scope = ["https://graph.microsoft.com/.default"]
            
            app = ConfidentialClientApplication(
                self.client_id,
                authority=authority,
                client_credential=self.client_secret
            )
            
            result = app.acquire_token_for_client(scopes=scope)
            
            if "access_token" in result:
                self._access_token = result["access_token"]
                logger.info("Successfully obtained access token")
                return self._access_token
            else:
                error = result.get("error_description", "Unknown error")
                raise StorageError(f"Failed to obtain access token: {error}")
                
        except ImportError:
            raise StorageError(
                "MSAL library not installed. "
                "Install it with: pip install msal"
            )
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise StorageError(f"Authentication failed: {e}")
    
    def _get_headers(self) -> dict:
        """Get headers for Graph API requests."""
        return {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json"
        }
    
    def _get_item_path(self, path: str) -> str:
        """Get full item path within the drive."""
        if self.base_path:
            return f"{self.base_path}/{path}".replace("//", "/")
        return path
    
    def _create_folder_raw(self, path: str) -> bool:
        """
        Create a folder in SharePoint using raw path (without adding base_path).
        Used internally by copy_template to avoid double base_path.
        
        Args:
            path: Full path where to create the folder (already includes base_path).
            
        Returns:
            True if folder was created successfully.
            
        Raises:
            StorageError: If folder creation fails.
        """
        try:
            # Use path directly without adding base_path
            parent_path = str(Path(path).parent)
            folder_name = Path(path).name
            
            # Create folder using Graph API
            url = f"{self.graph_url}/drives/{self.drive_id}/root:/{parent_path}:/children"
            
            payload = {
                "name": folder_name,
                "folder": {},
                "@microsoft.graph.conflictBehavior": "fail"  # Fail if exists instead of creating duplicate
            }
            
            response = requests.post(url, json=payload, headers=self._get_headers())
            
            if response.status_code in [200, 201]:
                logger.info(f"Created folder: {path}")
                return True
            else:
                error_msg = response.json().get("error", {}).get("message", "Unknown error")
                raise StorageError(f"Failed to create folder: {error_msg}")
                
        except Exception as e:
            logger.error(f"Failed to create folder {path}: {e}")
            raise StorageError(f"Failed to create folder: {e}")
    
    def create_folder(self, path: str) -> bool:
        """
        Create a folder in SharePoint.
        
        Args:
            path: Path where to create the folder.
            
        Returns:
            True if folder was created successfully.
            
        Raises:
            StorageError: If folder creation fails.
        """
        item_path = self._get_item_path(path)
        return self._create_folder_raw(item_path)
    
    def _folder_exists_raw(self, path: str) -> bool:
        """
        Check if a folder exists in SharePoint using raw path.
        
        Args:
            path: Full path to check (already includes base_path).
            
        Returns:
            True if folder exists, False otherwise.
        """
        try:
            url = f"{self.graph_url}/drives/{self.drive_id}/root:/{path}"
            
            response = requests.get(url, headers=self._get_headers())
            exists = response.status_code == 200
            
            logger.debug(f"Folder exists check for {path}: {exists}")
            return exists
            
        except Exception as e:
            logger.error(f"Error checking folder existence for {path}: {e}")
            return False
    
    def folder_exists(self, path: str) -> bool:
        """
        Check if a folder exists in SharePoint.
        
        Args:
            path: Path to check.
            
        Returns:
            True if folder exists, False otherwise.
        """
        item_path = self._get_item_path(path)
        return self._folder_exists_raw(item_path)
    
    def _upload_file_raw(self, file_content: BinaryIO, destination: str, filename: str) -> bool:
        """
        Upload a file to SharePoint using raw path (without adding base_path).
        Used internally by copy_template to avoid double base_path.
        
        Args:
            file_content: File content as binary stream.
            destination: Full destination folder path (already includes base_path).
            filename: Name of the file.
            
        Returns:
            True if upload was successful.
            
        Raises:
            StorageError: If upload fails.
        """
        try:
            # Use path directly without adding base_path
            item_path = f"{destination}/{filename}"
            
            # For files < 4MB, use simple upload
            # For larger files, use resumable upload session
            url = f"{self.graph_url}/drives/{self.drive_id}/root:/{item_path}:/content"
            
            headers = self._get_headers()
            headers["Content-Type"] = "application/octet-stream"
            
            response = requests.put(url, data=file_content.getvalue(), headers=headers)
            
            if response.status_code in [200, 201]:
                logger.info(f"Uploaded file: {item_path}")
                return True
            else:
                error_msg = response.json().get("error", {}).get("message", "Unknown error")
                raise StorageError(f"Failed to upload file: {error_msg}")
                
        except Exception as e:
            logger.error(f"Failed to upload file {filename} to {destination}: {e}")
            raise StorageError(f"Failed to upload file: {e}")
    
    def upload_file(self, file_content: BinaryIO, destination: str, filename: str) -> bool:
        """
        Upload a file to SharePoint.
        
        Args:
            file_content: File content as binary stream.
            destination: Destination folder path.
            filename: Name of the file.
            
        Returns:
            True if upload was successful.
            
        Raises:
            StorageError: If upload fails.
        """
        item_path = self._get_item_path(destination)
        return self._upload_file_raw(file_content, item_path, filename)
    
    def upload_files(self, files: List[tuple], destination: str) -> List[str]:
        """
        Upload multiple files to SharePoint.
        
        Args:
            files: List of tuples (filename, file_content).
            destination: Destination folder path (already includes base_path).
            
        Returns:
            List of uploaded file paths.
            
        Raises:
            StorageError: If upload fails.
        """
        uploaded_paths = []
        
        for filename, file_content in files:
            try:
                # Use _raw method to avoid double base_path
                # destination already includes base_path from StorageService
                self._upload_file_raw(file_content, destination, filename)
                uploaded_paths.append(f"{destination}/{filename}")
            except StorageError as e:
                logger.error(f"Failed to upload {filename}: {e}")
                raise
        
        logger.info(f"Uploaded {len(uploaded_paths)} files to {destination}")
        return uploaded_paths
    
    def copy_template(self, template_path: str, destination: str) -> bool:
        """
        Copy a local template folder to a destination in SharePoint.
        
        This method uploads a local template folder recursively to SharePoint.
        All files and subfolders are copied maintaining the directory structure.
        
        Args:
            template_path: Path to the LOCAL template folder.
            destination: Destination path in SharePoint.
            
        Returns:
            True if copy was successful.
            
        Raises:
            StorageError: If copy fails or template doesn't exist.
        """
        from pathlib import Path
        from io import BytesIO
        
        template_path_obj = Path(template_path)
        
        # Validate template exists locally
        if not template_path_obj.exists():
            raise StorageError(f"Template not found locally: {template_path}")
        
        if not template_path_obj.is_dir():
            raise StorageError(f"Template path is not a directory: {template_path}")
        
        logger.info(f"Copying template from {template_path} to SharePoint: {destination}")
        
        try:
            # NOTE: destination already includes base_path (e.g., "01_2025/1_ICT/...")
            # We need to use the raw path without adding base_path again
            
            # DO NOT create destination folder here - it was already created by create_project_folder()
            # Creating it here causes SharePoint to create a duplicate with suffix (e.g., "Project1")
            # self._create_folder_raw(destination)  # ❌ Commented out - causes duplicate
            
            # Counter for progress
            files_copied = 0
            folders_created = 0
            
            # Recursively walk through template directory
            for item in template_path_obj.rglob("*"):
                # Calculate relative path from template root
                relative_path = item.relative_to(template_path_obj)
                # destination already includes base_path, so we use it directly
                sharepoint_path = f"{destination}/{relative_path}".replace("\\", "/")
                
                if item.is_dir():
                    # Create folder in SharePoint (use raw path)
                    try:
                        self._create_folder_raw(sharepoint_path)
                        folders_created += 1
                        logger.debug(f"Created folder: {sharepoint_path}")
                    except StorageError as e:
                        # Folder might already exist, continue
                        logger.debug(f"Folder creation skipped (might exist): {sharepoint_path}")
                
                elif item.is_file():
                    # Upload file to SharePoint (use raw path)
                    try:
                        with open(item, 'rb') as f:
                            file_content = BytesIO(f.read())
                            parent_folder = str(Path(sharepoint_path).parent)
                            filename = item.name
                            
                            self._upload_file_raw(file_content, parent_folder, filename)
                            files_copied += 1
                            
                            if files_copied % 10 == 0:  # Progress log every 10 files
                                logger.info(f"Progress: {files_copied} files copied...")
                                
                    except Exception as e:
                        logger.error(f"Failed to upload file {item.name}: {e}")
                        raise StorageError(f"Failed to upload {item.name}: {e}")
            
            logger.info(
                f"✅ Template copied successfully: "
                f"{folders_created} folders created, {files_copied} files uploaded"
            )
            return True
            
        except StorageError:
            raise
        except Exception as e:
            logger.error(f"Failed to copy template: {e}", exc_info=True)
            raise StorageError(f"Failed to copy template from {template_path}: {e}")
    
    def write_file(self, content: str, destination: str, filename: str) -> bool:
        """
        Write text content to a file in SharePoint.
        
        Args:
            content: Text content to write.
            destination: Destination folder path (already includes base_path from get_full_path).
            filename: Name of the file.
            
        Returns:
            True if write was successful.
            
        Raises:
            StorageError: If write fails.
        """
        try:
            from io import BytesIO
            
            # Convert string content to binary
            file_content = BytesIO(content.encode('utf-8'))
            
            # Use _raw method to avoid double base_path
            # destination already includes base_path from StorageService.get_full_path()
            return self._upload_file_raw(file_content, destination, filename)
            
        except Exception as e:
            logger.error(f"Failed to write file {filename} to {destination}: {e}")
            raise StorageError(f"Failed to write file: {e}")
    
    def get_full_path(self, *path_parts: str) -> str:
        """
        Get full path by joining path parts.
        
        Args:
            path_parts: Path components to join.
            
        Returns:
            Full path as string.
        """
        base = self.base_path if self.base_path else ""
        full_path = "/".join([base] + list(path_parts)).replace("//", "/")
        return full_path


# Factory function to create storage provider based on configuration
def create_storage_provider(provider_type: str, **kwargs) -> StorageProvider:
    """
    Factory function to create a storage provider.
    
    Args:
        provider_type: Type of provider ('local' or 'sharepoint')
        **kwargs: Configuration parameters for the provider
        
    Returns:
        StorageProvider instance
        
    Raises:
        ValueError: If provider_type is unknown
    """
    if provider_type == "local":
        from .local_storage import LocalStorageProvider
        return LocalStorageProvider(**kwargs)
    elif provider_type == "sharepoint":
        return SharePointStorageProvider(**kwargs)
    else:
        raise ValueError(f"Unknown storage provider type: {provider_type}")
