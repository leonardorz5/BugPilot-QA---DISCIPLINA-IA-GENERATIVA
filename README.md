# 🐞 BugPilot QA

O **BugPilot QA** é uma aplicação de apoio ao processo de Quality Assurance que utiliza IA generativa para auxiliar na **triagem de bugs** e na **geração de casos de teste**.

A aplicação recebe um relato textual, estrutura as informações utilizando o Gemini e permite gerar sugestões de cenários de teste a partir da triagem realizada.

> As respostas produzidas pela IA são sugestões e devem passar por revisão humana antes de serem utilizadas em um processo real de QA.

---

# Como executar o projeto

## Pré-requisitos

Para executar o BugPilot QA é necessário possuir:

- Python 3.11 ou compatível;
- conexão com a internet;
- uma chave própria de acesso à API do Google Gemini.

> **A chave da API não acompanha este projeto.**
>
> Cada pessoa que executar a aplicação deve gerar e utilizar **sua própria chave da API Gemini**.

A chave não deve ser escrita diretamente no código-fonte nem enviada para o repositório.

---

## 1. Clonar ou baixar o projeto

Entre na pasta do projeto:

```powershell
cd BugPilot-QA
```

---

## 2. Criar um ambiente virtual

No Windows:

```powershell
python -m venv .venv
```

---

## 3. Ativar o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Quando ativado, o terminal deverá apresentar algo semelhante a:

```text
(.venv) PS C:\...\BugPilot-QA>
```

---

## 4. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

---

## 5. Configurar a chave da API Gemini

Na raiz do projeto existe o arquivo:

```text
.env.example
```

Crie um novo arquivo chamado:

```text
.env
```

e adicione sua própria chave:

```env
GEMINI_API_KEY=SUA_CHAVE_DO_GEMINI_AQUI
```

Exemplo da estrutura:

```text
BugPilot-QA/
├── .env
├── .env.example
├── app.py
├── requirements.txt
└── ...
```

### Importante

O arquivo `.env` contém uma credencial pessoal e **não deve ser enviado ao GitHub ou compartilhado com outras pessoas**.

O projeto já possui `.env` no `.gitignore`.

---

## 6. Executar a aplicação

Com o ambiente virtual ativo:

```powershell
streamlit run app.py
```

O Streamlit disponibilizará a aplicação localmente, normalmente em:

```text
http://localhost:8501
```

---

## 7. Executar os testes

```powershell
python -m pytest -v
```

Na última execução registrada do projeto:

```text
16 testes coletados
16 testes aprovados
0 falhas
```

Os testes unitários utilizam mocks e não realizam chamadas reais ao Gemini.

---

# Funcionalidades

## Triagem de bugs

A partir de um relato em linguagem natural, o BugPilot QA gera uma estrutura contendo:

- título;
- resumo;
- passos de reprodução;
- comportamento atual;
- comportamento esperado;
- ambiente, quando informado;
- frequência, quando informada;
- informações ausentes;
- sugestão de severidade;
- justificativa da severidade.

Informações que não estiverem disponíveis no relato devem ser sinalizadas como ausentes em vez de serem inventadas pelo modelo.

---

## Geração de casos de teste

Após a triagem, o usuário pode solicitar sugestões de casos de teste.

Cada caso pode conter:

- identificador;
- título;
- objetivo;
- tipo;
- pré-condições;
- passos;
- resultado esperado.

O sistema prioriza a **rastreabilidade das informações** em vez da quantidade de casos gerados.

Caso não existam dados suficientes para gerar cenários adicionais de forma confiável, o sistema pode produzir menos casos e registrar a limitação em `observacoes`.

---

## Revisão humana

A aplicação não trata as respostas do LLM como automaticamente corretas.

Exigem revisão humana:

- severidade sugerida;
- casos de teste gerados;
- código produzido ou refatorado com apoio de IA;
- documentação produzida com apoio de IA.

