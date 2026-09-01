# Como rodar o backend do Jarbas

## 1. Instalar dependências
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Configurar variáveis de ambiente
```bash
cp .env.example .env
# edite .env e coloque sua OPENAI_API_KEY
```

## 3. Trocar os dados de exemplo pelos dados reais
Os arquivos em `data/` são **placeholders** com a mesma estrutura descrita na
Base de Conhecimento. Substitua pelo `historico_atendimento.csv`,
`perfil_investidor.json`, `produtos_financeiros.json` e `transacoes.csv`
reais do desafio — mantendo os mesmos nomes de coluna/chave, ou ajustando
`app/data/loader.py` e `app/services/context.py` se os nomes forem diferentes.

## 4. Rodar o servidor
```bash
uvicorn app.main:app --reload
```
A API sobe em `http://localhost:8000`. Docs interativas em `http://localhost:8000/docs`.

## 5. Testar as rotas
- `POST /gastos` — cadastra um gasto manual
- `GET /resumo?periodo=dia` ou `?periodo=semana` — resumo de gastos
- `GET /alertas` — alertas de limite por categoria (ajuste os limites em `.env`)
- `POST /chat` — pergunta em linguagem natural pro Jarbas, ex: `{"pergunta": "quanto gastei essa semana?"}`

## O que ainda falta pra virar produto de verdade
- Trocar a persistência em CSV por um banco de verdade (SQLite/Postgres) — só mexe em `app/data/loader.py`, o resto do código não muda (separação de responsabilidades)
- Frontend (React) consumindo essas rotas
- Autenticação, caso vire multiusuário
