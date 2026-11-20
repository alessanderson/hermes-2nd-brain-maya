---
name: plano-alimentar
description: Use quando o usuário pedir um plano alimentar (dia ou semana), distribuição de macros por refeição, ajuste do plano após check-in, ou avaliação/recomendação de suplementação.
version: 1.0.0
author: Alessanderson
license: MIT
metadata:
  hermes:
    tags: [nutricao, plano-alimentar, macros, suplementacao, recomposicao-corporal, pessoal]
    related_skills: [perfil-nutricional, calculos-corporais, receitas, checkin-semanal, exames-laboratoriais]
---

# Plano alimentar e suplementação

## Overview

Monta e ajusta o plano alimentar e avalia suplementos com base em `PERFIL.md`, na composição corporal recente e nos exames laboratoriais. Caminhos em `/srv/hermes/saude/README.md`.

Isto é acompanhamento nutricional e de performance, **não substitui nutricionista ou médico**.

## When to Use

- "Monta meu plano", "como distribuo as refeições", "quanto de proteína no jantar".
- Ajuste proposto pelo `checkin-semanal`.
- "Devo tomar creatina/whey/vitamina D?", revisão da suplementação.

Não use para: receita de uma refeição (`receitas`), interpretação de exame de sangue (`exames-laboratoriais`).

## Pré-requisitos

- Objetivo, nível de atividade e intolerâncias preenchidos no `PERFIL.md`. Faltando → `perfil-nutricional` antes.
- Meta calórica e proteica: do `PERFIL.md`; se não houver, calcular com `calculos-corporais` e propor.

## Estrutura do plano

- Proteína distribuída em todas as refeições.
- Carboidratos concentrados perto do treino, reduzindo ao longo do dia quando combinar com a rotina.
- Gordura de qualidade em pelo menos 3 refeições.
- Hidratação de referência 2,5–3,5 L/dia, ajustada a peso, treino e clima.
- Timing:
  - Pré-treino: carboidrato de médio/baixo índice glicêmico.
  - Pós-treino: proteína + carboidrato.
  - Jantar: proteína + vegetais + gordura boa; carboidrato conforme objetivo e treino.
  - Pré-sono: proteína de absorção lenta, se fizer sentido.
- Priorizar alimentos integrais e minimamente processados; usar `receitas` para detalhar refeições.
- Totais do plano somados por ferramenta e apresentados como aproximados.

## Ajustes após check-in

- Proporcionais aos dados; intervenção mínima efetiva.
- Mudar uma variável por vez (calorias **ou** distribuição **ou** cardio) para saber o que funcionou.
- Considerar a aderência: plano ótimo que não se cumpre é plano ruim.

## Suplementação

Para cada suplemento atual ou sugerido:

1. Justificativa ligada ao objetivo ou a um gap (dieta ou exame laboratorial).
2. Nível de evidência e custo-benefício.
3. Segurança, contraindicações e quando precisa de acompanhamento profissional.

Questionar suplemento sem evidência robusta. Nunca recomendar sem justificativa clara, nunca prescrever medicamento, nunca sugerir substância experimental ou sem aprovação regulatória. Mudanças aceitas pelo usuário → atualizar a seção de suplementação do `PERFIL.md`.

## Verification Checklist

- [ ] `PERFIL.md` consultado; restrições respeitadas.
- [ ] Metas calculadas por ferramenta e confirmadas.
- [ ] Ajustes proporcionais e executáveis.
- [ ] Suplementos com justificativa e ressalvas; sem prescrição.
