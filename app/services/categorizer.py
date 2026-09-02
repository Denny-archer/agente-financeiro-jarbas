KEYWORDS_POR_CATEGORIA = {
    "Alimentacao": [
        "ifood", "rappi", "uber eats", "restaurante", "lanchonete",
        "mercado", "supermercado", "padaria", "pizza", "delivery", "comida",
    ],
    "Streaming": [
        "netflix", "spotify", "disney", "hbomax", "hbo max", "prime video",
        "paramount", "youtube premium", "apple tv", "streaming",
    ],
    "Transporte": [
        "uber", "99", "99pop", "combustivel", "posto", "gasolina",
        "etanol", "passagem", "onibus", "metro", "pedagio", "lyft",
    ],
    "Saude": [
        "academia", "farmacia", "drogaria", "hospital", "clinica",
        "dentista", "medico", "plano de saude", "plano saude", "consultas",
    ],
    "Investimento": [
        "fii", "fundo", "acao", "acoes", "renda fixa", "cdb", "lci",
        "lca", "tesouro", "investimento", "aporte", "corretora", "etf",
    ],
    "Moradia": [
        "aluguel", "condominio", "conta de luz", "conta de agua",
        "internet", "luz", "agua", "iptu", "gás", "gas",
    ],
    "Entretenimento": [
        "cinema", "show", "balada", "jogo", "games", "teatro", "parque",
        "stream", "evento",
    ],
    "Educacao": [
        "faculdade", "curso", "escola", "mensalidade", "livro", "ebook",
        "cursos", "universidade",
    ],
}

DEFAULT_CATEGORIA = "Outros"


def categorizar(descricao: str) -> str:
    texto = (descricao or "").lower()
    for categoria, keywords in KEYWORDS_POR_CATEGORIA.items():
        for kw in keywords:
            if kw in texto:
                return categoria
    return DEFAULT_CATEGORIA
