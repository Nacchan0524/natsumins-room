#!/usr/bin/env python3
"""
Example script demonstrating how to use the AWS Environment Visualizer as a library.
"""

import os
import sys
from aws_visualizer import AWSEnvironmentVisualizer

def main():
    """
    Example usage of the AWS Environment Visualizer.
    """
    # Get AWS region and profile from environment variables or use defaults
    region = os.environ.get('AWS_REGION', 'us-east-1')
    profile = os.environ.get('AWS_PROFILE', None)
    
    print(f"Using AWS region: {region}")
    if profile:
        print(f"Using AWS profile: {profile}")
    
    try:
        # Initialize the visualizer
        visualizer = AWSEnvironmentVisualizer(region=region, profile=profile)
        
        # Generate a diagram
        output_path = "example_aws_diagram.png"
        result_path = visualizer.generate_diagram(output_path=output_path)
        
        if result_path:
            print(f"AWS environment diagram generated successfully: {result_path}")
            return 0
        else:
            print("Failed to generate AWS environment diagram")
            return 1
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())