import json
import pandas as pd
from app.config import DATA_DIR


def load_transacoes() -> pd.DataFrame:
    path = DATA_DIR / "transacoes.csv"
    return pd.read_csv(path, parse_dates=["data"])


def load_perfil_investidor() -> dict:
    path = DATA_DIR / "perfil_investidor.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_produtos_financeiros() -> list[dict]:
    path = DATA_DIR / "produtos_financeiros.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_historico_atendimento() -> pd.DataFrame:
    path = DATA_DIR / "historico_atendimento.csv"
    return pd.read_csv(path, parse_dates=["data"])


def salvar_transacao(nova_transacao: dict) -> None:
    """Adiciona um novo gasto ao transacoes.csv (persistência simples para o MVP)."""
    path = DATA_DIR / "transacoes.csv"
    df = load_transacoes()
    df = pd.concat([df, pd.DataFrame([nova_transacao])], ignore_index=True)
    df.to_csv(path, index=False)
