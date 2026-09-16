# Projeto Final — BugPilot QA

**Disciplina:** IA Generativa em Engenharia de Software  
**Instituição:** PUC Minas  
**Aluno:** [PREENCHER NOME]

---

# 1. Visão Geral

O BugPilot QA é uma aplicação de apoio ao processo de Quality Assurance que
utiliza IA generativa para auxiliar na triagem de bugs e na geração de casos
de teste.

O sistema recebe um relato textual de um problema e utiliza um LLM para
estruturá-lo em informações como:

- título;
- resumo;
- comportamento atual;
- comportamento esperado;
- passos de reprodução;
- ambiente;
- frequência;
- informações ausentes;
- sugestão de severidade.

Após a triagem, o sistema pode gerar sugestões de casos de teste baseadas
somente nas informações disponíveis.

A solução foi desenvolvida com foco em revisão humana, evitando tratar a
resposta do LLM como automaticamente correta.

---

# 2. Problema Escolhido

Durante processos de QA, relatos de bugs podem chegar de forma pouco
estruturada, contendo informações incompletas ou espalhadas em texto livre.

Isso exige trabalho manual para identificar:

- o que ocorreu;
- qual era o comportamento esperado;
- como reproduzir;
- quais informações ainda estão faltando;
- quais cenários merecem ser testados.

O BugPilot QA foi criado para auxiliar nessa etapa inicial, transformando
relatos livres em informações estruturadas e sugerindo casos de teste.

A proposta não é substituir o QA, mas fornecer uma primeira organização que
deve ser revisada antes de uso.

---

# 3. Modelo de IA Utilizado

Foi utilizado o modelo:

`gemini-3.6-flash`

A integração é realizada pelo SDK `google-genai`.

## Justificativa

A escolha considerou três aspectos principais:

### Custo

O modelo pertence à família Flash, adequada a interações frequentes com custo
inferior ao de modelos de maior capacidade.

Para o escopo acadêmico do BugPilot QA, não existe necessidade de utilizar um
modelo mais caro para tarefas como estruturação de texto e geração inicial de
casos de teste.

### Latência

A aplicação possui interface interativa, portanto o tempo de resposta influencia
diretamente a experiência do usuário.

Foi priorizado um modelo da família Flash por sua orientação a respostas rápidas.

Não foi realizado benchmark formal de latência no projeto. Portanto, a escolha
é baseada nas características declaradas pelo provedor e na experiência durante
as execuções realizadas.

### Contexto

O limite de contexto disponível é muito superior ao tamanho máximo de entrada
utilizado pelo BugPilot QA.

Além disso, a aplicação restringe os relatos a 5000 caracteres, evitando enviar
conteúdo excessivamente grande ao LLM.

Essa decisão reduz consumo desnecessário de tokens e mantém o caso de uso bem
abaixo dos limites do modelo.

---

# 4. Arquitetura

O BugPilot QA utiliza uma arquitetura AI-as-a-Service.

```text
Usuário
   |
   v
Interface Streamlit
   |
   v
Serviços da aplicação
   |
   +-- TriageService
   |
   +-- CaseGenerationService
   |
   v
GeminiClient
   |
   v
Gemini API