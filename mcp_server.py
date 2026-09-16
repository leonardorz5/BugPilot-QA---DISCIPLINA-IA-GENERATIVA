from mcp.server import MCPServer

from bugpilot.triage_service import TriageService


mcp = MCPServer("BugPilot QA")


@mcp.tool()
def validar_relato_bug(
    relato: str,
) -> dict[str, object]:
    """
    Valida deterministicamente um relato de bug
    antes de seu envio ao LLM.
    """

    try:
        relato_validado = TriageService.validar_relato(
            relato
        )

        return {
            "valido": True,
            "tamanho": len(relato_validado),
            "mensagem": "Relato válido para processamento.",
        }

    except ValueError as erro:
        return {
            "valido": False,
            "tamanho": len(relato.strip()),
            "mensagem": str(erro),
        }


if __name__ == "__main__":
    mcp.run()