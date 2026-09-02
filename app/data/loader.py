import json
from datetime import date

import pandas as pd
from app.config import DATA_DIR

_cache = {"transacoes": None, "perfil": None, "produtos": None, "historico": None}


def _invalidar(keys):
    for key in keys:
        _cache[key] = None


def _normalizar_datas(df: pd.DataFrame, col: str = "data") -> pd.DataFrame:
    df = df.copy()
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def load_transacoes() -> pd.DataFrame:
    if _cache["transacoes"] is not None:
        return _cache["transacoes"]
    path = DATA_DIR / "transacoes.csv"
    if not path.exists():
        df = pd.DataFrame(columns=["data", "categoria", "valor", "descricao"])
    else:
        df = pd.read_csv(path)
    df = _normalizar_datas(df)
    _cache["transacoes"] = df
    return df


def load_perfil_investidor() -> dict:
    if _cache["perfil"] is not None:
        return _cache["perfil"]
    path = DATA_DIR / "perfil_investidor.json"
    if not path.exists():
        _cache["perfil"] = {}
        return _cache["perfil"]
    with open(path, encoding="utf-8") as f:
        _cache["perfil"] = json.load(f)
    return _cache["perfil"]


def load_produtos_financeiros() -> list[dict]:
    if _cache["produtos"] is not None:
        return _cache["produtos"]
    path = DATA_DIR / "produtos_financeiros.json"
    if not path.exists():
        _cache["produtos"] = []
        return _cache["produtos"]
    with open(path, encoding="utf-8") as f:
        _cache["produtos"] = json.load(f)
    return _cache["produtos"]


def load_historico_atendimento() -> pd.DataFrame:
    if _cache["historico"] is not None:
        return _cache["historico"]
    path = DATA_DIR / "historico_atendimento.csv"
    if not path.exists():
        df = pd.DataFrame(columns=["data", "pergunta", "resposta"])
    else:
        df = pd.read_csv(path, parse_dates=["data"])
    _cache["historico"] = df
    return df


def _formatar_para_csv(df: pd.DataFrame, col: str = "data") -> pd.DataFrame:
    df = df.copy()
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%d")
    return df


def salvar_transacao(nova_transacao: dict) -> None:
    path = DATA_DIR / "transacoes.csv"
    df = load_transacoes()
    novo_df = pd.DataFrame([nova_transacao])
    novo_df = _normalizar_datas(novo_df)
    df = pd.concat([df, novo_df], ignore_index=True)
    _formatar_para_csv(df).to_csv(path, index=False)
    _invalidar(["transacoes"])


def salvar_conversa(pergunta: str, resposta: str) -> None:
    path = DATA_DIR / "historico_atendimento.csv"
    df = load_historico_atendimento()
    nova = pd.DataFrame(
        [{"data": date.today().isoformat(), "pergunta": pergunta, "resposta": resposta}]
    )
    df = pd.concat([df, nova], ignore_index=True)
    df.to_csv(path, index=False)
    _invalidar(["historico"])


def importar_transacoes(registros: list[dict]) -> int:
    path = DATA_DIR / "transacoes.csv"
    df = load_transacoes()
    df_novo = _normalizar_datas(pd.DataFrame(registros))
    if not df_novo.empty:
        df = pd.concat([df, df_novo], ignore_index=True)
        _formatar_para_csv(df).to_csv(path, index=False)
    _invalidar(["transacoes"])
    return len(registros)
