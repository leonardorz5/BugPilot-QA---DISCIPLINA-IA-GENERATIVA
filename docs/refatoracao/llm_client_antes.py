import os

from google import genai

from bugpilot.models import BugTriage, SuiteTestes
from bugpilot.prompts import (
    TRIAGE_PROMPT,
    TEST_GENERATION_PROMPT,
)


class GeminiClient:

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gemini-3.6-flash",
    ) -> None:

        resolved_key = api_key or os.getenv("GEMINI_API_KEY")

        if not resolved_key:
            raise RuntimeError(
                "GEMINI_API_KEY não configurada."
            )

        self.client = genai.Client(
            api_key=resolved_key
        )

        self.model = model

    def analisar_bug(
        self,
        relato: str,
    ) -> BugTriage:

        prompt = f"""
{TRIAGE_PROMPT}

RELATO DO BUG:

{relato}
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": BugTriage,
            },
        )

        if response.parsed is None:
            raise RuntimeError(
                "O modelo não retornou uma resposta válida."
            )

        return response.parsed

    def gerar_casos_teste(
        self,
        triagem: BugTriage,
    ) -> SuiteTestes:

        prompt = f"""
{TEST_GENERATION_PROMPT}

TRIAGEM DO BUG:

{triagem.model_dump_json(indent=2)}
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": SuiteTestes,
            },
        )

        if response.parsed is None:
            raise RuntimeError(
                "O modelo não retornou casos de teste válidos."
            )

        return response.parsed