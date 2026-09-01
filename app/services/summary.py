import pandas as pd
from datetime import datetime, timedelta


def gerar_resumo(transacoes: pd.DataFrame, periodo: str = "dia") -> dict:
    """Gera um resumo de gastos para 'dia' (hoje) ou 'semana' (últimos 7 dias)."""
    hoje = pd.Timestamp(datetime.now().date())

    if periodo == "dia":
        filtro = transacoes["data"] == hoje
    elif periodo == "semana":
        inicio = hoje - timedelta(days=7)
        filtro = (transacoes["data"] >= inicio) & (transacoes["data"] <= hoje)
    else:
        raise ValueError("periodo deve ser 'dia' ou 'semana'")

    recorte = transacoes.loc[filtro]
    total = float(recorte["valor"].sum())
    por_categoria = recorte.groupby("categoria")["valor"].sum().round(2).to_dict()

    return {"periodo": periodo, "total": round(total, 2), "por_categoria": por_categoria}
