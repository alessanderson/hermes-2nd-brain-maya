---
name: exames-laboratoriais
description: Use quando o usuário compartilhar exames de sangue ou laboratoriais (PDF, foto ou valores) para registrar na base histórica e analisar sob a ótica nutricional e de performance, comparando com exames anteriores.
version: 2.0.0
author: Alessanderson
license: MIT
metadata:
  hermes:
    tags: [exames, laboratorio, sangue, marcadores, nutricao, pessoal]
    related_skills: [plano-alimentar, composicao-corporal-analise]
---

# Exames laboratoriais

## Overview

Registra exames em `exames-laboratoriais/exames.csv` (formato longo: uma linha por marcador) e analisa do ponto de vista nutricional e de performance. Caminhos e regras de dados em `/srv/hermes/saude/README.md`.

**Não é diagnóstico.** Valor alterado ou combinação preocupante → orientar avaliação médica, sem alarmismo.

## When to Use

- Usuário enviou laudo de exame de sangue/urina ou digitou valores.
- "Como estão meus exames?", "minha vitamina D melhorou?".

## Workflow

1. **Extrair** só o que está impresso: marcador, valor, unidade e faixa de referência **do próprio laudo** (as faixas variam por laboratório e método). Ignorar anotações à caneta.
2. **Arquivar** o laudo em `exames-laboratoriais/laudos/AAAA-MM-DD_laboratorio.<ext>`.
3. **Gravar** no CSV: `data_coleta` (`YYYY-MM-DD`), `marcador` (nome padronizado, ex.: `vitamina_d_25oh`, `hba1c`, `ldl`), `valor`, `unidade`, `ref_min`, `ref_max`, `ref_texto` (quando a referência não é um intervalo simples), `laboratorio`, `arquivo_laudo`, `status_observacoes`. Antes de gravar, conferir se `data_coleta + marcador` já existe: igual → duplicata, diferente → conflito para o usuário decidir.
4. **Analisar** os marcadores de interesse, para cada um:
   1. Resultado × referência do laudo.
   2. Comparação com exames anteriores do CSV (tendência).
   3. O que significa para o objetivo do usuário.
   4. Ajuste nutricional ou de suplementação, se pertinente → detalhar via `plano-alimentar`.
   5. Quando procurar avaliação médica.

## Marcadores de interesse

- Glicose + HbA1c: controle glicêmico.
- Lipidograma completo: saúde cardiovascular.
- Hemograma: energia, imunidade, recuperação.
- Ferritina + ferro: transporte de oxigênio.
- Vitamina D (25-OH): força, imunidade, humor.
- TSH + T4 livre: metabolismo.
- Testosterona total + livre: contexto hormonal da recomposição.
- TGO + TGP: fígado.
- Creatinina + TFG: rins (a creatinina tende a ser mais alta em quem tem mais massa muscular ou usa creatina; considerar antes de alarmar).
- PCR ultrassensível: inflamação.

## Common Pitfalls

1. Usar faixa de referência genérica em vez da do laudo.
2. Comparar valores em unidades diferentes sem converter.
3. Diagnosticar ou sugerir medicamento.
4. Ignorar o contexto (jejum, treino intenso na véspera, suplementos).

## Verification Checklist

- [ ] Todos os marcadores impressos gravados, com unidade e referência do laudo.
- [ ] Laudo arquivado e caminho no CSV.
- [ ] Comparação histórica feita quando há exame anterior.
- [ ] Sem diagnóstico nem prescrição; avaliação médica indicada quando cabível.
