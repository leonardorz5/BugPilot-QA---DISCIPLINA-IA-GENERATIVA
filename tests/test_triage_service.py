from unittest.mock import Mock

import pytest

from bugpilot.triage_service import TriageService


def test_rejeita_relato_vazio():

    llm = Mock()

    service = TriageService(llm)

    with pytest.raises(
        ValueError,
        match="não pode estar vazio"
    ):
        service.analisar("")

    llm.analisar_bug.assert_not_called()


def test_rejeita_relato_muito_curto():

    llm = Mock()

    service = TriageService(llm)

    with pytest.raises(
        ValueError,
        match="pelo menos 20 caracteres"
    ):
        service.analisar("Erro ao salvar")

    llm.analisar_bug.assert_not_called()


def test_envia_relato_valido_para_llm():

    llm = Mock()

    service = TriageService(llm)

    relato = (
        "Ao editar o usuário, "
        "o novo nome não permanece salvo."
    )

    service.analisar(relato)

    llm.analisar_bug.assert_called_once_with(
        relato
    )