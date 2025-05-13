# AWS Tools Collection

This repository contains a collection of tools for AWS environment management and visualization.

## Tools

### 1. Unused IAM Policy Deletion Tool

未使用ポリシーの削除・参考コード：https://dev.classmethod.jp/articles/aws-iam-delete-unused-customer-managed-policies/

This tool helps identify and delete unused IAM policies in your AWS account.

### 2. AWS Environment Visualizer

A tool that uses Amazon Q Developer to analyze your AWS environment and automatically generate architecture diagrams.

#### Features
- Connects to your AWS environment using your configured credentials
- Uses Amazon Q Developer to analyze your AWS infrastructure
- Generates comprehensive architecture diagrams
- Supports different AWS regions and profiles

#### Usage
```bash
cd aws-environment-visualizer
./run_visualizer.sh --region us-east-1 --profile default --output my_diagram.png
```

For more details, see the [AWS Environment Visualizer README](aws-environment-visualizer/README.md).
