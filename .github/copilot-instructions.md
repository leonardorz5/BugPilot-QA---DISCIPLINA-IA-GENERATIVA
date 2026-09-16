# BugPilot QA — Instruções para Assistentes de Código

1. Toda função pública adicionada ao pacote `bugpilot` deve possuir type hints
   nos parâmetros e no retorno.

2. Validações determinísticas de entrada devem ser executadas em Python antes
   de qualquer chamada ao LLM. Não delegar ao modelo validações que podem ser
   realizadas localmente.

3. Nenhuma chave de API, token ou segredo pode ser escrito diretamente no
   código-fonte. Segredos devem ser obtidos por variáveis de ambiente.

4. Toda resposta do LLM utilizada pela aplicação deve passar por validação de
   um modelo Pydantic antes de ser consumida.

5. Testes unitários não devem realizar chamadas reais ao Gemini. A dependência
   externa deve ser substituída por mock ou equivalente.

6. O assistente não deve criar regras de negócio, pré-condições ou informações
   ausentes apenas para completar uma resposta.

7. Sugestões de severidade e casos de teste gerados por IA devem permanecer
   explicitamente sujeitos à revisão humana.

8. Alterações de refatoração devem preservar as assinaturas públicas existentes,
   salvo quando a mudança de contrato for parte explícita da especificação.