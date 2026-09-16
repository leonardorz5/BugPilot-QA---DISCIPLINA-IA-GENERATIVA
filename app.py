import streamlit as st
from dotenv import load_dotenv

from bugpilot.llm_client import GeminiClient
from bugpilot.triage_service import TriageService


load_dotenv()


st.set_page_config(
    page_title="BugPilot QA",
    page_icon="🐞",
)


st.title("🐞 BugPilot QA")

st.write(
    "Assistente de triagem de bugs com IA generativa."
)


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
            "uma sugestão da IA."
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

    except ValueError as erro:

        st.warning(str(erro))

    except Exception as erro:

        st.error(
            f"Erro ao analisar bug: {erro}"
        )