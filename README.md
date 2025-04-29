## Directory Hierarchy

```
|—— .env
|—— .env-example
|—— .env-prd
|—— .python-version
|—— .gitignore
|—— .dockerignore
|—— alembic.ini
|—— poetry.lock
|—— poetry.toml
|—— pyproject.toml
|—— Dockerfile
|—— docker-compose.yml
|—— entrypoint.sh
|—— migrations
|    |—— README
|    |—— env.py
|    |—— script.py.mako
|    |—— versions
|        |—— ...
|—— src
|    |—— app
|        |—— api
|            |—— libs
|                |—— __init__.py
|                |—— scheduler.py
|            |—— resolvers
|                |—— __init__.py
|                |—— short.py
|            |—— types
|                |—— __init__.py
|                |—— short.py
|            |—— __init__.py
|            |—— schema.py
|        |—— core
|            |—— __init__.py
|            |—— config.py
|            |—— database.py
|        |—— __init__.py
|        |—— main.py
|        |—— models
|            |—— __init__.py
|            |—— short.py
|        |—— static
|            |—— index.html
|            |—— styles.css
```
