#!/usr/bin/env python3
"""
AWS Environment Visualizer

This script uses Amazon Q Developer to analyze an AWS environment and generate
a configuration diagram of the AWS resources.

Requirements:
- AWS CLI configured with appropriate permissions
- boto3
- Amazon Q Developer SDK
"""

import os
import sys
import time
import json
import argparse
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

import boto3
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AWSEnvironmentVisualizer:
    """
    A class to visualize AWS environment using Amazon Q Developer.
    """
    
    def __init__(self, region: str = None, profile: str = None):
        """
        Initialize the visualizer with AWS credentials.
        
        Args:
            region: AWS region to use
            profile: AWS profile to use
        """
        self.region = region or os.environ.get('AWS_REGION', 'us-east-1')
        self.profile = profile
        self.session = self._create_session()
        self.q_client = self.session.client('q')
        
    def _create_session(self) -> boto3.Session:
        """
        Create a boto3 session with the specified profile and region.
        
        Returns:
            boto3.Session: A configured boto3 session
        """
        try:
            if self.profile:
                session = boto3.Session(profile_name=self.profile, region_name=self.region)
            else:
                session = boto3.Session(region_name=self.region)
            return session
        except Exception as e:
            logger.error(f"Failed to create AWS session: {str(e)}")
            raise
    
    def list_aws_services(self) -> List[str]:
        """
        List all AWS services in use in the current account.
        
        Returns:
            List[str]: List of AWS service names
        """
        services = []
        try:
            # Get list of available services
            available_services = self.session.get_available_services()
            
            # Check which services have resources
            for service_name in available_services:
                try:
                    client = self.session.client(service_name)
                    # Try to list resources for this service
                    # This is a simplified approach and may not work for all services
                    if hasattr(client, 'list_resources'):
                        resources = client.list_resources()
                        if resources:
                            services.append(service_name)
                except (ClientError, AttributeError):
                    # Skip services that don't support listing resources
                    continue
        except Exception as e:
            logger.error(f"Error listing AWS services: {str(e)}")
        
        return services
    
    def generate_diagram(self, output_path: str = None) -> str:
        """
        Generate a configuration diagram using Amazon Q Developer.
        
        Args:
            output_path: Path to save the diagram
            
        Returns:
            str: Path to the generated diagram
        """
        try:
            logger.info("Starting AWS environment analysis with Amazon Q Developer")
            
            # Create a conversation with Amazon Q Developer
            conversation_id = self._start_q_conversation()
            
            # Ask Amazon Q to generate a diagram of the AWS environment
            prompt = "Generate a comprehensive architecture diagram of my current AWS environment showing all resources and their relationships."
            
            # Send the prompt to Amazon Q
            response = self.q_client.send_message(
                conversationId=conversation_id,
                message=prompt
            )
            
            # Process the response
            diagram_content = self._extract_diagram_from_response(response)
            
            if not diagram_content:
                logger.warning("No diagram was generated in the response")
                return None
            
            # Save the diagram
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"aws_architecture_{timestamp}.png"
            
            with open(output_path, 'wb') as f:
                f.write(diagram_content)
            
            logger.info(f"Diagram saved to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating diagram: {str(e)}")
            raise
    
    def _start_q_conversation(self) -> str:
        """
        Start a new conversation with Amazon Q Developer.
        
        Returns:
            str: Conversation ID
        """
        try:
            response = self.q_client.create_conversation()
            conversation_id = response.get('conversationId')
            logger.info(f"Started Amazon Q conversation with ID: {conversation_id}")
            return conversation_id
        except Exception as e:
            logger.error(f"Failed to start Amazon Q conversation: {str(e)}")
            raise
    
    def _extract_diagram_from_response(self, response: Dict[str, Any]) -> Optional[bytes]:
        """
        Extract diagram content from Amazon Q response.
        
        Args:
            response: Response from Amazon Q
            
        Returns:
            bytes: Diagram content as bytes
        """
        try:
            # This is a placeholder implementation since the exact API response format
            # for Amazon Q Developer might differ. Adjust according to actual API.
            
            # Check if there's an attachment in the response
            attachments = response.get('attachments', [])
            for attachment in attachments:
                if attachment.get('type') == 'image/png' or attachment.get('type') == 'image/svg+xml':
                    # Get the attachment content
                    attachment_id = attachment.get('attachmentId')
                    attachment_response = self.q_client.get_attachment(
                        conversationId=response.get('conversationId'),
                        attachmentId=attachment_id
                    )
                    return attachment_response.get('content')
            
            # If no direct attachment, check if there's a URL to download the diagram
            message_content = response.get('message', {}).get('content', '')
            # Parse message content for URLs or other indicators of diagram location
            # This is highly dependent on how Amazon Q actually returns diagrams
            
            return None
        except Exception as e:
            logger.error(f"Error extracting diagram from response: {str(e)}")
            return None

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='AWS Environment Visualizer')
    parser.add_argument('--region', help='AWS region to use')
    parser.add_argument('--profile', help='AWS profile to use')
    parser.add_argument('--output', help='Output path for the diagram')
    return parser.parse_args()

def main():
    """Main entry point for the script."""
    args = parse_arguments()
    
    try:
        visualizer = AWSEnvironmentVisualizer(region=args.region, profile=args.profile)
        output_path = visualizer.generate_diagram(output_path=args.output)
        
        if output_path:
            print(f"AWS environment diagram generated successfully: {output_path}")
            return 0
        else:
            print("Failed to generate AWS environment diagram")
            return 1
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())