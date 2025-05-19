# AWS ユーティリティコードとテンプレート集

このリポジトリには、AWSリソースを管理するためのユーティリティコードとCloudFormationテンプレートが含まれています。

## 内容

### 1. 未使用IAMポリシーの削除スクリプト

未使用のカスタマー管理IAMポリシーを検出して削除するためのスクリプト。

- ディレクトリ: `/notuse-customer-iampolicy-delete`
- 参考コード：https://dev.classmethod.jp/articles/aws-iam-delete-unused-customer-managed-policies/

### 2. VPCとEC2インスタンスのCloudFormationテンプレート

AWSでVPCとEC2インスタンスを構築するためのCloudFormationテンプレート。

- ディレクトリ: `/cloudformation-templates`
- 含まれるテンプレート:
  - `vpc-ec2-template.yaml`: 完全なネットワーク構成を持つVPCとEC2インスタンス
  - `simple-vpc-ec2-template.yaml`: シンプルなVPCとEC2インスタンス

詳細な使用方法については、各ディレクトリ内のREADMEファイルを参照してください。
