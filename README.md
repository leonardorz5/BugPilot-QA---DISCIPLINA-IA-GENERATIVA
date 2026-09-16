# BugPilot QA

O BugPilot QA é uma aplicação acadêmica que utiliza IA generativa para apoiar
atividades de Quality Assurance.

A solução recebe um relato de bug em linguagem natural, utiliza um LLM para
estruturar as informações e pode gerar sugestões de casos de teste a partir
da triagem produzida.

O objetivo não é substituir a análise humana, mas reduzir o trabalho manual
de organização inicial de bugs e apoiar a elaboração de cenários de teste.

---

## Funcionalidades

### Triagem de bugs

A partir de um relato textual, o sistema gera uma estrutura contendo:

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

Informações não presentes no relato devem ser identificadas como ausentes em
vez de serem inventadas pelo modelo.

### Geração de casos de teste

Após a triagem, o usuário pode solicitar sugestões de casos de teste.

Cada caso pode conter:

- identificador;
- título;
- objetivo;
- tipo de teste;
- pré-condições;
- passos;
- resultado esperado.

O sistema busca gerar apenas cenários sustentados pelas informações presentes
na triagem. Quando não houver dados suficientes para criar cenários adicionais,
a limitação deve ser informada em `observacoes`.

### Revisão humana

A severidade e os casos de teste produzidos pelo modelo são apresentados como
sugestões.

Eles não devem ser considerados automaticamente corretos e precisam ser
revisados antes de serem utilizados em um processo real de QA.

---

## Arquitetura

A solução utiliza uma arquitetura do tipo AI-as-a-Service.

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