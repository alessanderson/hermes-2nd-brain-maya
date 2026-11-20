---
name: composicao-corporal-analise
description: Use quando o usuário perguntar como está, pedir interpretação ou comparação da composição corporal (gordura, músculo, visceral, peso, medidas) ao longo do tempo, usando a base de bioimpedâncias e os check-ins. Resposta em texto, sem gráficos.
version: 1.0.0
author: Alessanderson
license: MIT
metadata:
  hermes:
    tags: [composicao-corporal, bioimpedancia, evolucao, analise, pessoal]
    related_skills: [bioimpedancia-ingestao, bioimpedancia-relatorio, checkin-semanal, calculos-corporais]
---

# Análise de composição corporal

## Overview

Interpreta os dados **já armazenados** (bioimpedâncias, check-ins e metas do `PERFIL.md`). Não lê laudos e não grava em bases. Caminhos em `/srv/hermes/saude/README.md`.

## When to Use

- "Como estou?", "melhorei?", "o que mudou desde o último exame?", "explica esse resultado".
- Depois de uma ingestão, **se** o usuário pedir interpretação.
- Como etapa de análise do `checkin-semanal`.

Não use para: extrair laudo (`bioimpedancia-ingestao`), gráficos (`bioimpedancia-relatorio`), exame de sangue (`exames-laboratoriais`).

## Workflow

1. **Carregar dados**: CSV de bioimpedância (ordenado por data), `checkins/checkins.csv` e metas do `PERFIL.md`.
2. **Comparar** (cálculos por script ou Python, nunca de cabeça):
   - Último exame × anterior × primeiro.
   - Variação absoluta e por semana entre exames.
   - Respeitar `status_observacoes`: valor com `baixa_confiança` ou `possível_erro` entra com ressalva.
   - Altura diferente entre exames (178 × 180 cm) afeta IMC e SMI: avisar quando comparar esses dois indicadores.
3. **Interpretar em conjunto (80/20)**, nunca um indicador isolado:
   - Massa de gordura e PGC (o principal).
   - MME (preservação muscular).
   - Gordura visceral e RCQ (risco).
   - Peso e IMC (contexto).
   - Padrões: peso caindo com MME estável = perda de gordura de qualidade; peso estável com cintura caindo = recomposição; peso caindo com MME caindo = revisar proteína/treino/déficit.
4. **Comparar com metas** do `PERFIL.md`, se existirem. Projeção de quando chega na meta só com pelo menos 3 pontos e avisando que é linear e aproximada.
5. **Responder** curto: o que melhorou, o que precisa de atenção e um próximo passo prático. Separar fatos (números) de interpretação.

## Common Pitfalls

1. **Diagnosticar.** Usar "sugere", "indica no laudo". Risco clínico aparente → profissional de saúde.
2. **Usar o peso como métrica principal.**
3. **Misturar séries** (InBody × Marinha).
4. **Ignorar a qualidade do dado** marcada em `status_observacoes`.
5. **Dizer só o que o usuário quer ouvir.** Os dados mandam.

## Verification Checklist

- [ ] Dados lidos das bases, não da memória da conversa.
- [ ] Comparações calculadas por ferramenta.
- [ ] Ressalvas de qualidade e de altura mencionadas quando relevantes.
- [ ] Fatos separados de interpretação; sem diagnóstico.
