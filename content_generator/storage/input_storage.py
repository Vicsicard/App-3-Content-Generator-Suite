"""Supabase Storage Manager for App 3 Input Files.

Handles fetching input files (transcript and style profile) from Supabase Storage.
"""

from typing import Dict, Optional, Tuple
import os
from supabase import create_client, Client


class InputStorageManager:
    """Manages fetching input files from Supabase storage."""
    
    def __init__(self):
        """Initialize Supabase client and storage settings."""
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        self.client: Optional[Client] = None
        self.bucket_name = "content"
        
    def initialize(self) -> None:
        """Initialize Supabase client."""
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Supabase URL and key must be set in environment variables")
            
        self.client = create_client(self.supabase_url, self.supabase_key)
    
    def fetch_input_file(self, path: str) -> str:
        """Fetch input file content from Supabase storage.
        
        Args:
            path: Path to file in storage bucket (e.g. 'client-files/annie/transcript_chunks.md')
            
        Returns:
            File content as string
        """
        if not self.client:
            self.initialize()
            
        try:
            response = self.client.storage.from_(self.bucket_name).download(path)
            content = response.decode('utf-8')
            print(f"Successfully fetched {path}")
            return content
        except Exception as e:
            raise RuntimeError(f"Failed to fetch {path}: {str(e)}")
            
    def fetch_input_files(self, client_id: str = "annie") -> Tuple[str, str]:
        """Fetch both transcript and style profile for a client.
        
        Args:
            client_id: Client identifier (e.g. 'annie')
            
        Returns:
            Tuple of (transcript_content, style_profile_content)
        """
        base_path = f"client-files/{client_id}"
        transcript_path = f"{base_path}/transcript_chunks.md"
        style_path = f"{base_path}/style-profile.md"
        
        print(f"Fetching input files for client {client_id}:")
        print(f"- Transcript: {transcript_path}")
        print(f"- Style Profile: {style_path}")
        
        transcript = self.fetch_input_file(transcript_path)
        style_profile = self.fetch_input_file(style_path)
        
        return transcript, style_profile


# Create singleton instance
input_storage = InputStorageManager()
