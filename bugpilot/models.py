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


class TipoTeste(str, Enum):
    POSITIVO = "Positivo"
    NEGATIVO = "Negativo"
    BORDA = "Borda"
    REGRESSAO = "Regressão"


class CasoTeste(BaseModel):
    id: str = Field(
        description="Identificador do caso de teste, por exemplo TC01."
    )

    titulo: str

    objetivo: str

    tipo: TipoTeste

    pre_condicoes: list[str]

    passos: list[str]

    resultado_esperado: str


class SuiteTestes(BaseModel):
    casos: list[CasoTeste] = Field(
        min_length=1,
        description=(
            "Conjunto de casos de teste sustentados pelas informações "
            "disponíveis na triagem."
        )
    )

    observacoes: str | None = None
    
def test_suite_aceita_um_caso_quando_dados_sao_limitados():

    suite = SuiteTestes(
        casos=[
            CasoTeste(
                id="TC01",
                titulo="Validar persistência do nome",
                objetivo=(
                    "Verificar se o novo nome permanece "
                    "após atualizar a página."
                ),
                tipo=TipoTeste.POSITIVO,
                pre_condicoes=[],
                passos=[
                    "Editar o nome.",
                    "Salvar.",
                    "Atualizar a página.",
                ],
                resultado_esperado=(
                    "O novo nome permanece exibido."
                ),
            )
        ],
        observacoes=(
            "A triagem não possui informações suficientes "
            "para gerar outros cenários confiáveis."
        ),
    )

    assert len(suite.casos) == 1