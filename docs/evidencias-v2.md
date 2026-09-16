## Revisão do resultado da implementação

A primeira execução real da geração produziu três casos de teste e respeitou
a estrutura definida pelo Pydantic. Entretanto, a revisão humana identificou
que o terceiro caso gerado introduziu uma regra de negócio não presente na
triagem original.

O caso TC03 assumiu que, ao editar um nome sem salvar e atualizar a página,
o nome anterior deveria permanecer exibido. Embora esse comportamento possa
ser plausível, ele não foi informado no relato do bug e, portanto, não poderia
ser tratado como requisito confirmado.

A execução também revelou uma tensão na própria spec: ela exigia pelo menos
três casos de teste ao mesmo tempo em que proibia a criação de informações
não sustentadas pela triagem. Em relatos com poucas informações, a exigência
de quantidade pode incentivar o LLM a criar cenários adicionais sem evidência.

Por esse motivo, a spec será revisada para priorizar rastreabilidade e
correção sobre quantidade de casos gerados.

## Segunda revisão do resultado

Após a revisão da spec, o modelo deixou de gerar artificialmente três casos
de teste e passou a produzir apenas um cenário sustentado pelas informações
disponíveis, registrando corretamente a limitação em `observacoes`.

Entretanto, ainda foram criadas pré-condições não presentes na triagem, como
“usuário autenticado no sistema”. Isso mostrou que reduzir a quantidade de
casos não elimina automaticamente todas as inferências não rastreáveis.

O prompt foi então refinado novamente para determinar que pré-condições também
devem estar explicitamente sustentadas pela triagem e que, na ausência dessas
informações, `pre_condicoes` deve ser retornado como lista vazia.

## Resultado final da V2

Após os refinamentos da spec e do prompt, a nova execução produziu dois casos
de teste sustentados pelas informações presentes na triagem.

Diferentemente das execuções anteriores, o modelo não criou pré-condições
não informadas e retornou `pre_condicoes` vazia nos dois casos. Também não
forçou a criação de um terceiro cenário negativo ou de borda apenas para
atingir uma quantidade mínima.

O modelo registrou explicitamente em `observacoes` que não havia informações
suficientes sobre regras de validação, limites de caracteres ou permissões
para produzir outros cenários sem fazer pressuposições.

A suíte automatizada foi executada após as alterações e apresentou 11 testes
aprovados. A execução manual no Streamlit também confirmou o funcionamento
da integração completa com o Gemini.

A experiência mostrou que a validação estrutural com Pydantic é necessária,
mas não suficiente: uma resposta pode respeitar perfeitamente o schema e ainda
conter pressuposições incorretas. A revisão humana do conteúdo continuou sendo
necessária.