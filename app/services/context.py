import pandas as pd


def montar_contexto(pergunta: str, perfil: dict, transacoes: pd.DataFrame, produtos: list[dict]) -> str:
    """
    Seleciona apenas o recorte relevante da base de conhecimento para a pergunta,
    em vez de injetar tudo no prompt (reduz alucinação e mantém o contexto enxuto).
    """
    ultimas_transacoes = transacoes.sort_values("data", ascending=False).head(10)
    transacoes_texto = "\n".join(
        f"- {row['data'].date()}: {row['categoria']} - R$ {row['valor']:.2f}"
        for _, row in ultimas_transacoes.iterrows()
    )

    produtos_relevantes = [
        p for p in produtos if p["nome"].lower() in pergunta.lower()
    ] or produtos  # se nada bater, inclui todos (lista costuma ser pequena no MVP)

    produtos_texto = "\n".join(f"- {p['nome']}: {p['descricao']}" for p in produtos_relevantes)

    return f"""
Perfil do Cliente:
- Nome: {perfil.get('nome')}
- Perfil de investidor: {perfil.get('perfil')}
- Saldo disponível: R$ {perfil.get('saldo_disponivel'):.2f}

Últimas transações:
{transacoes_texto}

Produtos financeiros relevantes:
{produtos_texto}
""".strip()
