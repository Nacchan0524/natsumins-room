# AWS CloudFormation テンプレート: VPCとEC2インスタンス

このディレクトリには、AWSでVPCとEC2インスタンスを構築するためのCloudFormationテンプレートが含まれています。

## テンプレートの種類

1. **vpc-ec2-template.yaml** - 完全なネットワーク構成を持つVPCとEC2インスタンスを作成します
   - パブリックサブネット（2つ）とプライベートサブネット（2つ）
   - インターネットゲートウェイ
   - 適切なルートテーブル設定
   - セキュリティグループ
   - EC2インスタンス（Amazon Linux 2）

2. **simple-vpc-ec2-template.yaml** - シンプルなVPCとEC2インスタンスを作成します
   - 単一のパブリックサブネット
   - インターネットゲートウェイ
   - 基本的なルートテーブル設定
   - セキュリティグループ
   - EC2インスタンス（Amazon Linux 2）

## 使用方法

### AWS Management Consoleから使用する場合

1. AWS Management Consoleにログインします
2. CloudFormationサービスに移動します
3. 「スタックの作成」をクリックします
4. 「テンプレートの準備完了」を選択します
5. 「テンプレートファイルのアップロード」を選択し、テンプレートファイルをアップロードします
6. 必要なパラメータを入力し、スタックを作成します

### AWS CLIから使用する場合

```bash
# vpc-ec2-template.yamlを使用する場合
aws cloudformation create-stack \
  --stack-name vpc-ec2-stack \
  --template-body file://vpc-ec2-template.yaml \
  --parameters ParameterKey=KeyName,ParameterValue=your-key-pair-name

# simple-vpc-ec2-template.yamlを使用する場合
aws cloudformation create-stack \
  --stack-name simple-vpc-ec2-stack \
  --template-body file://simple-vpc-ec2-template.yaml \
  --parameters ParameterKey=KeyName,ParameterValue=your-key-pair-name
```

## パラメータ

### vpc-ec2-template.yaml のパラメータ

- **EnvironmentName**: 環境名（開発、テスト、本番など）
- **VpcCIDR**: VPCのCIDRブロック
- **PublicSubnet1CIDR**: パブリックサブネット1のCIDRブロック
- **PublicSubnet2CIDR**: パブリックサブネット2のCIDRブロック
- **PrivateSubnet1CIDR**: プライベートサブネット1のCIDRブロック
- **PrivateSubnet2CIDR**: プライベートサブネット2のCIDRブロック
- **InstanceType**: EC2インスタンスタイプ
- **KeyName**: EC2インスタンスにアクセスするためのキーペア名
- **SSHLocation**: SSHアクセスを許可するIPアドレス範囲

### simple-vpc-ec2-template.yaml のパラメータ

- **VpcCIDR**: VPCのCIDRブロック
- **SubnetCIDR**: パブリックサブネットのCIDRブロック
- **InstanceType**: EC2インスタンスタイプ
- **KeyName**: EC2インスタンスにアクセスするためのキーペア名

## 出力

テンプレートは、作成されたリソースのIDやIPアドレスなどの情報を出力します。これらの情報は、CloudFormationスタックの「出力」タブで確認できます。