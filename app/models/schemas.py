from datetime import date
from pydantic import BaseModel, Field, field_validator


class GastoIn(BaseModel):
    data: date
    categoria: str | None = None
    valor: float = Field(gt=0)
    descricao: str = ""

    @field_validator("categoria")
    @classmethod
    def normalizar_categoria(cls, v: str | None) -> str | None:
        if v is None:
            return None
        return v.strip().title()


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


class ImportacaoOut(BaseModel):
    total: int
    importados: int
    erros: list[dict]
