# Evidências — V3

## Refatoração escolhida

Foi escolhido o arquivo `bugpilot/llm_client.py`.

Os métodos `analisar_bug` e `gerar_casos_teste` possuem responsabilidades
diferentes, mas repetem a mesma estrutura para:

- chamar `client.models.generate_content`;
- definir `response_mime_type` como `application/json`;
- informar um schema Pydantic;
- verificar se `response.parsed` está disponível;
- retornar a resposta estruturada.

O objetivo da refatoração é reduzir essa duplicação sem alterar o
comportamento público dos métodos.
## Prompt utilizado na refatoração

Analise o arquivo `llm_client.py` do BugPilot QA e proponha uma refatoração
para eliminar a duplicação existente entre `analisar_bug` e
`gerar_casos_teste`.

Restrições:

1. Não alterar as assinaturas públicas de `analisar_bug` e
   `gerar_casos_teste`.
2. Não alterar os prompts enviados ao Gemini.
3. Não alterar o modelo utilizado.
4. Manter o uso de structured output com Pydantic.
5. Manter o tratamento de erro quando `response.parsed` for `None`.
6. Não adicionar novas dependências.
7. A refatoração deve preservar o comportamento atual.

Primeiro apresente apenas o plano da refatoração, sem gerar o código.
## Plano sugerido pela IA

1. Criar um método privado responsável pela chamada estruturada ao Gemini.
2. O método privado receberá o prompt, o schema Pydantic esperado e a
   mensagem de erro correspondente.
3. `analisar_bug` continuará responsável por construir o prompt de triagem.
4. `gerar_casos_teste` continuará responsável por construir o prompt de testes.
5. Os dois métodos públicos delegarão somente a parte repetida da chamada
   ao novo método privado.
6. Antes da alteração, testes deverão caracterizar o comportamento atual do
   cliente para permitir comparar o resultado após a refatoração.
   ## Revisão humana do plano

O plano reduz uma duplicação real sem mudar as responsabilidades públicas
da classe. Antes de realizar a refatoração, porém, farei um ajuste no fluxo:
primeiro serão criados testes automatizados para os dois métodos públicos
utilizando mocks da API do Gemini.

Dessa forma, os testes serão executados ainda sobre a implementação antiga e
novamente após a refatoração. Isso evita utilizar os próprios testes como
consequência da nova implementação e fornece uma referência mais confiável
para verificar se o comportamento permaneceu equivalente.

A chamada real ao Gemini não será utilizada nesses testes, pois o objetivo é
validar o comportamento do cliente e não disponibilidade, latência ou custo
da API externa.

## Resultado da refatoração

Antes da refatoração, a suíte foi executada com a implementação original
e apresentou 14 testes aprovados.

A duplicação das chamadas estruturadas ao Gemini foi então extraída para
o método privado `_gerar_resposta_estruturada`. As assinaturas públicas
de `analisar_bug` e `gerar_casos_teste`, os prompts utilizados, o modelo,
os schemas Pydantic e as mensagens de erro foram preservados.

Após a alteração, a mesma suíte de testes foi executada novamente sem
modificações nos testes de caracterização.

### Resultado antes

14 testes aprovados.

## Resultado final da refatoração

A suíte foi executada antes da refatoração e apresentou:

- 14 testes coletados;
- 14 testes aprovados;
- nenhuma falha.

Após a extração da lógica repetida de chamada estruturada ao Gemini para o
método privado `_gerar_resposta_estruturada`, a mesma suíte foi executada
novamente, sem alteração nos testes.

Resultado após a refatoração:

- 14 testes coletados;
- 14 testes aprovados;
- nenhuma falha.

Isso indica que a refatoração reduziu duplicação interna sem alterar os
comportamentos públicos cobertos pelos testes automatizados.