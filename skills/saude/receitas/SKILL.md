---
name: receitas
description: Use quando o usuário pedir uma receita ou ideia de refeição (café, lanche, almoço, jantar, ceia, marmita, congelável, aproveitamento de sobras), inclusive para encaixar nas calorias e proteína que restam no dia.
version: 2.0.0
author: Alessanderson
license: MIT
metadata:
  hermes:
    tags: [nutricao, receitas, refeicao, marmita, brasil, pessoal]
    related_skills: [perfil-nutricional, plano-alimentar, calculos-corporais]
---

# Receitas personalizadas

## Overview

Cria receitas simples, baratas e personalizadas para o dia real do usuário. Restrições, metas e preferências vêm de `PERFIL.md` (caminho em `/srv/hermes/saude/README.md`).

Nunca gerar receita genérica quando houver dados para personalizar. Valores nutricionais são estimativas: `aprox. 450 kcal`, nunca `447,36 kcal`.

## When to Use

- Receita para uma refeição específica, rápida, barata, marmita, congelável ou com sobras.
- "Restam X kcal e Y g de proteína, o que eu como?"
- Ajustar porção de uma receita a uma meta.

Não use para: montar o plano alimentar do dia/semana (`plano-alimentar`), diagnóstico ou orientação clínica.

## Antes de criar

Ler `PERFIL.md` e considerar, quando houver:

1. Calorias e proteína disponíveis para a refeição.
2. Qual refeição do dia.
3. Intolerâncias/alergias e restrições → **bloqueio absoluto**.
4. Preferências e aversões.
5. Alimentos que o usuário disse ter em casa.
6. Tempo disponível e orçamento.

Faltou dado não crítico → assumir algo seguro e dizer em uma linha. Só perguntar se a falta impedir uma receita segura. Se faltarem intolerâncias no perfil, perguntar uma vez e sugerir `perfil-nutricional`.

## Encaixe no restante do dia

1. Mirar ±10 % das calorias restantes e a proteína restante (ex.: restam 500 kcal/40 g → 450–550 kcal e 35–45 g).
2. Priorizar proteína sem estourar calorias.
3. Preferir porção realista a encaixe exato; explicar o pequeno desvio.
4. Somas e ajustes de porção por ferramenta, não de cabeça.

## Características

Priorizar: ingredientes baratos e comuns no Brasil, poucas etapas, pouca louça, boa proteína, porções realistas, alimentos de que o usuário gosta.

Substituições baratas (só quando agregarem): salmão → sardinha/atum/frango; iogurte grego → natural + whey ou leite em pó; castanhas → amendoim; queijo caro → cottage/ricota/minas/ovo; peito de peru → frango desfiado/ovos; frutas vermelhas → banana/mamão/maçã/fruta da estação.

## Formato obrigatório

```text
Nome da receita

Porção:
Calorias: aprox.
Proteínas: aprox.
Carboidratos: aprox.
Gorduras: aprox.
Tempo:
Custo: baixo | médio | alto

Ingredientes:
- quantidade + ingrediente

Preparo:
1. passo

Boa para: café da manhã / almoço / jantar / lanche / ceia
```

Arredondar kcal para 10 e macros para 1–5 g. Se o valor depender de marca ou quantidade, dizer isso em uma frase após o preparo.

## Exemplo

```text
Omelete de frango com aveia

Porção: 1 refeição
Calorias: aprox. 430 kcal
Proteínas: aprox. 42 g
Carboidratos: aprox. 28 g
Gorduras: aprox. 16 g
Tempo: 12 min
Custo: baixo

Ingredientes:
- 2 ovos
- 100 g de frango desfiado
- 30 g de aveia
- 1 tomate picado
- sal, pimenta e cheiro-verde a gosto

Preparo:
1. Bata os ovos com a aveia, sal e pimenta.
2. Misture o frango e o tomate.
3. Leve à frigideira antiaderente até firmar dos dois lados.

Boa para: café da manhã / almoço / jantar / lanche
```

## Common Pitfalls

1. Receita genérica havendo dados no perfil.
2. Falsa precisão nutricional.
3. Ignorar intolerância/restrição.
4. Ingrediente caro sem motivo.
5. Muitas etapas ou panelas.
6. Forçar encaixe exato com porção estranha.

## Verification Checklist

- [ ] `PERFIL.md` consultado; restrições e intolerâncias respeitadas.
- [ ] Calorias/proteína restantes consideradas quando informadas.
- [ ] Valores arredondados e marcados como aproximados.
- [ ] Formato obrigatório seguido, terminando em `Boa para: ...`.
