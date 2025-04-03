## 🚀 Sample Model Context Protocol Demos

GitHub folk: https://github.com/aws-samples/Sample-Model-Context-Protocol-Demos

### postgres mcp-server를 추가했습니다. ###

### ✅ Prerequisites
- Python 3.13+
- PostgreSQL (via Docker)

#### Start PostgreSQL with Docker Compose

```bash
  docker-compose -f docker-compose/docker-compose.yml up -d
```

#### Initialize the Database

- SQL initialization script: /init/init.sql  
  (Includes both DDL and DML)

---

### ⚡ Quick Start

1. Set up a virtual environment (recommended):

```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
  pip install -r init/requirements.txt
```
3. Run
```bash
  python3 main.py
```

---


### 🐘 PostgreSQL Driver Issue (psycopg)

만약, 아래 오류가 출력된다면 
```
ImportError: no pq wrapper available.
Attempts made:
- couldn't import psycopg 'c' implementation: No module named 'psycopg_c'
- couldn't import psycopg 'binary' implementation: No module named 'psycopg_binary'
- couldn't import psycopg 'python' implementation: libpq library not found
```

아래  PostgreSQL client libraries 설치하십시오. 또는 postgres 모듈을 변경 사용해도 됩니다.

#### macOS:

```bash
  brew install libpq
  brew link --force libpq
```

#### Ubuntu:

```bash
  sudo apt-get install libpq-dev
```


