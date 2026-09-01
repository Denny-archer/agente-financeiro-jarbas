from fastapi import FastAPI, HTTPException

from app.models.schemas import GastoIn, ChatIn, ChatOut, ResumoOut, AlertaOut
from app.data.loader import (
    load_transacoes,
    load_perfil_investidor,
    load_produtos_financeiros,
    salvar_transacao,
)
from app.services.summary import gerar_resumo
from app.services.alerts import verificar_alertas
from app.services.context import montar_contexto
from app.services.agent import perguntar_ao_agente

app = FastAPI(title="Jarbas - Agente Financeiro")


@app.post("/gastos", status_code=201)
def cadastrar_gasto(gasto: GastoIn):
    salvar_transacao(gasto.model_dump())
    return {"mensagem": "Gasto registrado com sucesso."}


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

    contexto = montar_contexto(chat.pergunta, perfil, transacoes, produtos)
    resposta = perguntar_ao_agente(chat.pergunta, contexto)
    return ChatOut(resposta=resposta)
