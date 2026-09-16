from enum import Enum

from pydantic import BaseModel, Field


class Severidade(str, Enum):
    BAIXA = "Baixa"
    MEDIA = "Média"
    ALTA = "Alta"
    CRITICA = "Crítica"


class BugTriage(BaseModel):
    titulo: str = Field(
        description="Título curto e objetivo para o bug."
    )

    resumo: str = Field(
        description="Resumo factual do problema."
    )

    passos_reproducao: list[str] = Field(
        default_factory=list,
        description="Passos identificados no relato."
    )

    comportamento_esperado: str | None = None

    comportamento_atual: str | None = None

    ambiente: str | None = None

    frequencia: str | None = None

    campos_ausentes: list[str] = Field(
        default_factory=list
    )

    severidade_sugerida: Severidade

    justificativa_severidade: str