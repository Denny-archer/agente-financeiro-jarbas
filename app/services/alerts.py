import pandas as pd
from app.config import LIMITES_POR_CATEGORIA


def verificar_alertas(transacoes: pd.DataFrame) -> list[dict]:
    """Compara o gasto do mês corrente por categoria com os limites configurados."""
    hoje = pd.Timestamp.now()
    mes_atual = transacoes[
        (transacoes["data"].dt.month == hoje.month) & (transacoes["data"].dt.year == hoje.year)
    ]
    gasto_por_categoria = mes_atual.groupby("categoria")["valor"].sum()

    alertas = []
    for categoria, limite in LIMITES_POR_CATEGORIA.items():
        gasto_atual = float(gasto_por_categoria.get(categoria, 0))
        if gasto_atual > limite:
            alertas.append({
                "categoria": categoria,
                "gasto_atual": round(gasto_atual, 2),
                "limite": limite,
                "mensagem": f"Você já passou do limite em {categoria}: R$ {gasto_atual:.2f} de R$ {limite:.2f}.",
            })
    return alertas
