# API de tarefas com FastAPI e SQLite

API REST para criar, listar, buscar, atualizar e remover tarefas. Os dados são guardados em um banco SQLite, então continuam existindo entre as execuções do servidor.

## Rotas

| Método | Rota | Função |
|---|---|---|
| GET | `/tarefas` | Lista todas as tarefas |
| GET | `/tarefas/{id}` | Busca uma tarefa pelo id |
| POST | `/tarefas` | Cria uma tarefa |
| PUT | `/tarefas/{id}` | Atualiza uma tarefa |
| DELETE | `/tarefas/{id}` | Remove uma tarefa |

Quando o id não existe, a API responde com erro **404**.

## Tecnologias
- Python
- FastAPI
- Pydantic (validação dos dados recebidos)
- SQLite (banco de dados, já incluído no Python)

## Como rodar

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

Depois, abra http://127.0.0.1:8000/docs para testar as rotas.

## Exemplo

Criar uma tarefa:

```json
{
  "titulo": "Estudar SQLite"
}
```

A resposta traz o `id` gerado pelo banco:

```json
{
  "id": 1,
  "titulo": "Estudar SQLite",
  "concluida": false
}
```
