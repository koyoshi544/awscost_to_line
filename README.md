## AWS料金通知

- AWSの請求金額を毎日1回 LINEに通知する仕組み。
- AWS Lambdaを使用している。
  - 関数名：`awscost_to_line`
- LINEに通知する方法として、LINE Messaging APIを使用している。
- 元々はネットで調べたコードを、ほぼそのままコピペして利用していた。
  - 今となっては出典不明。
---
- (2025/01/23) LINE Notifyがサービス終了予定のため、LINE Messaging APIを利用するように変更。
