# Clean Architecture
This API template designed with DDD and Clean Architecture using FastAPI.

With this template, I implemented a system that provides role-based secure access management service for users.

 - python 3.12
 - [fastapi](https://pypi.org/project/fastapi/)
 - [pytest](https://pypi.org/project/pytest/)
 - [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)

## 📖How To
### 💻 Set Up

READ [SET_UP.md](./doc/SET_UP.md)

### 🏃 Start
```bash
docker-compose up --build
```
 - [Swagger UI](http://localhost:8000/docs)
 - [MailHog](http://0.0.0.0:8025/)

```bash
mysql -h 127.0.0.1 -P 3306 -u user -p
# Enter password: pass
```

### ✅ Test

```bash
pip install pytest pytest-env httpx
pytest -v ./test
```

## 🛠 Architecture
### 🛠 Infra

<img src="./doc/infra.png" height="400" alt="Infra">

### 🛠 Application

<img src="./doc/clean-architecture.png" height="250" alt="Clean Architecture">

> refer : https://buildersbox.corp-sansan.com/entry/2019/07/10/110000


<details><summary>📁directory</summary>

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

</details>

## 🔗Appendix

 - [VaughnVernon/IDDD_Samples - github.com](https://github.com/VaughnVernon/IDDD_Samples)
 - [hafizn07/next-auth-v5-advanced-guide-2024 - github.com](https://github.com/hafizn07/next-auth-v5-advanced-guide-2024)
