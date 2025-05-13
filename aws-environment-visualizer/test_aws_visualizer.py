#!/usr/bin/env python3
"""
Unit tests for the AWS Environment Visualizer.
"""

import os
import unittest
from unittest.mock import patch, MagicMock

from aws_visualizer import AWSEnvironmentVisualizer

class TestAWSEnvironmentVisualizer(unittest.TestCase):
    """Test cases for AWSEnvironmentVisualizer class."""
    
    @patch('boto3.Session')
    def setUp(self, mock_session):
        """Set up test fixtures."""
        self.mock_session = mock_session
        self.mock_q_client = MagicMock()
        self.mock_session.return_value.client.return_value = self.mock_q_client
        self.visualizer = AWSEnvironmentVisualizer(region='us-east-1')
    
    def test_init(self):
        """Test initialization of the visualizer."""
        self.assertEqual(self.visualizer.region, 'us-east-1')
        self.assertIsNone(self.visualizer.profile)
        self.mock_session.assert_called_once_with(region_name='us-east-1')
        
    @patch('boto3.Session')
    def test_init_with_profile(self, mock_session):
        """Test initialization with a profile."""
        visualizer = AWSEnvironmentVisualizer(region='us-west-2', profile='dev')
        self.assertEqual(visualizer.region, 'us-west-2')
        self.assertEqual(visualizer.profile, 'dev')
        mock_session.assert_called_once_with(profile_name='dev', region_name='us-west-2')
    
    def test_start_q_conversation(self):
        """Test starting a conversation with Amazon Q Developer."""
        self.mock_q_client.create_conversation.return_value = {'conversationId': 'test-conversation-id'}
        conversation_id = self.visualizer._start_q_conversation()
        self.assertEqual(conversation_id, 'test-conversation-id')
        self.mock_q_client.create_conversation.assert_called_once()
    
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_generate_diagram(self, mock_open):
        """Test generating a diagram."""
        # Mock the conversation creation
        self.mock_q_client.create_conversation.return_value = {'conversationId': 'test-conversation-id'}
        
        # Mock the send_message response
        mock_response = {
            'conversationId': 'test-conversation-id',
            'attachments': [
                {
                    'attachmentId': 'test-attachment-id',
                    'type': 'image/png'
                }
            ]
        }
        self.mock_q_client.send_message.return_value = mock_response
        
        # Mock the get_attachment response
        self.mock_q_client.get_attachment.return_value = {
            'content': b'test-diagram-content'
        }
        
        # Call the method
        output_path = self.visualizer.generate_diagram(output_path='test_diagram.png')
        
        # Assertions
        self.assertEqual(output_path, 'test_diagram.png')
        self.mock_q_client.create_conversation.assert_called_once()
        self.mock_q_client.send_message.assert_called_once_with(
            conversationId='test-conversation-id',
            message='Generate a comprehensive architecture diagram of my current AWS environment showing all resources and their relationships.'
        )
        self.mock_q_client.get_attachment.assert_called_once_with(
            conversationId='test-conversation-id',
            attachmentId='test-attachment-id'
        )
        mock_open.assert_called_once_with('test_diagram.png', 'wb')
        mock_open().write.assert_called_once_with(b'test-diagram-content')
    
    def test_extract_diagram_from_response_with_attachment(self):
        """Test extracting diagram from response with attachment."""
        # Mock response with attachment
        mock_response = {
            'conversationId': 'test-conversation-id',
            'attachments': [
                {
                    'attachmentId': 'test-attachment-id',
                    'type': 'image/png'
                }
            ]
        }
        
        # Mock get_attachment response
        self.mock_q_client.get_attachment.return_value = {
            'content': b'test-diagram-content'
        }
        
        # Call the method
        result = self.visualizer._extract_diagram_from_response(mock_response)
        
        # Assertions
        self.assertEqual(result, b'test-diagram-content')
        self.mock_q_client.get_attachment.assert_called_once_with(
            conversationId='test-conversation-id',
            attachmentId='test-attachment-id'
        )
    
    def test_extract_diagram_from_response_no_attachment(self):
        """Test extracting diagram from response without attachment."""
        # Mock response without attachment
        mock_response = {
            'conversationId': 'test-conversation-id',
            'message': {
                'content': 'No diagram available'
            }
        }
        
        # Call the method
        result = self.visualizer._extract_diagram_from_response(mock_response)
        
        # Assertions
        self.assertIsNone(result)
        self.mock_q_client.get_attachment.assert_not_called()

if __name__ == '__main__':
    unittest.main()