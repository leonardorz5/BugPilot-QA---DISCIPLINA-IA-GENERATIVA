# Evidências — V4

## 1. Revisão crítica do README

O README foi gerado com apoio de IA e posteriormente revisado contra a
implementação real do BugPilot QA.

A revisão buscou verificar se as principais afirmações da documentação estavam
de fato sustentadas pelo código existente, evitando documentar funcionalidades
que ainda não haviam sido implementadas.

### Evidências no código

#### Triagem de bugs

Afirmação do README:

> O sistema recebe um relato de bug e produz uma triagem estruturada.

Evidências:

- `bugpilot/triage_service.py` contém a validação do relato antes da chamada ao LLM.
- `bugpilot/llm_client.py` contém o método `analisar_bug`.
- `bugpilot/models.py` contém o modelo `BugTriage`.
- `app.py` apresenta o resultado da triagem na interface Streamlit.

Conclusão:

A afirmação está de acordo com o código atual.

---

#### Geração de casos de teste

Afirmação do README:

> O sistema pode gerar sugestões de casos de teste a partir da triagem.

Evidências:

- `bugpilot/generation_service.py` valida os dados necessários antes da geração.
- `bugpilot/llm_client.py` contém o método `gerar_casos_teste`.
- `bugpilot/models.py` contém `CasoTeste` e `SuiteTestes`.
- `app.py` disponibiliza a ação de geração e exibe os casos produzidos.

Conclusão:

A afirmação está de acordo com o código atual.

---

#### Validação das respostas com Pydantic

Afirmação do README:

> As respostas utilizadas pela aplicação são validadas por modelos Pydantic.

Evidências:

- `bugpilot/models.py` utiliza `BaseModel` para representar as estruturas.
- `bugpilot/llm_client.py` passa os modelos Pydantic como `response_schema`
  nas chamadas estruturadas ao Gemini.

Conclusão:

A afirmação está de acordo com o código atual.

---

#### Testes sem chamadas reais ao Gemini

Afirmação do README:

> Os testes unitários utilizam mocks para evitar chamadas reais à API.

Evidências:

- `tests/test_triage_service.py` utiliza `Mock`.
- `tests/test_test_generation_service.py` utiliza `Mock`.
- `tests/test_llm_client.py` substitui o cliente real do Gemini por objetos
  simulados.

Conclusão:

A afirmação está de acordo com a implementação dos testes.

---

#### Proteção da chave da API

Afirmação do README:

> A chave da API não é armazenada diretamente no código-fonte.

Evidências:

- `bugpilot/llm_client.py` obtém `GEMINI_API_KEY` por variável de ambiente.
- `.env.example` possui apenas um valor de exemplo.
- `.gitignore` contém `.env`.

Conclusão:

A afirmação está de acordo com o projeto atual.

---

## 2. Imprecisão encontrada durante a revisão

Durante a revisão foi identificada uma afirmação que ainda não possui evidência
completa no processo de desenvolvimento.

O README informa que foram utilizadas `custom instructions` durante o
desenvolvimento. O arquivo `.github/copilot-instructions.md` já foi criado,
porém ainda não foi realizado o experimento comparando uma sugestão da IA com
e sem essas instruções ativas.

Portanto, essa prática está preparada no projeto, mas sua utilização ainda
precisa ser demonstrada antes da versão final da documentação.

A afirmação será considerada totalmente validada somente após a realização do
experimento de custom instructions.

## 3. Revisão crítica do ADR-001

O ADR-001 classifica o BugPilot QA como uma solução AI-as-a-Service.

Essa classificação está sustentada pela implementação atual porque o modelo
não é executado dentro da aplicação. O `GeminiClient`, definido em
`bugpilot/llm_client.py`, realiza chamadas a uma API externa do Gemini.

O ADR também afirma que um AI Gateway não foi adotado porque o projeto utiliza
atualmente apenas uma aplicação e um provedor de LLM. Essa decisão corresponde
à arquitetura implementada.

### Limitação da decisão

A escolha por AI-as-a-Service simplifica o protótipo, mas cria dependência de
rede, disponibilidade e política do provedor externo. Portanto, a decisão não
deve ser interpretada como a arquitetura ideal para qualquer evolução futura
do sistema.

