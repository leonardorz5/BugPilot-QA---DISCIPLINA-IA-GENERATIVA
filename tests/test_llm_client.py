from unittest.mock import Mock

import pytest

from bugpilot.llm_client import GeminiClient
from bugpilot.models import (
    BugTriage,
    CasoTeste,
    Severidade,
    SuiteTestes,
    TipoTeste,
)


def criar_cliente_mockado():
    client = object.__new__(GeminiClient)

    client.client = Mock()
    client.model = "gemini-3.6-flash"

    return client


def criar_triagem():
    return BugTriage(
        titulo="Nome não persiste",
        resumo="O nome antigo retorna após atualizar a página.",
        passos_reproducao=[
            "Editar o nome.",
            "Salvar.",
            "Atualizar a página.",
        ],
        comportamento_esperado=(
            "O novo nome deve permanecer exibido."
        ),
        comportamento_atual=(
            "O nome anterior volta a ser exibido."
        ),
        ambiente=None,
        frequencia=None,
        campos_ausentes=[
            "ambiente",
            "frequencia",
        ],
        severidade_sugerida=Severidade.ALTA,
        justificativa_severidade=(
            "A alteração não é persistida."
        ),
    )


def criar_suite():
    return SuiteTestes(
        casos=[
            CasoTeste(
                id="TC01",
                titulo="Validar persistência do nome",
                objetivo=(
                    "Verificar se o novo nome permanece salvo."
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
            "Não há informações suficientes "
            "para outros cenários."
        ),
    )


def test_analisar_bug_retorna_resposta_estruturada():

    client = criar_cliente_mockado()

    triagem = criar_triagem()

    response = Mock()
    response.parsed = triagem

    client.client.models.generate_content.return_value = (
        response
    )

    resultado = client.analisar_bug(
        "Ao editar o nome, a alteração não persiste."
    )

    assert resultado == triagem

    chamada = (
        client.client.models.generate_content
        .call_args
    )

    assert chamada.kwargs["model"] == (
        "gemini-3.6-flash"
    )

    assert (
        chamada.kwargs["config"]["response_schema"]
        is BugTriage
    )


def test_gerar_casos_retorna_suite_estruturada():

    client = criar_cliente_mockado()

    triagem = criar_triagem()
    suite = criar_suite()

    response = Mock()
    response.parsed = suite

    client.client.models.generate_content.return_value = (
        response
    )

    resultado = client.gerar_casos_teste(
        triagem
    )

    assert resultado == suite

    chamada = (
        client.client.models.generate_content
        .call_args
    )

    assert chamada.kwargs["model"] == (
        "gemini-3.6-flash"
    )

    assert (
        chamada.kwargs["config"]["response_schema"]
        is SuiteTestes
    )


def test_analisar_bug_falha_quando_resposta_nao_e_parseada():

    client = criar_cliente_mockado()

    response = Mock()
    response.parsed = None

    client.client.models.generate_content.return_value = (
        response
    )

    with pytest.raises(
        RuntimeError,
        match="não retornou uma resposta válida",
    ):
        client.analisar_bug(
            "Relato suficientemente detalhado do bug."
        )