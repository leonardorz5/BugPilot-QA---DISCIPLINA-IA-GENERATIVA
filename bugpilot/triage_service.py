from bugpilot.models import BugTriage


class TriageService:

    MIN_REPORT_LENGTH = 20
    MAX_REPORT_LENGTH = 5000

    def __init__(self, llm) -> None:
        self.llm = llm

    @classmethod
    def validar_relato(
        cls,
        relato: str,
    ) -> str:

        relato_limpo = relato.strip()

        if not relato_limpo:
            raise ValueError(
                "O relato do bug não pode estar vazio."
            )

        if len(relato_limpo) < cls.MIN_REPORT_LENGTH:
            raise ValueError(
                "O relato deve possuir pelo menos "
                f"{cls.MIN_REPORT_LENGTH} caracteres."
            )

        if len(relato_limpo) > cls.MAX_REPORT_LENGTH:
            raise ValueError(
                "O relato deve possuir no máximo "
                f"{cls.MAX_REPORT_LENGTH} caracteres."
            )

        return relato_limpo

    def analisar(
        self,
        relato: str,
    ) -> BugTriage:

        relato_validado = self.validar_relato(
            relato
        )

        return self.llm.analisar_bug(
            relato_validado
        )