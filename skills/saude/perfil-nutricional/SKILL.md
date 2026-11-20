---
name: perfil-nutricional
description: Use para coletar ou atualizar o perfil nutricional do usuário (objetivo, metas, restrições, intolerâncias, rotina, treino, suplementos) no PERFIL.md, ou quando outra skill de saúde precisar de um dado do perfil que está faltando.
version: 1.0.0
author: Alessanderson
license: MIT
metadata:
  hermes:
    tags: [perfil, anamnese, metas, restricoes, nutricao, pessoal]
    related_skills: [receitas, plano-alimentar, checkin-semanal, calculos-corporais]
---

# Perfil nutricional

## Overview

Mantém `PERFIL.md` (caminho em `/srv/hermes/saude/README.md`): a base que torna receitas, plano alimentar e check-ins personalizados. É a "coleta inicial" de que as outras skills dependem.

## When to Use

- `PERFIL.md` tem campos essenciais com `a preencher` e uma skill precisa deles.
- Usuário informa mudança: nova meta, nova restrição, mudou o treino, começou/parou um suplemento.
- Usuário pede "vamos montar meu perfil" ou "atualiza minha meta".

## Workflow

1. **Ler `PERFIL.md`** e listar o que falta, em ordem de prioridade:
   1. Intolerâncias/alergias (segurança).
   2. Objetivo principal e meta.
   3. Nível de atividade e treino.
   4. Rotina de refeições e tempo para cozinhar.
   5. Preferências, aversões, orçamento.
   6. Suplementos atuais.
2. **Perguntar uma coisa por vez**, de forma conversacional. Não despejar um questionário.
3. **Gravar** cada resposta no campo certo, substituindo `a preencher`. Atualizar `atualizado_em` no frontmatter.
4. **Registrar no histórico** do fim do arquivo: `- AAAA-MM-DD: <o que mudou>`.
5. **Metas calóricas**: quando o objetivo e a atividade estiverem definidos, calcular com `calculos-corporais` (TMB da regra 7 do README → TDEE → ajuste) e **propor** os números. Só gravar como meta após o usuário confirmar.

## Regras

- Nunca preencher por suposição; o que o usuário não disse continua `a preencher`.
- Restrição e intolerância são bloqueios absolutos para as outras skills.
- Dados básicos (altura, idade, sexo) podem vir do InBody mais recente, citando a data.

## Verification Checklist

- [ ] Só dados ditos pelo usuário (ou do InBody, com data).
- [ ] Uma pergunta por vez.
- [ ] `atualizado_em` e histórico atualizados.
- [ ] Meta calórica gravada só após confirmação.
