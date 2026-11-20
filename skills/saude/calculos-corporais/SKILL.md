---
name: calculos-corporais
description: Use sempre que precisar calcular percentual de gordura por medidas (método da Marinha/US Navy), massa gorda e magra, TMB (Katch-McArdle), gasto diário (TDEE) ou déficit calórico. Ferramenta de cálculo usada pelas outras skills de saúde.
version: 2.0.0
author: Alessanderson
license: MIT
metadata:
  hermes:
    tags: [calculo, gordura, tmb, tdee, us-navy, katch-mcardle, pessoal]
    related_skills: [biometric-tracking, nutrition-planning, nutricionista-pessoal]
---

# Cálculos corporais

## Overview

Ferramenta de cálculo. **Nunca calcular de cabeça:** sempre rodar o script desta skill. Calcular só quando pedido ou necessário à resposta; não recalcular nada automaticamente. Regra de fonte (InBody × Marinha, qual TMB usar): `/srv/hermes/saude/bioimpedancia/README.md`, regras 6 e 7.

## When to Use

- Check-in com medidas de fita (cintura, pescoço, quadril).
- Definir ou revisar meta calórica (TMB → TDEE → déficit/superávit).
- Qualquer conta envolvendo composição corporal.

## Script

```bash
python3 /srv/hermes/skills/saude/calculos-corporais/scripts/calculos.py \
  --sexo M --altura 180 --peso 86.1 --cintura 92 --pescoco 40 [--quadril 100] \
  [--atividade moderado] [--ajuste -500] [--massa-magra 66.5]
```

- Medidas em **centímetros** e peso em **kg**. O script recusa valores que parecem polegadas.
- `--quadril` é obrigatório só para mulher.
- `--massa-magra` (opcional) usa a massa magra do InBody em vez da estimada pela Marinha.
- `--atividade`: `sedentario`, `leve`, `moderado`, `muito`, `extremo`.
- `--ajuste`: kcal somadas ao TDEE para a meta (ex.: `-500` déficit).
- Saída em JSON com valores arredondados.

## Fórmulas (referência; quem calcula é o script)

- **Marinha (US Navy), em cm**
  - Homem: `%G = 495 / (1,0324 − 0,19077 × log10(cintura − pescoço) + 0,15456 × log10(altura)) − 450`
  - Mulher: `%G = 495 / (1,29579 − 0,35004 × log10(cintura + quadril − pescoço) + 0,22100 × log10(altura)) − 450`
- **Massa gorda** = peso × %G / 100; **massa magra** = peso − massa gorda.
- **TMB Katch-McArdle** = 370 + 21,6 × massa magra (kg). É a mesma fórmula que o InBody imprime.
- **TDEE** = TMB × fator: sedentário 1,2; leve (1–3×/sem) 1,375; moderado (3–5×/sem) 1,55; muito ativo (6–7×/sem) 1,725; extremo (2×/dia) 1,9.

## Medição (para orientar o usuário)

- Cintura: na altura do umbigo, relaxado, fim da expiração.
- Pescoço: logo abaixo da laringe, fita levemente inclinada para baixo na frente.
- Quadril (mulher): maior circunferência dos glúteos.
- Sempre no mesmo horário, de preferência manhã e em jejum.

## Common Pitfalls

1. **Medidas em polegadas** na fórmula em cm.
2. **Comparar %G da Marinha com %G do InBody** como se fosse a mesma série.
3. **TDEE com fator de atividade otimista.** Na dúvida, usar o nível abaixo.
4. **Falsa precisão.** Reportar %G com 1 casa e kcal arredondadas para dezenas.

## Verification Checklist

- [ ] Cálculo feito pelo script, não de cabeça.
- [ ] Unidades em cm e kg.
- [ ] Origem da massa magra/TMB informada (InBody ou Marinha).
