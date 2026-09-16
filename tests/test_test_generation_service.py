from unittest.mock import Mock

import pytest

from bugpilot.models import (
    BugTriage,
    CasoTeste,
    Severidade,
    SuiteTestes,
    TipoTeste,
)
from bugpilot.generation_service import (
    CaseGenerationService,
)


def criar_triagem(
    comportamento_esperado=(
        "O novo nome deve permanecer salvo."
    ),
    comportamento_atual=(
        "O nome anterior retorna após atualizar a página."
    ),
):
    return BugTriage(
        titulo="Nome alterado não persiste",
        resumo=(
            "A alteração aparenta sucesso, "
            "mas é perdida após atualizar a página."
        ),
        passos_reproducao=[
            "Editar o nome.",
            "Salvar.",
            "Atualizar a página.",
        ],
        comportamento_esperado=comportamento_esperado,
        comportamento_atual=comportamento_atual,
        ambiente=None,
        frequencia=None,
        campos_ausentes=[],
        severidade_sugerida=Severidade.MEDIA,
        justificativa_severidade=(
            "A alteração não permanece salva."
        ),
    )


def criar_suite():
    return SuiteTestes(
        casos=[
            CasoTeste(
                id="TC01",
                titulo="Salvar alteração válida",
                objetivo="Validar a persistência do nome.",
                tipo=TipoTeste.POSITIVO,
                pre_condicoes=["Usuário existente."],
                passos=[
                    "Editar o nome.",
                    "Salvar.",
                    "Atualizar a página.",
                ],
                resultado_esperado=(
                    "O novo nome permanece salvo."
                ),
            ),
            CasoTeste(
                id="TC02",
                titulo="Validar atualização da página",
                objetivo=(
                    "Confirmar a persistência após reload."
                ),
                tipo=TipoTeste.REGRESSAO,
                pre_condicoes=["Nome alterado e salvo."],
                passos=[
                    "Atualizar a página."
                ],
                resultado_esperado=(
                    "O nome atualizado continua visível."
                ),
            ),
            CasoTeste(
                id="TC03",
                titulo="Validar entrada inválida",
                objetivo=(
                    "Verificar tratamento de nome inválido."
                ),
                tipo=TipoTeste.NEGATIVO,
                pre_condicoes=["Usuário existente."],
                passos=[
                    "Informar um nome inválido.",
                    "Tentar salvar.",
                ],
                resultado_esperado=(
                    "A alteração inválida não é persistida."
                ),
            ),
        ]
    )


def test_gera_casos_quando_triagem_e_valida():

    llm = Mock()

    suite = criar_suite()

    llm.gerar_casos_teste.return_value = suite

    service = CaseGenerationService(llm)

    triagem = criar_triagem()

    resultado = service.gerar(triagem)

    assert resultado == suite

    llm.gerar_casos_teste.assert_called_once_with(
        triagem
    )


@pytest.mark.parametrize(
    "valor_invalido",
    [
        None,
        "",
        "   ",
    ],
)
def test_rejeita_comportamento_esperado_invalido(
    valor_invalido,
):

    llm = Mock()

    service = CaseGenerationService(llm)

    triagem = criar_triagem(
        comportamento_esperado=valor_invalido
    )

    with pytest.raises(
        ValueError,
        match="comportamento_esperado",
    ):
        service.gerar(triagem)

    llm.gerar_casos_teste.assert_not_called()


@pytest.mark.parametrize(
    "valor_invalido",
    [
        None,
        "",
        "   ",
    ],
)
def test_rejeita_comportamento_atual_invalido(
    valor_invalido,
):

    llm = Mock()

    service = CaseGenerationService(llm)

    triagem = criar_triagem(
        comportamento_atual=valor_invalido
    )

    with pytest.raises(
        ValueError,
        match="comportamento_atual",
    ):
        service.gerar(triagem)

    llm.gerar_casos_teste.assert_not_called()
    
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