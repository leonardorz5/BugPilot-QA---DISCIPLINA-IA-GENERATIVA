# Spec — Geração de Casos de Teste a partir de um Bug

## Objetivo

Permitir que o BugPilot QA gere sugestões de casos de teste a partir de uma
triagem de bug previamente estruturada.

## Critérios de aceite

1. O sistema deve receber uma triagem contendo, no mínimo:
   - título;
   - resumo;
   - comportamento esperado;
   - comportamento atual.

2. Se comportamento esperado ou comportamento atual estiverem ausentes,
   o sistema não deve solicitar ao LLM a geração de casos de teste.

3. Para uma triagem válida, o sistema deve gerar somente casos de teste
sustentados pelas informações disponíveis.

O sistema deve buscar gerar até três casos distintos quando houver
informação suficiente. Caso não existam dados suficientes para isso,
deve gerar uma quantidade menor e explicar a limitação em `observacoes`.

4. Cada caso de teste deve conter:
   - identificador;
   - título;
   - objetivo;
   - tipo;
   - pré-condições;
   - passos;
   - resultado esperado.

5. Cenários positivos, negativos, de borda ou regressão somente devem ser
gerados quando houver informações na triagem que sustentem o comportamento
esperado desses cenários.

6. O sistema não deve inventar detalhes técnicos ausentes na triagem.

7. A resposta produzida pelo LLM deve ser validada por um modelo Pydantic
   antes de ser utilizada pela aplicação.

8. Os casos gerados devem ser apresentados como sugestões sujeitas à
   revisão humana antes de serem incorporados a uma suíte de testes.