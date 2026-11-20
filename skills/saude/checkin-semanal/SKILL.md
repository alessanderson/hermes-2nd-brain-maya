---
name: checkin-semanal
description: Use para conduzir o check-in semanal de acompanhamento (peso, medidas de fita, sono, treino, alimentação, suplementos, bem-estar), registrar na base de check-ins e analisar a semana com ajustes.
version: 1.0.0
author: Alessanderson
license: MIT
metadata:
  hermes:
    tags: [checkin, acompanhamento, medidas, semanal, pessoal]
    related_skills: [calculos-corporais, composicao-corporal-analise, plano-alimentar, perfil-nutricional]
---

# Check-in semanal

## Overview

Coleta os dados da semana, grava uma linha em `checkins/checkins.csv`, recalcula o % de gordura pela Marinha e analisa a semana. Caminhos em `/srv/hermes/saude/README.md`.

## When to Use

- Usuário diz "check-in", "fechamento da semana" ou manda peso e medidas da semana.
- Lembrete agendado de check-in.

## Workflow

1. **Coletar**, de forma conversacional e em blocos curtos (não um questionário de uma vez). Aceitar o que o usuário mandar de uma vez e perguntar só o que faltar:
   - **Biometria**: peso (manhã, jejum, após urinar), cintura, peitoral, braço relaxado, quadril, coxa, pescoço, em cm.
   - **Sono**: média de horas/noite (aceitar print do app).
   - **Treino**: treinos na semana, carga nova/recorde, dores, cardio (vezes).
   - **Alimentação**: seguiu o plano (sim/parcial/não), substituições, fome e saciedade, intestino.
   - **Suplementos**: regularidade e efeitos percebidos.
   - **Bem-estar**: energia 1–10, estresse 1–10, dor ou desconforto.
2. **Calcular** o % de gordura da Marinha com `calculos-corporais` (precisa de cintura, pescoço e altura do `PERFIL.md`). Gravar em `pgc_navy_percentual`.
3. **Gravar** uma linha em `checkins/checkins.csv` (data `YYYY-MM-DD`, decimal com ponto, campo vazio se não informado). Não duplicar a mesma data: se já existir, perguntar se substitui.
4. **Analisar** com `composicao-corporal-analise`:
   - Tabela: semana atual × anterior × início.
   - Leitura conjunta (peso subiu e cintura caiu pode ser recomposição; peso caiu com perda de força pede ajuste).
   - Incluir o último InBody se for de até 30 dias.
5. **Fechar a semana**: o que foi positivo, o que precisa de atenção e **um** ajuste prático (via `plano-alimentar` se for alimentar). Atualizar a projeção para a meta se houver meta no `PERFIL.md`.

## Common Pitfalls

1. Perguntas demais de uma vez.
2. Peso como métrica principal.
3. Ajuste radical sem motivo forte.
4. Comparar %G da Marinha com %G do InBody.
5. Medidas de horários ou condições diferentes sem avisar.

## Verification Checklist

- [ ] Linha gravada no CSV, sem duplicar data.
- [ ] %G da Marinha calculado por script.
- [ ] Comparação semana atual × anterior × início.
- [ ] Um ajuste prático e proporcional; sem diagnóstico.
