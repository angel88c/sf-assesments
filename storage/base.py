"""
Base Storage Provider Module

This module defines the abstract interface for storage providers.
All storage implementations must inherit from this base class.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, BinaryIO


class StorageProvider(ABC):
    """
    Abstract base class for storage providers.
    
    This interface defines all operations needed for file storage,
    allowing different implementations (local filesystem, SharePoint, etc.)
    to be used interchangeably.
    """
    
    @abstractmethod
    def create_folder(self, path: str) -> bool:
        """
        Create a folder at the specified path.
        
        Args:
            path: Path where to create the folder.
            
        Returns:
            True if folder was created successfully, False otherwise.
            
        Raises:
            StorageError: If folder creation fails.
        """
        pass
    
    @abstractmethod
    def folder_exists(self, path: str) -> bool:
        """
        Check if a folder exists.
        
        Args:
            path: Path to check.
            
        Returns:
            True if folder exists, False otherwise.
        """
        pass
    
    @abstractmethod
    def upload_file(self, file_content: BinaryIO, destination: str, filename: str) -> bool:
        """
        Upload a file to the specified destination.
        
        Args:
            file_content: File content as binary stream.
            destination: Destination folder path.
            filename: Name of the file.
            
        Returns:
            True if upload was successful, False otherwise.
            
        Raises:
            StorageError: If upload fails.
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def copy_template(self, template_path: str, destination: str) -> bool:
        """
        Copy a template folder to a destination.
        
        Args:
            template_path: Path to the template folder.
            destination: Destination path.
            
        Returns:
            True if copy was successful, False otherwise.
            
        Raises:
            StorageError: If copy fails.
        """
        pass
    
    @abstractmethod
    def write_file(self, content: str, destination: str, filename: str) -> bool:
        """
        Write text content to a file.
        
        Args:
            content: Text content to write.
            destination: Destination folder path.
            filename: Name of the file.
            
        Returns:
            True if write was successful, False otherwise.
            
        Raises:
            StorageError: If write fails.
        """
        pass
    
    @abstractmethod
    def get_full_path(self, *path_parts: str) -> str:
        """
        Get full path by joining path parts.
        
        Args:
            path_parts: Path components to join.
            
        Returns:
            Full path as string.
        """
        pass
