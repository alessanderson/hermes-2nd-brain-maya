---
name: bioimpedancia-relatorio
description: Use quando o usuário pedir relatório, dashboard, gráfico, PDF ou PNG da evolução das bioimpedâncias. Trabalha só com o CSV já armazenado; não lê laudos nem altera dados.
version: 2.0.0
author: Alessanderson
license: MIT
metadata:
  hermes:
    tags: [bioimpedancia, relatorio, dashboard, graficos, csv, pessoal]
    related_skills: [bioimpedancia-ingestao, composicao-corporal-analise]
---

# Relatório de bioimpedância (dashboard)

## Overview

Gera o dashboard de uma página (PDF + PNG) a partir de `bioimpedancias/bioimpedancias.csv`. Caminhos em `/srv/hermes/saude/README.md`.

O layout está **implementado no script** `scripts/gerar_dashboard.py` desta skill. A skill não descreve pixel a pixel: quem manda é o script. Para mudar o visual, altere o script (e esta seção "Layout" se o conteúdo mudar), nunca recrie do zero a cada uso.

Imagem de referência do padrão visual: `assets/referencia-dashboard.png` (colocar aqui a imagem original fornecida pelo usuário).

## When to Use

- Pedido de relatório, dashboard, gráfico, PDF, PNG ou "como estou evoluindo" em formato visual.
- Depois de `bioimpedancia-ingestao` inserir exame **e** o usuário pedir o relatório atualizado.

Não use para:
- Ler laudo/foto → `bioimpedancia-ingestao`.
- Interpretação em texto → `composicao-corporal-analise`.

## Layout (resumo do que o script gera)

1. Cabeçalho azul-escuro com título e caixa "Período dos exames" (primeira → última data, nº de exames únicos), mais a linha "Fonte dos dados".
2. **Status atual**: 6 cards (Peso, Gordura, PGC, Músculo, Visceral, InBody) com valor e Δ desde o primeiro exame. A cor do Δ depende da direção favorável: gordura, PGC, visceral e peso caindo = verde; músculo e InBody subindo = verde; o contrário = vermelho.
3. **Indicadores vs faixas desejadas**: 6 gauges (PGC, IMC, visceral, RCQ, massa de gordura, MME) com status `DENTRO` / `ACIMA` / `ABAIXO`. A cor do status também respeita a direção: MME acima da faixa é favorável (verde), não alerta.
4. **Evolução**: 9 gráficos de linha separados (Peso, Gordura, Músculo, PGC, Visceral, IMC, RCQ, InBody, TMB), com rótulos nos pontos e eixos automáticos com folga, mais os cards de referências, legenda e observação.
5. Nota fixa: "Faixas desejadas são referências visuais para acompanhamento, não diagnóstico."

Faixas desejadas (editáveis no topo do script, constante `FAIXAS`): PGC 10–20 %; IMC 18,5–25; visceral 1–10; RCQ 0,80–0,90; massa de gordura 8,6–17,1 kg; MME 30,6–37,4 kg (faixas "normais" do laudo InBody para a altura/peso atuais; revisar se o peso mudar muito).

## Workflow

1. **Executar**

   ```bash
   /srv/hermes/.venv/bin/python /srv/hermes/skills/saude/bioimpedancia-relatorio/scripts/gerar_dashboard.py
   ```

   Sem venv/matplotlib: `python3 -m venv /srv/hermes/.venv && /srv/hermes/.venv/bin/pip install matplotlib`.

   O script lê o CSV, ordena por data e ignora duplicatas **em memória** (não altera o CSV). Grava em `bioimpedancias/relatorios/dashboard_AAAA-MM-DD.pdf` e `.png` (data do último exame; regerar sobrescreve) e imprime os caminhos.

2. **Verificar**
   - Arquivos existem e têm tamanho > 0.
   - Se o script foi alterado: usar `vision_analyze` no PNG e reprovar qualquer texto sobreposto, cortado ou ilegível. Corrigir o script e gerar de novo.

3. **Entregar**
   - `MEDIA:/caminho/do/arquivo.pdf` e/ou `.png`.
   - Uma frase com a quantidade de exames e o período. Sem reexplicar os números.

## Common Pitfalls

1. **Recriar o script do zero.** Ele está versionado nesta skill; corrigir em vez de reescrever.
2. **Alterar o CSV.** Este relatório é somente leitura.
3. **Pintar músculo acima da faixa como alerta.** A cor segue a direção favorável.
4. **Misturar % de gordura do InBody com o da Marinha** no mesmo gráfico.
5. **Parecer diagnóstico.** Usar "referência visual" e "acompanhamento".

## Verification Checklist

- [ ] Script executado sem erro; PDF e PNG gerados com tamanho > 0.
- [ ] Período e nº de exames batem com o CSV.
- [ ] Se o layout mudou, PNG validado visualmente sem sobreposição.
- [ ] Resposta entrega `MEDIA:` e não altera dados.
