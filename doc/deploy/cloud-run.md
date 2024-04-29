# GCP / Cloud Run

<img src="https://storage.googleapis.com/gweb-cloudblog-publish/images/Cloud_Run.max-2600x2600.jpg" width="400">

## 🏃 手順
### 💡 1. IAM Service Account Credentials API を有効にする
```bash
# Google Cloud SDK と Google アカウントを連携させる
gcloud auth login

# プロジェクトを変更する
gcloud config set project ${PROJECT_ID}

# IAM API を許可する
gcloud services enable iamcredentials.googleapis.com --project=${PROJECT_ID}

# Secret Manager API を許可する
gcloud services enable secretmanager.googleapis.com --project=${PROJECT_ID}
```

### 🛠️ 2. サービスアカウントを作成する

```bash
# サービスアカウントを作成
gcloud iam service-accounts create "github-actions"\
 --project=${PROJECT_ID} \
 --display-name="GitHub Actions サービスアカウント" \
 --description="GitHub Actions が GCP へアプリをデプロイするためのサービスアカウント"

# サービスアカウントが作成できたか確認
gcloud iam service-accounts list
```

GitHub Actions 経由でデプロイするために、本システムで以下のロールを利用します。そのため、予めサービスアカウントに以下のロールを付与します。

| ロール                                | 説明                                   |
|:-----------------------------------|:-------------------------------------|
| `roles/run.admin`                  | Cloud Run を設定し、デプロイするためのロール          |
| `roles/iam.serviceAccountUser`     | サービスアカウントのユーザーとしてのロール                |
| `roles/artifactregistry.repoAdmin` | Artifact Registry へのプッシュ、削除をするためのロール |
| `roles/`                           |  |

```bash
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
 --member="serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
 --role="roles/run.admin"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
 --member="serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
 --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
 --member="serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
 --role="roles/artifactregistry.repoAdmin"
```

### 🛠️ 3. Workload Identity プール・プロバイダを作成する
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


### 👌 4. Workload Identity プロバイダが該当のサービスアカウントの権限を借用することを許可する
最後に、Workload Identity プロバイダからの認証について、目的のサービスアカウントの権限の借用を許可します。

```bash
# サービスアカウントの権限の借用を許可
gcloud iam service-accounts add-iam-policy-binding "github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
  --project="${PROJECT_ID}" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/github-actions-pool/attribute.repository/${GITHUB_REPO_OWNER}/${GITHUB_REPO_NAME}"
```

### 📝 5. GitHub Actions の Variable に GCP 情報を保存する
※もしくは直接 `.github/workflows` 以下の YAML ファイルに書き込む

|            変数             | 説明                      | 例                                                                                               |
|:-------------------------:|:------------------------|:------------------------------------------------------------------------------------------------|
|    `GCP_WIF_PROVIDER`     | Workload Identity プロバイダ | `projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/<プールID>/providers/<プロバイダID>` |
| `GCP_WIF_SERVICE_ACCOUNT` | サービスアカウント               | `github-actions@${PROJECT_ID}.iam.gserviceaccount.com`                                          |
|     `GCP_PROJECT_ID`      | プロジェクトID                | `clean-architecture`                                                                            |

### 🔑 6. GitHub Actions が Secret Manager からクレデンシャル情報を取得できるようにする
データベースのパスワードや JWT で利用するキーなどのクレデンシャル情報を Secret Manager に保存しておきます。

| キー | 値                                         |
|:----|:------------------------------------------|
| `DATABASE_URL` | SQLAlchemy の `create_engine` の引数に指定する URL |
| `JWT_SECRET_KEY` | `jose.jwt` のエンコーディング・でコーディングで指定するキー |

次に GitHub Actions のサービスアカウントに Secret Manager アクセサー ロールを付与します。
```bash
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
 --member="serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
 --role="roles/secretmanager.secretAccessor"
```

### 🚀 6. GitHub の Actions からリリース

<img src="./deploy-production.png">