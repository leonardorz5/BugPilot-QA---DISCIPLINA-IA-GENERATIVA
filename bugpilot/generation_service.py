from typing import Protocol

from bugpilot.models import BugTriage, SuiteTestes


class TestGeneratorLLM(Protocol):

    def gerar_casos_teste(
        self,
        triagem: BugTriage,
    ) -> SuiteTestes:
        ...


class CaseGenerationService:

    CAMPOS_OBRIGATORIOS = (
        "titulo",
        "resumo",
        "comportamento_esperado",
        "comportamento_atual",
    )

    def __init__(
        self,
        llm: TestGeneratorLLM,
    ) -> None:
        self.llm = llm

    def gerar(
        self,
        triagem: BugTriage,
    ) -> SuiteTestes:

        campos_ausentes = []

        for campo in self.CAMPOS_OBRIGATORIOS:

            valor = getattr(triagem, campo)

            if (
                valor is None
                or (
                    isinstance(valor, str)
                    and not valor.strip()
                )
            ):
                campos_ausentes.append(campo)

        if campos_ausentes:

            nomes = ", ".join(campos_ausentes)

            raise ValueError(
                "Não é possível gerar casos de teste. "
                f"Campos obrigatórios ausentes: {nomes}."
            )

        return self.llm.gerar_casos_teste(
            triagem
        )