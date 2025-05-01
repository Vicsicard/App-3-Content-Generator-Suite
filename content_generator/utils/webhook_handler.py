"""Webhook handler for Content Generator Suite.

Handles webhook triggers for various events, including website creation.
"""

import os
import json
import logging
import requests
from typing import Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

# Import Supabase client
from ..database.supabase_client import supabase

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebhookHandler:
    """Handles webhook triggers for Content Generator Suite."""
    
    def __init__(self):
        """Initialize webhook handler."""
        # Use the provided make.com webhook URL
        self.website_creation_webhook_url = "https://hook.us1.make.com/fs6d6kwennmyj8oos3m12wwbuaw95enw"
        
        logger.info(f"Webhook handler initialized with URL: {self.website_creation_webhook_url}")
    
    def trigger_website_creation(self, client_id: str, content_record: Dict[str, Any]) -> bool:
        """Trigger webhook for website creation.
        
        Args:
            client_id: Client identifier
            content_record: Content record from database
            
        Returns:
            bool: True if webhook was triggered successfully, False otherwise
        """
        if not self.website_creation_webhook_url:
            logger.warning("Cannot trigger website creation webhook: URL not configured")
            return False
        
        # Get client email
        client_email = self._get_client_email(client_id)
        
        # Get project ID
        project_id = content_record.get("id", "")
        
        # Check if notification has already been sent
        if self._notification_already_sent(client_email, project_id):
            logger.info(f"Notification already sent for client {client_id}, project {project_id}")
            return True
            
        try:
            # Prepare payload for webhook
            payload = {
                "client_id": client_id,
                "project_id": project_id,
                "title": content_record.get("title", "Website Content"),
                "created_at": content_record.get("created_at", ""),
                "event_type": "website_creation",
                "content_type": "website",
                "message": "Your website has been created! Use your email address as your username and create your own password during the sign-up process."
            }
            
            # Add client email if available
            if client_email:
                payload["client_email"] = client_email
                
            # Log webhook trigger attempt
            logger.info(f"Triggering website creation webhook for client: {client_id}")
            
            # Send webhook request
            response = requests.post(
                self.website_creation_webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            # Check response
            if response.status_code >= 200 and response.status_code < 300:
                logger.info(f"Successfully triggered website creation webhook: {response.status_code}")
                
                # Update notification status in database
                self._update_notification_status(
                    client_email, 
                    project_id, 
                    True, 
                    "sent", 
                    response.status_code
                )
                
                return True
            else:
                logger.error(
                    f"Failed to trigger website creation webhook: {response.status_code} - {response.text}"
                )
                
                # Update notification status in database
                self._update_notification_status(
                    client_email, 
                    project_id, 
                    False, 
                    "failed", 
                    response.status_code
                )
                
                return False
                
        except Exception as e:
            logger.error(f"Error triggering website creation webhook: {str(e)}")
            
            # Update notification status in database
            self._update_notification_status(
                client_email, 
                project_id, 
                False, 
                f"error: {str(e)}", 
                None
            )
            
            return False
    
    def _notification_already_sent(self, client_email: Optional[str], project_id: str) -> bool:
        """Check if notification has already been sent.
        
        Args:
            client_email: Client email
            project_id: Project ID
            
        Returns:
            bool: True if notification has already been sent, False otherwise
        """
        if not client_email or not project_id:
            return False
            
        try:
            # Initialize Supabase client
            client = supabase.get_client()
            
            # Check if record exists with notification_sent=True
            result = client.table('user_projects')\
                .select('notification_sent')\
                .eq('user_email', client_email)\
                .eq('project_id', project_id)\
                .eq('notification_sent', True)\
                .execute()
                
            # Return True if any records found with notification_sent=True
            return bool(result.data and len(result.data) > 0)
                
        except Exception as e:
            logger.error(f"Error checking notification status: {str(e)}")
            # Default to False if error occurs to ensure notification is sent
            return False
    
    def _update_notification_status(
        self, 
        client_email: Optional[str], 
        project_id: str, 
        sent: bool, 
        status: str, 
        status_code: Optional[int]
    ) -> None:
        """Update notification status in database.
        
        Args:
            client_email: Client email
            project_id: Project ID
            sent: Whether notification was sent successfully
            status: Status message
            status_code: HTTP status code
        """
        if not client_email or not project_id:
            logger.warning("Cannot update notification status: missing client_email or project_id")
            return
            
        try:
            # Initialize Supabase client
            client = supabase.get_client()
            
            # Check if record exists
            result = client.table('user_projects')\
                .select('id')\
                .eq('user_email', client_email)\
                .eq('project_id', project_id)\
                .execute()
                
            # Prepare update data
            update_data = {
                'notification_sent': sent,
                'notification_sent_at': datetime.now().isoformat(),
                'notification_status': status,
                'notification_status_code': status_code
            }
                
            if result.data and len(result.data) > 0:
                # Update existing record
                client.table('user_projects')\
                    .update(update_data)\
                    .eq('user_email', client_email)\
                    .eq('project_id', project_id)\
                    .execute()
                    
                logger.info(f"Updated notification status for {client_email}, project {project_id}")
            else:
                # Create new record
                new_record = {
                    'user_email': client_email,
                    'project_id': project_id,
                    **update_data
                }
                
                client.table('user_projects')\
                    .insert(new_record)\
                    .execute()
                    
                logger.info(f"Created notification record for {client_email}, project {project_id}")
                
        except Exception as e:
            logger.error(f"Error updating notification status: {str(e)}")
    
    def _get_client_email(self, client_id: str) -> Optional[str]:
        """Get client email from client ID.
        
        Args:
            client_id: Client identifier
            
        Returns:
            Optional[str]: Client email if found, None otherwise
        """
        # TODO: Implement client email lookup from database
        # For now, we'll use a simple mapping or return None
        
        # This is a placeholder - in a real implementation, you would
        # query your database or user management system
        client_email_mapping = {
            # Add known client mappings here if available
        }
        
        return client_email_mapping.get(client_id)

# Create singleton instance
webhook_handler = WebhookHandler()
