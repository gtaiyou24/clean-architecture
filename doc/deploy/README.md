# 🚀 How to deploy
## AWS / Lambda
<img src="https://d2908q01vomqb2.cloudfront.net/1b6453892473a467d07372d45eb05abc2031647a/2023/02/23/lambda_service.png" height="100">

WIP


## AWS / Lightsail
WIP


## GCP / Cloud Run

<img src="https://storage.googleapis.com/gweb-cloudblog-publish/images/Cloud_Run.max-2600x2600.jpg" height="100">

**1. IAM Service Account Credentials API を有効にする**
```bash
# Google Cloud SDK と Google アカウントを連携させる
gcloud auth login

# プロジェクトを変更する
gcloud config set project ${PROJECT_ID}

gcloud services enable iamcredentials.googleapis.com \
  --project=${PROJECT_ID}
```

**2. サービスアカウントを作成する**
```bash
# サービスアカウントを作成
gcloud iam service-accounts create "github-actions"\
 --project=${PROJECT_ID} \
 --display-name="GitHub Actions サービスアカウント" \
 --description="GitHub Actions が GCP へアプリをデプロイするためのサービスアカウント"

# サービスアカウントが作成できたか確認
gcloud iam service-accounts list
```

サービス アカウントには、イメージを push し、Cloud Run サービス アカウントの権限を借用して Cloud Run をデプロイできるロールが必要とされます。以下のロールが必要です。
```bash
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
 --member="serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
 --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
 --member="serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
 --role="roles/run.admin"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
 --member="serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
 --role="roles/iam.serviceAccountUser"
```

**3. Workload Identity プール・プロバイダを作成する**

GitHub Actions 経由で Cloud Run へデプロイするには、 Workload Identity プールと Workload Identity プロバイダを作成して Workload Identity 連携を設定および構成する必要があります。
```bash
# Workload Identity プールを作成
gcloud iam workload-identity-pools create "github-actions-pool" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --display-name="GitHub Actions プール"

# Workload Identity プロバイダを作成
gcloud iam workload-identity-pools providers create-oidc "github-actions-provider" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="github-actions-pool" \
  --display-name="GitHub Actions Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository,attribute.actor=assertion.actor" \
  --issuer-uri="https://token.actions.githubusercontent.com"
```

最後に、Workload Identity プロバイダからの認証について、目的のサービスアカウントの権限の借用を許可します。
```bash
# サービスアカウントの権限の借用を許可
gcloud iam service-accounts add-iam-policy-binding "github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
  --project="${PROJECT_ID}" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/github-actions-pool/attribute.repository/${GITHUB_REPO_OWNER}/${GITHUB_REPO_NAME}"
```

シークレット情報
| Secret | Description | Example |
|:------:|:------------|:--------|
| `GCP_WIF_PROVIDER` | Workload Identity プロバイダ | `projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/<プールID>/providers/<プロバイダID>` |
| `GCP_WIF_SERVICE_ACCOUNT` | サービスアカウント | `github-actions@${PROJECT_ID}.iam.gserviceaccount.com` |

変数情報

| Variable | Description |
|:--------:|:------------|
| `GCP_PROJECT_ID` | プロジェクトID |
