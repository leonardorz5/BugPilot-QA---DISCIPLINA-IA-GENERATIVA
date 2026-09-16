from bugpilot.models import BugTriage


class TriageService:

    MIN_REPORT_LENGTH = 20

    def __init__(self, llm) -> None:
        self.llm = llm

    def analisar(
        self,
        relato: str,
    ) -> BugTriage:

        relato = relato.strip()

        if not relato:
            raise ValueError(
                "O relato do bug não pode estar vazio."
            )

        if len(relato) < self.MIN_REPORT_LENGTH:
            raise ValueError(
                "O relato deve possuir pelo menos "
                f"{self.MIN_REPORT_LENGTH} caracteres."
            )

        return self.llm.analisar_bug(relato)