Durante o desenvolvimento foram encontrados casos em que respostas estruturalmente válidas continham pressuposições não presentes no relato original.

Por isso, validação estrutural e revisão humana são utilizadas em conjunto.

---

# Validação de entrada

Antes de qualquer chamada ao LLM, o relato passa por validações determinísticas em Python.

Atualmente:

- o relato não pode estar vazio;
- deve possuir pelo menos **20 caracteres**;
- deve possuir no máximo **5000 caracteres**.

Exemplos de testes de fronteira existentes:

```text
5000 caracteres → aceito
5001 caracteres → rejeitado
```

Essas validações acontecem antes da API, evitando chamadas desnecessárias ao modelo.

---

# Arquitetura

O BugPilot QA utiliza uma arquitetura **AI-as-a-Service**.

```text
Usuário
   |
   v
Streamlit
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
```

As responsabilidades foram separadas para evitar que interface, regras de negócio e integração com IA fiquem concentradas no mesmo módulo.

---

## Principais componentes

### `app.py`

Interface gráfica construída com Streamlit.

---

### `bugpilot/models.py`

Contém os modelos Pydantic utilizados para representar e validar:

- triagem;
- severidade;
- casos de teste;
- suítes de teste.

---

### `bugpilot/prompts.py`

Contém as instruções utilizadas para:

- triagem de bugs;
- geração de casos de teste;
- restrição de informações não sustentadas;
- separação entre instruções do sistema e conteúdo do usuário.

---

### `bugpilot/triage_service.py`

Responsável pelas validações determinísticas realizadas antes da chamada ao LLM.

Inclui:

```text
MIN_REPORT_LENGTH = 20
MAX_REPORT_LENGTH = 5000
```

---

### `bugpilot/generation_service.py`

Verifica se existem informações mínimas suficientes para solicitar casos de teste ao LLM.

Também rejeita campos:

```text
None
""
"   "
```

quando representam informações obrigatórias.

---

### `bugpilot/llm_client.py`

Encapsula a comunicação com a API do Gemini.

As respostas são solicitadas utilizando **structured output** e modelos Pydantic.

A lógica comum de geração estruturada foi refatorada para:

```text
_gerar_resposta_estruturada()
```

---

# Tecnologias

- Python 3.11
- Streamlit
- Google Gemini API
- `google-genai`
- Pydantic
- Pytest
- python-dotenv
- Model Context Protocol — MCP

O modelo utilizado atualmente pela aplicação é:

```text
gemini-3.6-flash
```

---

# Testes automatizados

A suíte atual possui **16 testes automatizados**.

Entre os comportamentos verificados estão:

- rejeição de relato vazio;
- rejeição de relato muito curto;
- aceitação de relato válido;
- limite máximo de 5000 caracteres;
- rejeição de 5001 caracteres;
- ausência de comportamento esperado;
- ausência de comportamento atual;
- strings vazias;
- strings contendo apenas espaços;
- geração de quantidade reduzida de casos quando faltam informações;
- structured output da triagem;
- structured output dos casos de teste;
- comportamento do cliente quando a resposta do modelo não pode ser parseada.

Execute:

```powershell
python -m pytest -v
```

Último resultado registrado:

```text
16 passed
```

---

# Desenvolvimento Spec-Driven

A funcionalidade de geração de casos de teste foi construída utilizando uma abordagem spec-driven.

A especificação está em:

```text
docs/spec-generate-tests.md
```

O fluxo utilizado foi:

```text
Spec
  |
  v
Plano produzido pela IA
  |
  v
Revisão humana
  |
  v
Plano ajustado
  |
  v
Implementação
  |
  v
Testes
  |
  v
Execução real
  |
  v
Revisão da saída
```

Durante esse processo, a própria especificação precisou ser revisada.

Inicialmente era exigida uma quantidade mínima de três casos de teste, o que incentivou o modelo a criar cenários não sustentados pelas informações disponíveis.

