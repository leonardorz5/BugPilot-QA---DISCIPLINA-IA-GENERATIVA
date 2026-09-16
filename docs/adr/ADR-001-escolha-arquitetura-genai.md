# ADR-001 — Escolha da Arquitetura GenAI do BugPilot QA

## Status

Aceito

## Data

16/09/2026

## Contexto

O BugPilot QA é uma aplicação voltada ao apoio do processo de Quality Assurance.
A solução recebe relatos de bugs em linguagem natural, utiliza um modelo de
linguagem para produzir uma triagem estruturada e também pode sugerir casos de
teste a partir das informações identificadas.

A aplicação precisava integrar recursos de IA generativa sem exigir a execução
local de um modelo, mantendo a implementação simples o suficiente para um
protótipo acadêmico.

Também era necessário:

- utilizar uma interface gráfica simples;
- obter respostas estruturadas do modelo;
- validar as respostas antes de utilizá-las na aplicação;
- evitar exposição de credenciais no código;
- permitir testes unitários sem depender de chamadas reais à API;
- manter separação entre interface, regras de negócio e integração com o LLM.

## Decisão

Foi adotada uma arquitetura do tipo AI-as-a-Service.

O BugPilot QA utiliza uma API externa de LLM por meio da classe `GeminiClient`.
A aplicação não executa nem hospeda localmente o modelo de linguagem.

A arquitetura principal é:

```text
Usuário
   ↓
Interface Streamlit
   ↓
Serviços da aplicação
   ├── TriageService
   └── CaseGenerationService
   ↓
GeminiClient
   ↓
Gemini API