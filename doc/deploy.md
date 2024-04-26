# Deploy

## AWS / Lambda
<img src="https://d2908q01vomqb2.cloudfront.net/1b6453892473a467d07372d45eb05abc2031647a/2023/02/23/lambda_service.png" height="200">

```bash
cd app
touch start_lambda.py
```

```python
# at start_lambda.py
from mangum import Mangum

from app import app

handler = Mangum(app, lifespan='on', api_gateway_base_path='/')
```


## AWS / Lightsail
WIP


## GCP / Cloud Run

<img src="https://storage.googleapis.com/gweb-cloudblog-publish/images/Cloud_Run.max-2600x2600.jpg" height="200">

WIP
