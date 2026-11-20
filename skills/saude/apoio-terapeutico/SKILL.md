---
name: apoio-terapeutico
description: Roteia TCC, Gestalt e preparo para psicoterapia.
version: 3.1.0
metadata:
  hermes:
    category: health
    tags: [apoio, terapia, roteamento, gestalt, tcc]
---
# Roteador de apoio terapeutico

## When to Use
Ative pela linguagem natural quando o usuário pedir apoio terapêutico, uma conversa em estilo Gestalt ou TCC, ou ajuda emocional reflexiva de forma inequívoca. Exemplos: "quero conversar como numa terapia", "me ajuda com uma questão emocional", "preciso organizar isso para levar à minha psicóloga". Não ativar em perguntas de TI, trabalho técnico, escrita genérica ou mera menção incidental a emoção. Se ambíguo, responda normalmente ou faça uma pergunta curta, sem carregar outras skills.

## Quick Reference
Escolha a rota a partir da **intenção atual**, não de palavras isoladas. Carregue no máximo uma skill de execução inicialmente. Não exiba classificações internas. Não declare ser terapeuta humano nem substituir atendimento clínico.

| Pedido principal | Skill a carregar |
|---|---|
| Examinar pensamentos automáticos, interpretações, pressupostos, crenças e comportamentos pela TCC | `tcc-reflexao` |
| Explorar vivências, sentimentos e consciência da experiência presente | `gestalt-dialogo` |
| Pedir ou consentir exercício experiencial | `gestalt-experimentos` |
| Organizar acontecimentos e sentimentos, relato, pauta, roteiro ou mensagem para psicóloga humana | `preparo-para-terapia` |
| Sínteses e acompanhamento de reflexões para uso próprio, sem registro automático | `gestalt-integracao` |

## Procedure
1. Classifique silenciosamente a intenção: tcc, gestalt-dialogo, gestalt-experimento, preparo-terapeuta, integracao ou fora-do-escopo.
2. Se houver risco agudo de autoagressão, suicídio ou violência, priorize resposta de segurança e ajuda humana imediata sem iniciar exercícios ou sínteses demoradas.
3. Se o pedido for fora do escopo, não carregar módulos. Se for claramente apoio, use `skill_view` para abrir **somente** a skill correspondente, se disponível e ainda não carregada no contexto atual.
4. Execute a skill especializada no mesmo turno. A roteadora não deve provocar uma resposta adicional, duplicada ou exigir ao usuário um comando slash.
5. Se o usuário disser apenas "quero apoio terapêutico" sem pistas suficientes para distinguir TCC e Gestalt, faça uma pergunta curta sobre o tipo de exploração desejada, sem carregar as duas. Se mais de uma intenção coexistir, priorize o resultado final solicitado. Ex.: "entenda e organize para minha terapeuta" => `preparo-para-terapia`; esclareça detalhes apenas quando estritamente necessários.
6. Carregue outra skill só com mudança real de intenção ou quando um exercício foi consentido; não carregue módulos preventivamente. Nunca ler arquivos references sem demanda específica.
7. Para questionamento socrático e registro de pensamentos, use `tcc-reflexao`; para cadeira vazia e foco experiencial, use Gestalt. Evite fusão automática de técnicas.
8. Não recuperar memória, histórico, conectores, arquivos ou fazer pesquisas externas sem pedido e necessidade definidos. Não salvar dados íntimos sem autorização específica.

## Economy Rules
- Evitar ler ou imprimir lista completa de skills repetidamente.
- Manter rota ativa no turno/conversa; não reabrir `SKILL.md` desnecessariamente.
- Uma skill operacional por solicitação, salvo mudança explícita de tarefa.
- Preferir resposta de 2 a 6 frases para diálogo; para documentos à terapeuta, usar o tamanho pedido.
- Não fazer resumos retrospectivos automáticos nem carregar material que não será usado.

## Safety
IA de apoio reflexivo, não psicoterapeuta. Não diagnosticar, prescrever, afirmar confidencialidade clínica nem prometer resultado. Em risco imediato, orientar apoio humano e emergência local, no Brasil SAMU 192; CVV 188 como apoio emocional. Não afirmar sigilo técnico, retenção zero ou controle sobre logs.

## Verification
A intenção era apoio terapêutico? Só a skill necessária foi carregada? A resposta atendeu ao objetivo final sem dados inventados, ações externas ou memória não autorizadas?

## Fontes e pré-requisitos do segundo cérebro
- Usar inicialmente apenas a mensagem e o contexto atual.
- Se for indispensável localizar contexto persistente, consultar `/srv/hermes/base/MAPA-MEMORIAS.md` e apenas a fonte pertinente, com necessidade e autorização verificadas.
- Dados pessoais permanecem em `/srv/hermes/config/memorias/` e `/srv/hermes/saude/`, nunca nesta skill.
- Nunca presumir conteúdo, acesso, memória carregada, permissões ou ferramenta disponível.

## Integração e roteamento de baixo custo
- Ativar por intenção clara em linguagem natural. Descoberta automática depende de indexação/configuração do Hermes, não é garantida apenas por este arquivo.
- Usar o catálogo/resumo das skills se já estiver presente; `skill_view` somente para a skill escolhida.
- Não ler a skill roteadora de novo se suas instruções já estiverem ativas.
- Não acessar o segundo cérebro ou iniciar memória persistente por conveniência.
- Não alterar configurações do Hermes ou arquivos do workspace como efeito colateral da conversa.
