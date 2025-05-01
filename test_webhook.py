#!/usr/bin/env python3
"""
Test script for the website creation webhook.
Sends test data to the make.com webhook to verify it's working correctly.
"""

import requests
import json
import traceback
from datetime import datetime

# Make.com webhook URL
WEBHOOK_URL = "https://hook.us1.make.com/fs6d6kwennmyj8oos3m12wwbuaw95enw"

def test_webhook():
    """Send test data to the webhook."""
    
    # Create test payload
    payload = {
        "client_id": "test_client",
        "project_id": "test_project_123",
        "client_email": "test@example.com",
        "title": "Test Website Content",
        "created_at": datetime.now().isoformat(),
        "event_type": "website_creation",
        "content_type": "website",
        "message": "Your website has been created! Use your email address as your username and create your own password during the sign-up process.",
        "test": True
    }
    
    print(f"Sending test payload to webhook: {json.dumps(payload, indent=2)}")
    print(f"Webhook URL: {WEBHOOK_URL}")
    
    try:
        # Send POST request to webhook
        print("Sending request...")
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        # Check response
        print(f"Response received with status code: {response.status_code}")
        
        if response.status_code >= 200 and response.status_code < 300:
            print(f"Success! Webhook responded with status code: {response.status_code}")
            try:
                response_json = response.json()
                print(f"Response JSON: {json.dumps(response_json, indent=2)}")
            except:
                print(f"Response text: {response.text}")
        else:
            print(f"Error: Webhook responded with status code: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            print(f"Response text: {response.text}")
            
    except Exception as e:
        print(f"Error sending test data to webhook: {str(e)}")
        print("Traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    print("Starting webhook test...")
    test_webhook()
    print("Test completed.")
