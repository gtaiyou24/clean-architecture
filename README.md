# FastAPI × DDD × Clean Architecture
This API template designed with DDD and Clean Architecture using FastAPI. 
With this template, I implemented a system that provides role-based secure access management service for users.

<details><summary>📁Packages</summary>

 - [fastapi](https://pypi.org/project/fastapi/)
 - [pytest](https://pypi.org/project/pytest/)
 - [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)

</details>

```bash
git clone https://github.com/gtaiyou24/clean-architecture [your-system-name]
```

## 🛠️Architecture

<img src="./doc/clean-architecture.png" height="250" alt="Clean Architecture">

> refer : https://buildersbox.corp-sansan.com/entry/2019/07/10/110000


```
app
├── application  # application layer
├── domain
│   └── model  # domain layer
├── exception  # exception class package
└── port
    └── adapter  # port/adapter layer
        ├── persistence
        ├── resource
        │   └── health
        │       └── health_resource.py
        └── service
```

## 📖How To
### 🏃 Start
```bash
docker-compose up --build
```
 - [Swagger UI](http://localhost:8000/docs)
 - [MailHog](http://0.0.0.0:8025/)

### ✅ Test

```bash
pip install pytest pytest-env httpx

pytest -v ./test
```

## 🔗Appendix

 - [VaughnVernon/IDDD_Samples - github.com](https://github.com/VaughnVernon/IDDD_Samples)
 - [hafizn07/next-auth-v5-advanced-guide-2024 - github.com](https://github.com/hafizn07/next-auth-v5-advanced-guide-2024)
