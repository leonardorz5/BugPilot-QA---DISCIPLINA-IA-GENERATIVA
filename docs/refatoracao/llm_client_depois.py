import os
from typing import TypeVar

from google import genai
from pydantic import BaseModel

from bugpilot.models import BugTriage, SuiteTestes
from bugpilot.prompts import (
    TEST_GENERATION_PROMPT,
    TRIAGE_PROMPT,
)


T = TypeVar(
    "T",
    bound=BaseModel,
)


class GeminiClient:

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gemini-3.6-flash",
    ) -> None:

        resolved_key = (
            api_key
            or os.getenv("GEMINI_API_KEY")
        )

        if not resolved_key:
            raise RuntimeError(
                "GEMINI_API_KEY não configurada."
            )

        self.client = genai.Client(
            api_key=resolved_key
        )

        self.model = model

    def _gerar_resposta_estruturada(
        self,
        prompt: str,
        schema: type[T],
        mensagem_erro: str,
    ) -> T:

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": schema,
            },
        )

        if response.parsed is None:
            raise RuntimeError(
                mensagem_erro
            )

        return response.parsed

    def analisar_bug(
        self,
        relato: str,
    ) -> BugTriage:

        prompt = f"""
{TRIAGE_PROMPT}

RELATO DO BUG:

{relato}
"""

        return self._gerar_resposta_estruturada(
            prompt=prompt,
            schema=BugTriage,
            mensagem_erro=(
                "O modelo não retornou uma resposta válida."
            ),
        )

    def gerar_casos_teste(
        self,
        triagem: BugTriage,
    ) -> SuiteTestes:

        prompt = f"""
{TEST_GENERATION_PROMPT}

TRIAGEM DO BUG:

{triagem.model_dump_json(indent=2)}
"""

        return self._gerar_resposta_estruturada(
            prompt=prompt,
            schema=SuiteTestes,
            mensagem_erro=(
                "O modelo não retornou casos de teste válidos."
            ),
        )