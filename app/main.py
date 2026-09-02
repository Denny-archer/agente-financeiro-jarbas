from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS
from app.models.schemas import (
    GastoIn,
    ChatIn,
    ChatOut,
    ResumoOut,
    AlertaOut,
    ImportacaoOut,
)
from app.data.loader import (
    load_transacoes,
    load_perfil_investidor,
    load_produtos_financeiros,
    load_historico_atendimento,
    salvar_transacao,
    salvar_conversa,
    importar_transacoes,
)
from app.services.summary import gerar_resumo
from app.services.alerts import verificar_alertas
from app.services.context import montar_contexto
from app.services.agent import perguntar_ao_agente, AgenteError
from app.services.categorizer import categorizar

app = FastAPI(title="Jarbas - Agente Financeiro")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/gastos", status_code=201)
def cadastrar_gasto(gasto: GastoIn):
    dados = gasto.model_dump()
    if not dados.get("categoria"):
        dados["categoria"] = categorizar(dados["descricao"])
    salvar_transacao(dados)
    return {"mensagem": "Gasto registrado com sucesso.", "categoria": dados["categoria"]}


@app.get("/resumo", response_model=ResumoOut)
def obter_resumo(periodo: str = "dia"):
    if periodo not in ("dia", "semana"):
        raise HTTPException(400, "periodo deve ser 'dia' ou 'semana'")
    transacoes = load_transacoes()
    return gerar_resumo(transacoes, periodo)


@app.get("/alertas", response_model=list[AlertaOut])
def obter_alertas():
    transacoes = load_transacoes()
    return verificar_alertas(transacoes)


@app.post("/chat", response_model=ChatOut)
def conversar(chat: ChatIn):
    transacoes = load_transacoes()
    perfil = load_perfil_investidor()
    produtos = load_produtos_financeiros()
    historico = load_historico_atendimento()

    contexto = montar_contexto(chat.pergunta, perfil, transacoes, produtos, historico)

    try:
        resposta = perguntar_ao_agente(chat.pergunta, contexto)
    except AgenteError as exc:
        raise HTTPException(502, str(exc)) from exc

    salvar_conversa(chat.pergunta, resposta)
    return ChatOut(resposta=resposta)


@app.post("/importar", response_model=ImportacaoOut)
def importar_csv(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(400, "Apenas arquivos .csv são aceitos.")

    import io

    import pandas as pd

    conteudo = file.file.read().decode("utf-8")
    try:
        df = pd.read_csv(io.StringIO(conteudo))
    except Exception as exc:
        raise HTTPException(400, f"Arquivo CSV inválido: {exc}") from exc

    colunas_necessarias = {"data", "valor"}
    if not colunas_necessarias.issubset(df.columns):
        raise HTTPException(
            400,
            "CSV deve conter as colunas 'data' e 'valor' (opcional: 'categoria', 'descricao').",
        )

    df["descricao"] = df.get("descricao", "").fillna("")

    registros = []
    erros = []
    for idx, row in df.iterrows():
        try:
            linha = {
                "data": pd.Timestamp(row["data"]).date().isoformat(),
                "valor": float(row["valor"]),
            }
            categoria = row.get("categoria")
            if isinstance(categoria, str) and categoria.strip():
                linha["categoria"] = categoria.strip().title()
            else:
                linha["categoria"] = categorizar(str(row["descricao"]))
            linha["descricao"] = str(row["descricao"]) if row["descricao"] else ""
            registros.append(linha)
        except Exception as exc:
            erros.append({"linha": idx + 2, "erro": str(exc)})

    if registros:
        importar_transacoes(registros)

    return ImportacaoOut(
        total=len(df), importados=len(registros), erros=erros
    )
