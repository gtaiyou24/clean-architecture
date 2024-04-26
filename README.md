# FastAPI × DDD × Clean Architecture
DDD API template designed with Clean Architecture using FastAPI

<details><summary>📁Packages</summary>

 - [fastapi](https://pypi.org/project/fastapi/)
 - [pytest](https://pypi.org/project/pytest/)
 - [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)

</details>

```bash
git clone https://github.com/gtaiyou24/clean-architecture [your-system-name]
```

## 🛠️Architecture

<img src="./doc/clean-architecture.png" height="400" alt="Clean Architecture">

> refer : https://buildersbox.corp-sansan.com/entry/2019/07/10/110000


```
app
├── app.py
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
### 🏃Start
```bash
docker-compose up --build
```

open [localhost:8000/docs](http://localhost:8000/docs)

### ✅Test

```bash
pytest -v ./test
```

## 🔗Appendix

 - [VaughnVernon/IDDD_Samples - github.com](https://github.com/VaughnVernon/IDDD_Samples)