A regra foi alterada para priorizar:

```text
Rastreabilidade > quantidade
```

---

# Refatoração assistida por IA

Foi realizada uma refatoração no `GeminiClient`.

Antes da alteração:

```text
14 testes aprovados
```

Depois da alteração:

```text
14 testes aprovados
```

Os mesmos testes foram utilizados antes e depois da refatoração.

As versões estão disponíveis em:

```text
docs/refatoracao/
├── llm_client_antes.py
└── llm_client_depois.py
```

---

# Custom Instructions

O projeto possui:

```text
.github/copilot-instructions.md
```

O arquivo estabelece regras específicas para assistentes de código, incluindo:

- funções públicas devem possuir type hints;
- validações determinísticas devem acontecer antes do LLM;
- segredos não podem ser colocados diretamente no código;
- respostas do LLM devem ser validadas com Pydantic;
- testes unitários não devem realizar chamadas reais à API;
- informações ausentes não devem ser inventadas;
- resultados gerados por IA exigem revisão humana;
- refatorações devem preservar contratos públicos quando aplicável.

Foi realizado um experimento utilizando a mesma solicitação com e sem essas instruções.

A alteração escolhida foi a implementação do limite máximo de 5000 caracteres para relatos.

---

# Segurança e Governança

As principais medidas adotadas no projeto são:

- chave da API armazenada em variável de ambiente;
- arquivo `.env` ignorado pelo Git;
- `.env.example` sem credenciais reais;
- validações determinísticas antes do LLM;
- limite máximo de 5000 caracteres;
- structured output;
- validação com Pydantic;
- mocks durante os testes;
- mensagens internas de exceção não são exibidas diretamente ao usuário;
- revisão humana das respostas;
- separação explícita entre instruções do sistema e conteúdo do usuário;
- mitigação básica contra prompt injection.

---

## Tratamento de exceções

Erros inesperados são registrados utilizando:

```python
logging.exception(...)
```

Enquanto a interface apresenta ao usuário uma mensagem genérica.

Isso reduz o risco de exposição de detalhes internos retornados pelo SDK ou pela API.

---

## Prompt Injection

O conteúdo fornecido pelo usuário é tratado explicitamente como dado.

No prompt, o relato é delimitado:

```text
<relato_bug>
...
</relato_bug>
```

Também existem instruções para que o modelo não execute comandos presentes dentro do relato.

Foi realizado um teste controlado contendo uma tentativa de forçar:

- severidade Crítica;
- ambiente Produção;
- remoção de campos ausentes.

O modelo ignorou essas instruções no cenário testado e retornou:

```text
Severidade: Média
Ambiente: Não informado
Frequência: Não informado
```

Essa abordagem deve ser considerada uma **mitigação**, e não uma garantia absoluta contra prompt injection.

---

# Proteção de credenciais

A aplicação lê:

```text
GEMINI_API_KEY
```

a partir do ambiente.

O comando:

```powershell
git check-ignore .env
```

confirmou:

```text
.env
```

O arquivo também não aparece em `git status`.

---

# Dependências

O ambiente foi verificado com:

```powershell
python -m pip check
```

Resultado registrado:

```text
No broken requirements found.
```

As dependências do ambiente estão registradas em:

```text
requirements.txt
```

O projeto utiliza atualmente:

```text
mcp==2.2.0
```

para suporte ao Model Context Protocol.

---

# MCP

O projeto contém um servidor MCP simples:

```text
mcp_server.py
```

A tool disponibilizada é:

```text
validar_relato_bug
```

Ela reutiliza:

```python
TriageService.validar_relato()
```

em vez de duplicar as regras de validação.

O fluxo é:

```text
Cliente MCP
    |
    v
validar_relato_bug
    |
    v
TriageService.validar_relato
```

