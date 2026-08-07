# FastAPI + MySQL 1

API REST construída com FastAPI e MySQL, com virtual environment isolado.

## Estrutura

```
.
├── app/
│   ├── main.py           # Ponto de entrada da aplicação
│   ├── config.py         # Configurações via variáveis de ambiente
│   ├── database.py       # Engine e sessão do SQLAlchemy
│   ├── models/           # Modelos ORM (tabelas)
│   │   └── user.py
│   ├── schemas/          # Schemas Pydantic (validação / serialização)
│   │   └── user.py
│   ├── repositories/     # Camada de acesso ao banco
│   │   └── user.py
│   └── routers/          # Rotas da API
│       └── users.py
├── .env.example
├── requirements.txt
└── setup.sh
```

## Setup rápido

```bash
chmod +x setup.sh
./setup.sh
```

Ou manualmente:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edite as credenciais
```

## Variáveis de ambiente

| Variável      | Padrão       | Descrição              |
|---------------|--------------|------------------------|
| `DB_HOST`     | `localhost`  | Host do MySQL          |
| `DB_PORT`     | `3306`       | Porta do MySQL         |
| `DB_USER`     | `root`       | Usuário do MySQL       |
| `DB_PASSWORD` | `secret`     | Senha do MySQL         |
| `DB_NAME`     | `fastapi_db` | Nome do banco de dados |

## Rodando a API

```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

A API ficará disponível em `http://localhost:8000`.  
Documentação interativa: `http://localhost:8000/docs`

## Endpoints

| Método   | Rota                  | Descrição             |
|----------|-----------------------|-----------------------|
| `GET`    | `/health`             | Health check          |
| `GET`    | `/api/v1/users`       | Listar usuários       |
| `GET`    | `/api/v1/users/{id}`  | Buscar usuário por ID |
| `POST`   | `/api/v1/users`       | Criar usuário         |
| `PATCH`  | `/api/v1/users/{id}`  | Atualizar usuário     |
| `DELETE` | `/api/v1/users/{id}`  | Remover usuário       |
