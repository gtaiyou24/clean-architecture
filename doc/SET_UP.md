# 💻 セットアップ方法

## 1. システム名をリネーム
デフォルトでは、API 名、DB 名、Docker コンテナ名などがテンプレートのリポジトリ名になっているのでこれを変更します。
```bash
# replace 'clean-architecture' to your system name
sh ./bin/rename.sh $YOUR_SYSTEM_NAME
```

## 2. GitHub Actions を有効化
このテンプレートリポジトリでは、`.github/workflows` にワークフローを定義しています。このワークフローを動かすために予め以下の設定をしてください。

 1. GitHub リポジトリの `settings` > `actions` を開く。
 2. `Workflow permissions` を `Read and write permissions` に変更してください。
