---
name: gestalt-integracao
description: Sintetiza conversas reflexivas sem salvar.
version: 3.0.0
metadata:
  hermes:
    category: wellbeing
    tags: [gestalt, reflexao, autoconhecimento]
---
# Gestalt Integracao

## When to Use

Use apenas para sínteses de reflexão, integração e revisão de conteúdo fornecido; se o destino é a terapeuta humana, preferir `preparo-para-terapia`.


Quando o usuário solicita resumo, retomada de conversa anterior, revisão de padrões ou plano de reflexão. Não registrar temas íntimos automaticamente. Se não houver memória autorizada ou contexto anterior, dizer que não sabe em vez de criar histórico.

## Quick Reference

Referência: `references/modelo-resumo.md`. Priorizar resumo **apenas na resposta**, sem gravação. Separar fatos narrados, emoções que a pessoa nomeou, hipóteses, perguntas em aberto e possibilidades voluntárias.

## Procedure

1. Confirme o escopo no pedido atual: síntese desta conversa, comparação de sessões fornecidas, ou pedido explícito de salvar. Se faltar acesso aos registros, diga não sei e peça apenas o material estritamente necessário.
2. Sintetize apenas o que está disponível. Não invente lembranças nem estados emocionais, rótulos clínicos, diagnósticos ou progresso medido.
3. Estruture brevemente: **O que foi dito; O que foi sentido (quando nomeado); Tensões/necessidades; Hipóteses abertas; Escolha/questão a explorar.** Só use categorias pertinentes.
4. Se um padrão aparecer em múltiplos relatos, indique fonte e grau de certeza: 'Nestas duas conversas você mencionou...' e convide a revisar. Não transformar recorrência em personalidade fixa.
5. Para gravação persistente, pergunte previamente **o quê, onde, por quanto tempo e com que finalidade**. Use ferramenta de escrita apenas após autorização explícita e se existir. Permita revisar/retificar o resumo antes de gravar. Não afirme segurança/eliminação de logs que não controla.
6. Se o usuário quiser revisitar no futuro, produza resumo minimizado para ser **salvo pelo próprio usuário** ou, somente com autorização e ferramenta adequada, salve no destino escolhido. Não crie automações de acompanhamento por conta própria.
7. Termine sem cobrança, metas obrigatórias ou promessa de cura. Preserve abertura e autonomia.

## Safety, always on

- Conteúdo de saúde mental sensível exige minimização. Sem sincronizar, enviar, pesquisar terceiros, gravar, ou compartilhar sem consentimento explícito.
- Não emitir avaliação clínica, conclusão de risco a partir de texto parcial ou diagnóstico. IA não substitui profissional de saúde mental.
- Se aparecer risco de suicídio, automutilação ou violência iminente, interromper síntese para priorizar segurança, apoio humano e serviço emergencial. No Brasil, SAMU 192; CVV 188 para escuta.
- Não prometer confidencialidade profissional ou ausência de logs, e não acessar dados de perfis distintos sem autorização.

## Pitfalls

- Guardar dados íntimos só porque o usuário pediu resumo: **resumir não é autorização para persistir**.
- Converter hipótese em verdade ou atribuir intenção a terceiros: corrigir linguagem.
- Simular continuidade sem acesso à conversa anterior: informar limitação.
- Gerar métricas de 'melhora' ou 'tratamento': não quantificar sem fonte/metodologia real, e nunca chamar de desfecho clínico.

## Verification

Os fatos vieram da conversa? Todas as hipóteses estão marcadas? Há consentimento específico para qualquer gravação? O resumo é útil, breve e não clínico? Nenhuma ação externa foi simulada?

## Fontes e pré-requisitos do segundo cérebro
- Usar o contexto atual por padrão. Só consultar histórico quando explicitamente solicitado ou realmente necessário.
- Se indispensável e autorizado, localizar a fonte pertinente em `/srv/hermes/base/MAPA-MEMORIAS.md`; não varrer memórias ou dados clínicos.
- Confirmar existência, permissões e atualidade. Se faltarem, dizer que não foi possível comparar.
- Nunca presumir que o texto de uma skill contenha dados pessoais.

## Persistência somente mediante autorização
Caso haja pedido de registro, apresentar conteúdo e destino propostos, obter aprovação específica e confirmar acesso à escrita antes de qualquer mudança.
Não editar `config/memorias/`, `saude/` ou `rascunhos/` automaticamente.

## Verificação adicional
- Nenhuma memória inventada, nenhuma conclusão clínica, nenhum dado gravado por padrão.
