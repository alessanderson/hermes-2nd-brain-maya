---
name: preparo-para-terapia
description: Organiza relatos e perguntas para terapeuta humana.
version: 3.0.0
metadata:
  hermes:
    category: wellbeing
    tags: [terapia, terapeuta, sintese, relato]
---
# Preparo de pauta para terapeuta humana

## When to Use
Quando o usuário quer levar uma situação à terapeuta/psicóloga, transformar vivências em roteiro de fala, sintetizar uma conversa para sessão, organizar sentimentos ou formular perguntas a profissional humano. Não usar para diagnóstico, avaliação clínica ou resumo para uso próprio sem terapeuta como destinatária.

## Quick Reference
Entregar **uma versão pronta para apresentar**, em primeira pessoa e linguagem natural, separando fato narrado, sentimento nomeado, interpretação do usuário, dúvida e objetivo da conversa. Nunca transformar hipótese em fato nem decidir qual seria a opinião da terapeuta.

## Procedure
1. Identifique o destino: fala na sessão (padrão) ou mensagem escrita (se pedido). Use só informações desta mensagem/contexto acessível e autorizado; não consultar histórico automaticamente.
2. Extraia: [situação/linha do tempo], [pessoas e contexto], [o que eu disse/fiz], [o que eu senti], [pensamentos/hipóteses], [impacto], [dilema e tema que quero trabalhar]. Omita campos sem suporte; nunca complete lacunas por inferência.
3. Marque epistemicamente: "aconteceu" apenas se narrado como fato; "interpretei como" para leitura subjetiva; "não sei se" para incerteza; quando útil preserve frases literais do próprio usuário entre aspas.
4. Entregue o formato e tamanho pedidos, sem acrescentar versões, tabelas ou perguntas obrigatórias. Sem formato especificado, prefira um roteiro breve em primeira pessoa; perguntas à profissional são opcionais quando úteis. Se pedido texto para enviar, entregar mensagem natural e respeitosa, sem enviar.
5. Seja fiel aos sentimentos do usuário sem dramatizar, atribuir patologia, diagnosticar terceiros ou exigir autorresponsabilização por violência de outros. Permita ambivalências e conflitos de valores.
6. Se faltar dado essencial, inclua marcador **[confirmar]** ou uma única pergunta, sem inventar. Não perguntar detalhes íntimos que não sejam necessários.
7. Se solicitado, ofereça uma versão neutra e outra emocionalmente mais explícita; nunca invente falas, sintomas, episódios ou cronologias.
8. Não guardar, enviar ou compartilhar automaticamente. Para enviar mensagem a terceiros, exigir pedido explícito e aprovação de texto e destinatário.

## Safety
A terapeuta humana deve fazer sua própria avaliação. Não dizer o que ela concluirá nem representar síntese como laudo. Em risco imediato, priorizar apoio humano e urgência, não apenas documento. Respeitar privacidade e armazenamento mínimo.

## Pitfalls
- Misturar opinião da IA com relato do usuário: distinguir sempre.
- Fazer sessão terapêutica extensa quando foi pedido apenas roteiro: priorizar artefato solicitado.
- Dizer "você tem trauma/dependência/narcisismo": não diagnosticar.
- Resumir apagando ambiguidades: incluir contradições relevantes como dúvidas, não defeitos.

## Verification
Todos os fatos e sentimentos vieram do usuário? O texto é confortável de falar em primeira pessoa? Separou interpretações de eventos? Oferece questões úteis à psicóloga sem responder por ela? Não houve gravação nem envio?

## Fontes e pré-requisitos do segundo cérebro
Ordem obrigatória de preferência: relato atual; contexto já disponível; documentos indicados pelo usuário; fontes persistentes específicas, apenas se indispensáveis e autorizadas.
Para localizar fonte persistente indispensável e autorizada, consultar `/srv/hermes/base/MAPA-MEMORIAS.md` e somente o arquivo pertinente. Verificar existência, acesso e atualidade.
Não ler exames e demais dados clínicos por padrão. Não presumir conteúdo ou permissões.

## Template sob demanda
Se estiver preparando roteiro de sessão, carregar `templates/roteiro-sessao.md` com `skill_view(name="preparo-para-terapia", file_path="templates/roteiro-sessao.md")` somente quando necessário e disponível.
Não abrir o template para simples perguntas sobre a skill.

## Persistência e entrega
A resposta é apresentada primeiro no chat. Nenhum rascunho, memória, mensagem ou arquivo será criado/sobrescrito/enviado sem autorização específica sobre conteúdo e destino.
Para consultas retrospectivas, citar internamente a origem dos fatos no texto e informar quando o histórico não estiver disponível.
