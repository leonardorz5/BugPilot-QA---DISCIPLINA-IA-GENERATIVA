import logging

import streamlit as st
from dotenv import load_dotenv

from bugpilot.generation_service import CaseGenerationService
from bugpilot.llm_client import GeminiClient
from bugpilot.triage_service import TriageService


load_dotenv()

logger = logging.getLogger(__name__)


st.set_page_config(
    page_title="BugPilot QA",
    page_icon="🐞",
)


st.title("🐞 BugPilot QA")

st.write(
    "Assistente de triagem de bugs e geração de casos de teste com IA generativa."
)


# Mantém os resultados entre as execuções do Streamlit
if "triagem" not in st.session_state:
    st.session_state.triagem = None

if "suite_testes" not in st.session_state:
    st.session_state.suite_testes = None


relato = st.text_area(
    "Descreva o bug:",
    height=200,
    placeholder=(
        "Ex.: Ao editar o nome de um usuário, "
        "o sistema informa que a alteração foi salva, "
        "mas depois de atualizar a página o nome anterior volta."
    ),
)


if st.button("Analisar bug"):

    try:

        client = GeminiClient()

        service = TriageService(client)

        triagem = service.analisar(relato)

        st.session_state.triagem = triagem

        # Limpa testes anteriores caso um novo bug seja analisado
        st.session_state.suite_testes = None

    except ValueError as erro:

        st.warning(str(erro))

    except Exception:

        logger.exception(
            "Erro inesperado durante a análise do bug."
        )

        st.error(
            "Não foi possível analisar o bug. "
            "Tente novamente em alguns instantes."
        )


triagem = st.session_state.triagem


if triagem:

    st.subheader("Resultado da triagem")

    st.write(
        f"**Título:** {triagem.titulo}"
    )

    st.write(
        f"**Resumo:** {triagem.resumo}"
    )

    st.write(
        "**Comportamento atual:**",
        triagem.comportamento_atual
        or "Não informado"
    )

    st.write(
        "**Comportamento esperado:**",
        triagem.comportamento_esperado
        or "Não informado"
    )

    st.write(
        "**Ambiente:**",
        triagem.ambiente
        or "Não informado"
    )

    st.write(
        "**Frequência:**",
        triagem.frequencia
        or "Não informado"
    )

    st.warning(
        "A severidade abaixo é apenas "
        "uma sugestão da IA e deve ser revisada."
    )

    st.write(
        "**Severidade sugerida:**",
        triagem.severidade_sugerida.value
    )

    st.write(
        "**Justificativa:**",
        triagem.justificativa_severidade
    )

    if triagem.campos_ausentes:

        st.subheader(
            "Informações ausentes"
        )

        for campo in triagem.campos_ausentes:

            st.write(
                f"- {campo}"
            )

    if triagem.passos_reproducao:

        st.subheader(
            "Passos de reprodução"
        )

        for numero, passo in enumerate(
            triagem.passos_reproducao,
            start=1,
        ):

            st.write(
                f"{numero}. {passo}"
            )

    st.divider()

    st.subheader(
        "Geração de casos de teste"
    )

    st.warning(
        "Os casos gerados pela IA são sugestões "
        "e devem ser revisados antes de serem usados "
        "em uma suíte de testes."
    )

    if st.button("Gerar casos de teste"):

        try:

            client = GeminiClient()

            service = CaseGenerationService(
                client
            )

            suite = service.gerar(
                triagem
            )

            st.session_state.suite_testes = suite

        except ValueError as erro:

            st.warning(
                str(erro)
            )

        except Exception:

            logger.exception(
                "Erro inesperado durante a geração de casos de teste."
            )

            st.error(
                "Não foi possível gerar os casos de teste. "
                "Tente novamente em alguns instantes."
            )


suite = st.session_state.suite_testes


if suite:

    st.subheader(
        "Casos de teste sugeridos"
    )

    for caso in suite.casos:

        with st.expander(
            f"{caso.id} — {caso.titulo}"
        ):

            st.write(
                "**Tipo:**",
                caso.tipo.value
            )

            st.write(
                "**Objetivo:**",
                caso.objetivo
            )

            st.write(
                "**Pré-condições:**"
            )

            for item in caso.pre_condicoes:

                st.write(
                    f"- {item}"
                )

            st.write(
                "**Passos:**"
            )

            for numero, passo in enumerate(
                caso.passos,
                start=1,
            ):

                st.write(
                    f"{numero}. {passo}"
                )

            st.write(
                "**Resultado esperado:**",
                caso.resultado_esperado
            )

    if suite.observacoes:

        st.info(
            f"Observações: {suite.observacoes}"
        )