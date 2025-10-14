"""
Local Storage Provider Module

This module implements the StorageProvider interface for local filesystem storage.
This is the current implementation that the application uses.
"""

import os
import shutil
from pathlib import Path
from typing import List, BinaryIO
from .base import StorageProvider
from core.exceptions import StorageError
from core.logging_config import get_logger

logger = get_logger(__name__)


class LocalStorageProvider(StorageProvider):
    """
    Local filesystem storage provider.
    
    This provider implements file operations using the local filesystem.
    It's the default provider and maintains compatibility with the current
    implementation.
    """
    
    def __init__(self, base_path: Path):
        """
        Initialize the local storage provider.
        
        Args:
            base_path: Base path for all storage operations.
        """
        self.base_path = Path(base_path)
        logger.info(f"Initialized LocalStorageProvider with base_path: {self.base_path}")
    
    def create_folder(self, path: str) -> bool:
        """
        Create a folder at the specified path.
        
        Args:
            path: Path where to create the folder.
            
        Returns:
            True if folder was created successfully.
            
        Raises:
            StorageError: If folder creation fails.
        """
        try:
            full_path = Path(path)
            full_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created folder: {full_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to create folder {path}: {e}")
            raise StorageError(f"Failed to create folder: {e}")
    
    def folder_exists(self, path: str) -> bool:
        """
        Check if a folder exists.
        
        Args:
            path: Path to check.
            
        Returns:
            True if folder exists, False otherwise.
        """
        exists = Path(path).exists()
        logger.debug(f"Folder exists check for {path}: {exists}")
        return exists
    
    def upload_file(self, file_content: BinaryIO, destination: str, filename: str) -> bool:
        """
        Upload a file to the specified destination.
        
        Args:
            file_content: File content as binary stream.
            destination: Destination folder path.
            filename: Name of the file.
            
        Returns:
            True if upload was successful.
            
        Raises:
            StorageError: If upload fails.
        """
        try:
            dest_path = Path(destination)
            dest_path.mkdir(parents=True, exist_ok=True)
            
            file_path = dest_path / filename
            with open(file_path, 'wb') as f:
                f.write(file_content.getvalue())
            
            logger.info(f"Uploaded file: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to upload file {filename} to {destination}: {e}")
            raise StorageError(f"Failed to upload file: {e}")
    
    def upload_files(self, files: List[tuple], destination: str) -> List[str]:
        """
        Upload multiple files to the specified destination.
        
        Args:
            files: List of tuples (filename, file_content).
            destination: Destination folder path.
            
        Returns:
            List of uploaded file paths.
            
        Raises:
            StorageError: If upload fails.
        """
        uploaded_paths = []
        
        for filename, file_content in files:
            try:
                self.upload_file(file_content, destination, filename)
                uploaded_paths.append(str(Path(destination) / filename))
            except StorageError as e:
                logger.error(f"Failed to upload {filename}: {e}")
                raise
        
        logger.info(f"Uploaded {len(uploaded_paths)} files to {destination}")
        return uploaded_paths
    
    def copy_template(self, template_path: str, destination: str) -> bool:
        """
        Copy a template folder to a destination.
        
        Args:
            template_path: Path to the template folder.
            destination: Destination path.
            
        Returns:
            True if copy was successful.
            
        Raises:
            StorageError: If copy fails.
        """
        try:
            src = Path(template_path)
            dst = Path(destination)
            
            if not src.exists():
                raise StorageError(f"Template path does not exist: {template_path}")
            
            shutil.copytree(src, dst, dirs_exist_ok=True)
            logger.info(f"Copied template from {template_path} to {destination}")
            return True
        except Exception as e:
            logger.error(f"Failed to copy template from {template_path} to {destination}: {e}")
            raise StorageError(f"Failed to copy template: {e}")
    
    def write_file(self, content: str, destination: str, filename: str) -> bool:
        """
        Write text content to a file.
        
        Args:
            content: Text content to write.
            destination: Destination folder path.
            filename: Name of the file.
            
        Returns:
            True if write was successful.
            
        Raises:
            StorageError: If write fails.
        """
        try:
            dest_path = Path(destination)
            dest_path.mkdir(parents=True, exist_ok=True)
            
            file_path = dest_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Wrote file: {file_path}")
            return True
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
        full_path = os.path.join(str(self.base_path), *path_parts)
        return full_path
