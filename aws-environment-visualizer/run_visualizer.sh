#!/bin/bash

# Run AWS Environment Visualizer
# This script makes it easier to run the AWS environment visualizer

set -e

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is required but not installed. Please install pip3 and try again."
    exit 1
fi

# Install dependencies if needed
echo "Checking dependencies..."
pip3 install -r requirements.txt

# Parse command line arguments
REGION=""
PROFILE=""
OUTPUT=""

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --region)
            REGION="--region $2"
            shift
            shift
            ;;
        --profile)
            PROFILE="--profile $2"
            shift
            shift
            ;;
        --output)
            OUTPUT="--output $2"
            shift
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Run the visualizer
echo "Running AWS Environment Visualizer..."
python3 aws_visualizer.py $REGION $PROFILE $OUTPUT

# Check if the script ran successfully
if [ $? -eq 0 ]; then
    echo "AWS Environment Visualizer completed successfully."
else
    echo "AWS Environment Visualizer failed."
    exit 1
fi