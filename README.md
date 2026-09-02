# Jarbas — Agente Financeiro 💸

Jarbas é um agente financeiro conversacional que ajuda o usuário a entender e organizar os próprios gastos. Ele processa transações (cadastradas manualmente ou importadas via CSV) e responde dúvidas em linguagem natural, sempre com base **apenas** nos dados disponíveis — sem inventar informações.

## Funcionalidades

- **Cadastro manual de gastos** (`POST /gastos`) com categorização automática simples a partir da descrição
- **Importação de extrato CSV** (`POST /importar`) em lote
- **Resumo diário/semanal** de gastos por categoria (`GET /resumo`)
- **Alertas** de limite de gasto por categoria (`GET /alertas`)
- **Chat conversacional** (`POST /chat`) com contexto de perfil, transações, produtos financeiros e histórico de atendimento

## Arquitetura

```
Cliente → Frontend (React) → FastAPI API → OpenAI (GPT) ← Base de Dados (CSV)
```

O projeto segue separação de responsabilidades:
- `app/models/` — schemas Pydantic
- `app/data/` — carregamento/persistência dos dados (CSV/JSON)
- `app/services/` — lógica de negócio (resumo, alertas, contexto, agente LLM, categorização)
- `app/prompts/` — system prompt do agente

## Como rodar (backend)

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env       # edite e coloque sua OPENAI_API_KEY
uvicorn app.main:app --reload
```

A API sobe em `http://localhost:8000`. Docs interativas em `http://localhost:8000/docs`.

## Como rodar (frontend)

```bash
cd frontend
npm install
npm run dev
```

O frontend sobe em `http://localhost:5173` (proxy configurado para a API em `:8000`).

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/gastos` | Cadastra um gasto (categoria opcional — é inferida automaticamente) |
| GET | `/resumo?periodo=dia\|semana` | Resumo de gastos por período |
| GET | `/alertas` | Alertas de limite por categoria |
| POST | `/chat` | Pergunta em linguagem natural, ex: `{"pergunta": "quanto gastei essa semana?"}` |
| POST | `/importar` | Upload de arquivo CSV com colunas `data`, `valor` (e opcionais `categoria`, `descricao`) |

## Variáveis de ambiente

| Variável | Descrição | Default |
|----------|-----------|---------|
| `OPENAI_API_KEY` | Chave da API da OpenAI | — (obrigatória) |
| `LIMITE_SUPERMERCADO` | Limite de alerta p/ categoria Supermercado | `500` |
| `LIMITE_STREAMING` | Limite de alerta p/ categoria Streaming | `100` |
| `CORS_ORIGINS` | Origens permitidas (separadas por vírgula) | `*` |

## Estrutura de dados

Os arquivos em `data/` são placeholders com a estrutura de exemplo:
- `transacoes.csv` — transações (data, categoria, valor, descricao)
- `historico_atendimento.csv` — conversas passadas (contexto de continuidade no chat)
- `perfil_investidor.json` — perfil do cliente
- `produtos_financeiros.json` — produtos financeiros disponíveis