Caso o BugPilot passe a utilizar múltiplos modelos, requisitos mais rígidos de
auditoria, controle centralizado de custos ou tratamento de dados confidenciais,
a arquitetura deverá ser reavaliada.


## 4. Experimento com Custom Instructions

### Solicitação utilizada

Quero fazer uma pequena alteração no BugPilot QA.

Atualmente o sistema aceita relatos de bugs de qualquer tamanho.
Adicione uma validação para impedir relatos com mais de 5000 caracteres.

Sugira a menor alteração necessária ao projeto e mostre o código que você
criaria ou modificaria.

Inclua também os testes que considerar necessários.

### Resposta sem Custom Instructions
A menor alteração é centralizar o limite em TriageService, pois todo relato passa por analisar() antes de chegar ao LLM. O app.py já captura ValueError e exibe a mensagem ao usuário, portanto não precisa ser alterado.

1. Arquivos

Alterar apenas:

triage_service.py:4
test_triage_service.py:1
2. Código

Em TriageService, adicionar a constante e a validação:


A validação deve ocorrer depois de strip(), mantendo o comportamento atual do serviço.

3. Testes automatizados

Adicionar em test_triage_service.py:19:


Esses testes cobrem a rejeição acima do limite e o valor exato permitido. O caso abaixo de 5000 já fica coberto pelo teste existente de relato válido.

### Resposta com Custom Instructions

A menor alteração é validar o tamanho em TriageService, antes da chamada ao LLM. Isso segue as instruções do projeto para validações determinísticas locais.

1. Arquivos a alterar

triage_service.py
test_triage_service.py
Nenhuma alteração é necessária em app.py, pois ele já captura ValueError e exibe a mensagem.

2. Alteração em triage_service.py


Após a validação do tamanho mínimo:


A validação deve permanecer antes de:


3. Testes necessários

Adicionar em test_triage_service.py:


O teste de relato válido já cobre valores abaixo de 5000. Não serão feitas alterações no projeto.

### Comparação das respostas

As duas respostas chegaram a uma solução tecnicamente semelhante: realizar a
validação do limite de 5000 caracteres em `TriageService` e adicionar testes em
`test_triage_service.py`.

Mesmo sem as Custom Instructions, o assistente identificou corretamente que a
regra deveria ficar no serviço, evitando alterações desnecessárias em `app.py`.
Isso indica que a arquitetura e o código existentes já forneciam contexto
suficiente para orientar parte da solução.

Com as Custom Instructions ativas, entretanto, a justificativa ficou mais
alinhada às convenções definidas para o projeto. O assistente afirmou
explicitamente que a validação deveria ocorrer antes da chamada ao LLM por se
tratar de uma validação determinística local.

A regra que produziu a diferença mais visível foi:

> "Validações determinísticas de entrada devem ser executadas em Python antes
> de qualquer chamada ao LLM."

A resposta com as instruções também reforçou que nenhuma alteração seria
necessária em `app.py`, preservando a separação entre interface e regra de
negócio.

Neste experimento, as instruções não provocaram uma mudança radical na
implementação proposta. A principal razão é que o projeto já possuía uma
arquitetura bem definida, com `TriageService` responsável pelas validações e
testes existentes que serviam como referência para o assistente.

Portanto, o resultado indica que Custom Instructions funcionaram principalmente
como mecanismo de consistência e explicitação das convenções do projeto, e não
como substituto para uma arquitetura de código bem organizada.

## 5. Implementação da alteração sugerida

Após o experimento com e sem Custom Instructions, a validação de tamanho máximo
do relato foi implementada no `TriageService`.

Foi adicionada a constante:

`MAX_REPORT_LENGTH = 5000`

A validação ocorre localmente antes da chamada ao LLM.

Também foram adicionados dois testes de fronteira:

- relato com exatamente 5000 caracteres deve ser aceito;
- relato com 5001 caracteres deve ser rejeitado e o LLM não deve ser chamado.

Após a implementação, a suíte completa foi executada.

Resultado:

- 16 testes coletados;
- 16 testes aprovados;
- nenhuma falha.

Esse resultado confirma que a nova regra foi adicionada sem quebrar os
comportamentos já cobertos pela suíte.