from datetime import date
from pydantic import BaseModel, Field


class GastoIn(BaseModel):
    data: date
    categoria: str
    valor: float = Field(gt=0)
    descricao: str = ""


class ChatIn(BaseModel):
    pergunta: str


class ChatOut(BaseModel):
    resposta: str


class ResumoOut(BaseModel):
    periodo: str
    total: float
    por_categoria: dict[str, float]


class AlertaOut(BaseModel):
    categoria: str
    gasto_atual: float
    limite: float
    mensagem: str
