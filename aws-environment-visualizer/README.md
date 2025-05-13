# AWS Environment Visualizer

This tool uses Amazon Q Developer to analyze your AWS environment and automatically generate architecture diagrams showing your AWS resources and their relationships.

## Features

- Connects to your AWS environment using your configured credentials
- Uses Amazon Q Developer to analyze your AWS infrastructure
- Generates comprehensive architecture diagrams
- Supports different AWS regions and profiles
- Saves diagrams in PNG format

## Prerequisites

- Python 3.8 or higher
- AWS CLI configured with appropriate permissions
- Amazon Q Developer access enabled for your AWS account

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script with the following command:

```bash
python aws_visualizer.py [--region REGION] [--profile PROFILE] [--output OUTPUT_PATH]
```

### Arguments

- `--region`: AWS region to use (defaults to AWS_REGION environment variable or 'us-east-1')
- `--profile`: AWS profile to use (defaults to default profile)
- `--output`: Path to save the generated diagram (defaults to 'aws_architecture_TIMESTAMP.png')

### Example

```bash
python aws_visualizer.py --region us-west-2 --profile dev --output my_aws_diagram.png
```

## Required Permissions

The AWS user or role running this script needs the following permissions:

- Read-only access to AWS services for environment discovery
- Access to Amazon Q Developer API

You can use the AWS managed policy `ReadOnlyAccess` and add specific permissions for Amazon Q Developer.

## Notes on Amazon Q Developer

Amazon Q Developer is an AI-powered assistant that can help with various development tasks, including generating architecture diagrams. This tool leverages Amazon Q's capabilities to analyze your AWS environment and create visual representations of your infrastructure.

To use this tool, you need to have Amazon Q Developer enabled for your AWS account. For more information, visit the [Amazon Q Developer documentation](https://aws.amazon.com/q/).