# 🚀 FastAPI + MySQL — Users API

> API RESTful de gerenciamento de usuários construída com **FastAPI**, **SQLAlchemy** e **MySQL**, containerizada com **Docker**.

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql)](https://www.mysql.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)](https://docs.docker.com/compose/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Execução](#-instalação-e-execução)
  - [Com Docker (recomendado)](#-com-docker-recomendado)
  - [Sem Docker (local)](#-sem-docker-local)
- [Banco de Dados](#-banco-de-dados)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Referência dos Endpoints](#-referência-dos-endpoints)
- [Estrutura de Pastas](#-estrutura-de-pastas)
- [Tratamento de Erros](#-tratamento-de-erros)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

---

## 🔭 Visão Geral

Esta API fornece um CRUD completo de usuários exposto via HTTP/JSON. O projeto serve como base de referência para quem quer ver na prática como conectar **FastAPI** a um banco de dados relacional **MySQL** usando **SQLAlchemy 2.x** com tipagem moderna, validação de dados via **Pydantic v2** e toda a stack containerizada com **Docker Compose**.

**Problemas que resolve:**

- Boilerplate de API REST pronta para produção com separação clara de responsabilidades (router → repository → model)
- Setup de banco de dados com health-check, connection pooling e reconexão automática
- Ambiente reproduzível com Docker, eliminando o problema de "funciona na minha máquina"

**Público-alvo:** Desenvolvedores back-end buscando um template FastAPI+MySQL bem estruturado, ou equipes iniciando um novo serviço Python.

---

## 🛠 Pré-requisitos

### Com Docker

| Ferramenta | Versão mínima |
|------------|---------------|
| Docker     | 24+           |
| Docker Compose | v2+       |

### Sem Docker (local)

| Ferramenta | Versão mínima |
|------------|---------------|
| Python     | 3.12+         |
| MySQL      | 8.0+          |
| pip        | 23+           |

---

## 🚀 Instalação e Execução

### 🐳 Com Docker (recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/app-mysql-docker.git
cd app-mysql-docker

# 2. Suba os containers (API + MySQL)
docker compose up --build
```

A API estará disponível em `http://localhost:8000`.
O MySQL ficará acessível na porta `3306`.

Para rodar em background:

```bash
docker compose up --build -d
```

Para encerrar:

```bash
docker compose down
```

Para encerrar e remover o volume de dados:

```bash
docker compose down -v
```

---

### 💻 Sem Docker (local)

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/app-mysql-docker.git
cd app-mysql-docker

# 2. Execute o script de setup (cria venv, instala dependências e copia .env)
bash setup.sh

# 3. Ative o virtual environment
source venv/bin/activate

# 4. Edite o .env com as credenciais do seu MySQL local
nano .env

# 5. Suba a aplicação com hot-reload
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.

> ⚠️ Certifique-se de que o banco `fastapi_db` já existe no seu MySQL local antes de subir a aplicação. A criação das tabelas é feita automaticamente no startup.

---

## 🗄️ Banco de Dados

### Com Docker

Quando você sobe o projeto com `docker compose up`, o MySQL já cria o banco `fastapi_db` automaticamente — nenhuma ação manual é necessária. A variável `MYSQL_DATABASE` no `docker-compose.yml` cuida disso.

Para acessar o MySQL rodando no container:

```bash
docker exec -it mysql_db mysql -u root -pmy-secret-pw
```

### Sem Docker (local)

Crie o banco manualmente antes de subir a aplicação:

```bash
mysql -u root -p
```

```sql
CREATE DATABASE fastapi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

As tabelas são criadas automaticamente no startup da aplicação via SQLAlchemy.

---

### Verificando os dados

**Listar todos os usuários via curl:**

```bash
curl -s http://localhost:8000/api/v1/users | python3 -m json.tool
```

**Listar diretamente no MySQL** (via container):

```bash
docker exec -it mysql_db mysql -u root -pmy-secret-pw fastapi_db \
  -e "SELECT id, name, email, is_active, created_at FROM users;"
```

**Listar diretamente no MySQL** (local):

```bash
mysql -u root -p fastapi_db -e "SELECT id, name, email, is_active, created_at FROM users;"
```

---

## 🔑 Variáveis de Ambiente

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

| Variável      | Padrão      | Descrição                                 |
|---------------|-------------|-------------------------------------------|
| `DB_HOST`     | `localhost` | Host do servidor MySQL                    |
| `DB_PORT`     | `3306`      | Porta do MySQL                            |
| `DB_USER`     | `root`      | Usuário do banco de dados                 |
| `DB_PASSWORD` | `secret`    | Senha do usuário do banco                 |
| `DB_NAME`     | `fastapi_db`| Nome do banco de dados                    |

`.env.example`:

```dotenv
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=secret
DB_NAME=fastapi_db
```

> 🔒 O arquivo `.env` está no `.gitignore` e nunca deve ser comitado.

---

## 📡 Referência dos Endpoints

**Base URL:** `http://localhost:8000`

A documentação interativa (Swagger UI) está disponível em:
- **Swagger:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

### 🟢 `GET /health`

Verifica se a API está no ar.

**Headers:** nenhum

**Resposta de sucesso — `200 OK`:**

```json
{
  "status": "ok"
}
```

**Exemplo com curl:**

```bash
curl -s http://localhost:8000/health
```

---

### 🔵 `GET /api/v1/users`

Lista todos os usuários com suporte a paginação.

**Query Parameters:**

| Parâmetro | Tipo  | Padrão | Descrição                          |
|-----------|-------|--------|------------------------------------|
| `skip`    | `int` | `0`    | Número de registros a pular (≥ 0)  |
| `limit`   | `int` | `100`  | Máximo de registros retornados (1–200) |

**Exemplo de requisição:**

```http
GET /api/v1/users?skip=0&limit=10
```

**Exemplo com curl:**

```bash
curl -s "http://localhost:8000/api/v1/users?skip=0&limit=10"
```

**Resposta de sucesso — `200 OK`:**

```json
[
  {
    "id": 1,
    "name": "Maria Silva",
    "email": "maria@email.com",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
]
```

---

### 🔵 `GET /api/v1/users/{user_id}`

Retorna um único usuário pelo seu ID.

**Path Parameters:**

| Parâmetro | Tipo  | Descrição      |
|-----------|-------|----------------|
| `user_id` | `int` | ID do usuário  |

**Exemplo de requisição:**

```http
GET /api/v1/users/1
```

**Exemplo com curl:**

```bash
curl -s http://localhost:8000/api/v1/users/1
```

**Resposta de sucesso — `200 OK`:**

```json
{
  "id": 1,
  "name": "Maria Silva",
  "email": "maria@email.com",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Respostas de erro:**

| Status | Descrição                        |
|--------|----------------------------------|
| `404`  | Usuário não encontrado           |

---

### 🟡 `POST /api/v1/users`

Cria um novo usuário.

**Headers:**

```
Content-Type: application/json
```

**Request Body:**

| Campo   | Tipo     | Obrigatório | Descrição                    |
|---------|----------|-------------|------------------------------|
| `name`  | `string` | ✅           | Nome completo (não pode ser vazio) |
| `email` | `string` | ✅           | E-mail válido e único        |

**Exemplo de payload:**

```json
{
  "name": "João Souza",
  "email": "joao@email.com"
}
```

**Exemplo com curl:**

```bash
curl -s -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name": "João Souza", "email": "joao@email.com"}'
```

**Resposta de sucesso — `201 Created`:**

```json
{
  "id": 2,
  "name": "João Souza",
  "email": "joao@email.com",
  "is_active": true,
  "created_at": "2024-01-15T11:00:00",
  "updated_at": "2024-01-15T11:00:00"
}
```

**Respostas de erro:**

| Status | Descrição                              |
|--------|----------------------------------------|
| `409`  | E-mail já cadastrado                   |
| `422`  | Payload inválido (campos faltando, e-mail mal formatado, name vazio) |

---

### 🟠 `PATCH /api/v1/users/{user_id}`

Atualiza parcialmente um usuário existente. Apenas os campos enviados serão modificados.

**Path Parameters:**

| Parâmetro | Tipo  | Descrição      |
|-----------|-------|----------------|
| `user_id` | `int` | ID do usuário  |

**Headers:**

```
Content-Type: application/json
```

**Request Body (todos os campos são opcionais):**

| Campo       | Tipo      | Descrição                             |
|-------------|-----------|---------------------------------------|
| `name`      | `string`  | Novo nome (não pode ser vazio)        |
| `email`     | `string`  | Novo e-mail válido e único            |
| `is_active` | `boolean` | Status de ativação do usuário         |

**Exemplo de payload:**

```json
{
  "name": "João Souza Atualizado",
  "is_active": false
}
```

**Exemplo com curl:**

```bash
curl -s -X PATCH http://localhost:8000/api/v1/users/2 \
  -H "Content-Type: application/json" \
  -d '{"name": "João Souza Atualizado", "is_active": false}'
```

**Resposta de sucesso — `200 OK`:**

```json
{
  "id": 2,
  "name": "João Souza Atualizado",
  "email": "joao@email.com",
  "is_active": false,
  "created_at": "2024-01-15T11:00:00",
  "updated_at": "2024-01-15T11:45:00"
}
```

**Respostas de erro:**

| Status | Descrição                              |
|--------|----------------------------------------|
| `404`  | Usuário não encontrado                 |
| `409`  | Novo e-mail já pertence a outro usuário|
| `422`  | Payload inválido                       |

---

### 🔴 `DELETE /api/v1/users/{user_id}`

Remove permanentemente um usuário.

**Path Parameters:**

| Parâmetro | Tipo  | Descrição      |
|-----------|-------|----------------|
| `user_id` | `int` | ID do usuário  |

**Exemplo de requisição:**

```http
DELETE /api/v1/users/2
```

**Exemplo com curl:**

```bash
curl -s -X DELETE http://localhost:8000/api/v1/users/2 -w "%{http_code}"
```

**Resposta de sucesso — `204 No Content`** *(sem corpo na resposta)*

**Respostas de erro:**

| Status | Descrição              |
|--------|------------------------|
| `404`  | Usuário não encontrado |

---

## 📁 Estrutura de Pastas

```
app-mysql-docker/
├── app/
│   ├── main.py             # Entrypoint da aplicação FastAPI
│   ├── config.py           # Configurações via variáveis de ambiente (Pydantic Settings)
│   ├── database.py         # Engine, Session e Base do SQLAlchemy
│   ├── models/
│   │   └── user.py         # Modelo ORM da tabela `users`
│   ├── schemas/
│   │   └── user.py         # Schemas Pydantic (request/response)
│   ├── repositories/
│   │   └── user.py         # Camada de acesso a dados (queries)
│   └── routers/
│       └── users.py        # Rotas HTTP e handlers
├── .env                    # Variáveis de ambiente (não commitado)
├── .env.example            # Template de variáveis de ambiente
├── .gitignore
├── docker-compose.yml      # Orquestração API + MySQL
├── Dockerfile              # Imagem da aplicação
├── requirements.txt        # Dependências Python
└── setup.sh                # Script de setup para desenvolvimento local
```

---

## ⚠️ Tratamento de Erros

Todos os erros seguem o formato padrão do FastAPI:

```json
{
  "detail": "Mensagem descritiva do erro"
}
```

| Status Code | Significado                                                     |
|-------------|-----------------------------------------------------------------|
| `200 OK`         | Requisição bem-sucedida                                    |
| `201 Created`    | Recurso criado com sucesso                                 |
| `204 No Content` | Recurso removido com sucesso (sem corpo na resposta)       |
| `404 Not Found`  | Recurso não encontrado                                     |
| `409 Conflict`   | Conflito de dados (ex: e-mail duplicado)                   |
| `422 Unprocessable Entity` | Payload inválido ou campos com formato incorreto |
| `500 Internal Server Error` | Erro inesperado no servidor                     |

---

## 🤝 Contribuição

Contribuições são bem-vindas! Siga os passos abaixo:

1. Faça um **fork** do repositório
2. Crie uma branch para sua feature ou correção:
   ```bash
   git checkout -b feat/minha-feature
   ```
3. Faça seus commits com mensagens claras seguindo [Conventional Commits](https://www.conventionalcommits.org/):
   ```bash
   git commit -m "feat: adiciona endpoint de busca por nome"
   ```
4. Envie para o seu fork:
   ```bash
   git push origin feat/minha-feature
   ```
5. Abra um **Pull Request** descrevendo as mudanças realizadas

### 📌 Boas práticas

- Mantenha a cobertura de testes (use `pytest`)
- Siga o padrão de arquitetura router → repository → model
- Para migrações de banco em produção, utilize **Alembic** (já incluso no `requirements.txt`)

---

## 📄 Licença

Distribuído sob a licença **MIT**. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<p align="center">Feito com ❤️ usando <a href="https://fastapi.tiangolo.com/">FastAPI</a></p>
