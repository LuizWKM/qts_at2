# Biblioteca Viva — AT2

Sistema FastAPI de gerenciamento de livros, com interface em `http://localhost:3000`.

## Executar

```powershell
uv sync
uv run uvicorn app.main:app --host 0.0.0.0 --port 3000
```

## Testes

```powershell
uv run pytest -m integration
uv run pytest -m "e2e or accessibility" --base-url http://127.0.0.1:3000
```

O E2E e a auditoria usam Playwright, Page Object Model, seletores semânticos, Axe-core e navegação por teclado.

## Carga

Com o servidor em execução:

```powershell
uv run locust -f locustfile.py --host http://127.0.0.1:3000
```

Registre no relatório da execução o RPS, o p95 e a taxa de falhas exibidos pelo Locust. Como referência de aceite, use taxa de falhas `0%` e p95 inferior a `500 ms` em uma execução local com 10 usuários.

## Rotas

- `GET /livros`
- `POST /livros`
- `PATCH /livros/{id}`
- `DELETE /livros/{id}`

Consulte [PRD.md](PRD.md) e [AI_USAGE.md](AI_USAGE.md) para os requisitos e a transparência de uso de IA.
