# 🚀 How to deploy
## AWS / Lambda
<img src="https://d2908q01vomqb2.cloudfront.net/1b6453892473a467d07372d45eb05abc2031647a/2023/02/23/lambda_service.png" height="100">

WIP


## AWS / Lightsail
WIP


## GCP / Cloud Run

<img src="https://storage.googleapis.com/gweb-cloudblog-publish/images/Cloud_Run.max-2600x2600.jpg" height="100">

GitHub Actions 経由で Cloud Run へデプロイするには、 Workload Identity プールと Workload Identity プロバイダを作成して Workload Identity 連携を設定および構成する必要があります。
```bash
# Google Cloud SDK と Google アカウントを連携させる
gcloud auth login

# Workload Identity プールを作成
gcloud iam workload-identity-pools create "my-pool" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --display-name="Demo pool"

# Workload Identity プロバイダを作成
gcloud iam workload-identity-pools providers create-oidc "my-provider" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="my-pool" \
  --display-name="Demo provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.aud=assertion.aud" \
  --issuer-uri="https://token.actions.githubusercontent.com"
```

最後に、Workload Identity プロバイダからの認証について、目的のサービスアカウントの権限の借用を許可します。
```bash
gcloud iam service-accounts add-iam-policy-binding "my-service-account@${PROJECT_ID}.iam.gserviceaccount.com" \
  --project="${PROJECT_ID}" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/my-org/my-repo"
```

シークレット情報

| Secret | Description |
|:------:|:------------|
| `GCP_WIF_PROVIDER` | Workload Identity プロバイダ |
| `GCP_WIF_SERVICE_ACCOUNT` | サービスアカウント |

変数情報

| Variable | Description |
|:--------:|:------------|
| `GCP_PROJECT_ID` | プロジェクトID |