A integração foi testada com o **MCP Inspector** utilizando relatos válidos e inválidos.

---

# Custom Instructions x MCP

As duas formas de personalização atuam em níveis diferentes.

```text
Custom Instructions
        ↓
orientam COMO o assistente trabalha


MCP
        ↓
amplia O QUE um agente consegue executar
```

No BugPilot:

- Custom Instructions orientam arquitetura, testes, validações e segurança;
- MCP expõe a validação de relatos como uma ferramenta executável.

---

# Documentação

A pasta `docs/` contém:

```text
docs/
├── adr/
│   └── ADR-001-escolha-arquitetura-genai.md
│
├── refatoracao/
│   ├── llm_client_antes.py
│   └── llm_client_depois.py
│
├── evidencias-v2.md
├── evidencias-v3.md
├── evidencias-v4.md
├── evidencias-v5.md
├── evidencias-finais.md
└── spec-generate-tests.md
```

---

# ADR

A decisão sobre arquitetura GenAI está documentada em:

```text
docs/adr/ADR-001-escolha-arquitetura-genai.md
```

A arquitetura atual foi classificada como:

```text
AI-as-a-Service
```

Um AI Gateway não foi adotado devido ao escopo atual possuir apenas:

- uma aplicação;
- um provedor de LLM;
- baixo volume de chamadas.

A decisão deve ser reavaliada caso o projeto passe a necessitar de múltiplos modelos, controle centralizado de custos, observabilidade ou roteamento.

---

# Evidências

As evidências visuais estão armazenadas em:

```text
evidencias/
```

Entre elas:

```text
v1_triagem_gemini.png
v4_limite_5000.png
v4_pytest_16_passed.png
v5_mcp_inspector.png
```

As evidências textuais e registros do processo estão disponíveis na pasta:

```text
docs/
```

---

# Limitações atuais

O BugPilot QA é um protótipo acadêmico.

Entre as principais limitações estão:

- dependência de um serviço externo de IA;
- necessidade de conexão com a internet;
- possibilidade de respostas semanticamente incorretas;
- mitigação de prompt injection não absoluta;
- ausência de persistência de histórico;
- ausência de integração direta com Jira ou outras ferramentas;
- ausência de autenticação própria;
- necessidade de revisão humana;
- dependência das políticas e disponibilidade do provedor de IA.

---

# Estrutura do projeto

```text
BugPilot-QA/
│
├── .github/
│   └── copilot-instructions.md
│
├── bugpilot/
│   ├── __init__.py
│   ├── generation_service.py
│   ├── llm_client.py
│   ├── models.py
│   ├── prompts.py
│   └── triage_service.py
│
├── docs/
│   ├── adr/
│   ├── refatoracao/
│   ├── evidencias-v2.md
│   ├── evidencias-v3.md
│   ├── evidencias-v4.md
│   ├── evidencias-v5.md
│   ├── evidencias-finais.md
│   └── spec-generate-tests.md
│
├── evidencias/
│
├── tests/
│   ├── test_llm_client.py
│   ├── test_test_generation_service.py
│   └── test_triage_service.py
│
├── .env.example
├── .gitignore
├── app.py
├── mcp_server.py
├── README.md
└── requirements.txt
```

> O arquivo `.env` e a pasta `.venv` não fazem parte da distribuição do projeto.

---

# Status

✅ **Projeto Final concluído**

Desenvolvido para a disciplina:

**IA Generativa em Engenharia de Software — PUC Minas**

O estado final inclui:

- triagem de bugs com IA;
- geração de casos de teste;
- structured output;
- validação Pydantic;
- desenvolvimento spec-driven;
- refatoração assistida por IA;
- suíte automatizada com 16 testes;
- Custom Instructions;
- documentação automatizada;
- ADR;
- segurança e governança;
- mitigação básica de prompt injection;
- tratamento seguro de exceções;
- servidor MCP;
- revisão humana das saídas geradas.