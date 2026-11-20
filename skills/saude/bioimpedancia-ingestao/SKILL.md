---
name: bioimpedancia-ingestao
description: Use quando o usuário enviar foto, print ou PDF de laudo de bioimpedância (InBody, Tanita, Omron) para extrair os dados impressos e gravar na base histórica. Não interpreta nem gera gráficos.
version: 2.0.0
author: Alessanderson
license: MIT
metadata:
  hermes:
    tags: [bioimpedancia, inbody, ocr, extracao, csv, pessoal]
    related_skills: [composicao-corporal-analise, bioimpedancia-relatorio]
---

# Ingestão de bioimpedância

## Overview

Transforma um laudo visual em **uma linha auditável** no CSV de bioimpedâncias. Só extrai, valida e grava.

Caminhos, regras de duplicidade e formato: ler `/srv/hermes/saude/README.md` antes de começar. O significado de cada coluna está em `bioimpedancias/DICIONARIO.md`.

## When to Use

- Usuário enviou imagem, print ou PDF de bioimpedância (um ou vários).
- Usuário pediu para "guardar", "registrar" ou "processar" um exame.

Não use para:
- Interpretar ou comparar resultados → `composicao-corporal-analise`.
- Gráficos, dashboard, PDF → `bioimpedancia-relatorio`.
- Exame de sangue → `exames-laboratoriais`.

## Modos de resposta

| Modo | Quando | Resposta ao usuário |
|---|---|---|
| **Silencioso (padrão)** | Usuário só enviou o laudo | Uma frase: "Exame de DD/MM/AAAA HH:MM processado e armazenado." (ou "já estava na base" / "conflito: ..."). Não mostrar valores. |
| **Tabela** | Usuário pediu explicitamente os dados extraídos | Tabela por seção do laudo, na ordem impressa, com unidades e faixas de referência entre parênteses. |

Se o usuário pedir interpretação junto, terminar a ingestão e passar para `composicao-corporal-analise`.

## Workflow

1. **Ler o laudo**
   - Usar visão/OCR. Se a imagem estiver rotacionada, ler considerando a rotação e marcar `baixa_confiança` nos campos incertos.
   - Ignorar sempre escritos, setas, círculos e rasuras à caneta. Só dado impresso.
   - Tentar decodificar o QR code com ferramenta local; se falhar, registrar "QR não decodificado".
   - Ler de cima para baixo e da esquerda para a direita, seção por seção, respeitando esquerda/direita impressos no desenho corporal.
   - Concluído quando todos os blocos impressos visíveis foram inspecionados.

2. **Montar o registro**
   - Montar um JSON com as colunas do schema (lista em `DICIONARIO.md` ou no cabeçalho do CSV). Nunca criar coluna nova se o dado couber no schema.
   - Campo não visível → vazio + motivo em `status_observacoes`.
   - Rótulos de qualidade em `status_observacoes`, separados por `;`: `OK`, `baixa_confiança`, `ilegível`, `incompleto`, `inconclusivo`, `possível_erro: <detalhe>`.

3. **Arquivar o laudo original**
   - Copiar a imagem/PDF para `bioimpedancias/laudos/AAAA-MM-DD_HHMM.<ext>` (data e hora do exame).
   - Gravar esse caminho em `fonte_imagem`. Nunca deixar apontando para o cache do Hermes.
   - Em lote com a mesma foto repetida, arquivar a mais legível.

4. **Inserir com o script** (deduplica, valida e ordena sozinho)

   ```bash
   python3 /srv/hermes/skills/saude/bioimpedancia-ingestao/scripts/bioimpedancia.py inserir --json /tmp/exame.json
   ```

   Saídas possíveis:
   - `INSERIDO` → exame novo gravado, CSV reordenado por data.
   - `DUPLICATA` → mesma data_hora e mesmos valores-chave; nada foi gravado.
   - `CONFLITO` → mesma data_hora com valores diferentes; nada foi gravado. **Avisar o usuário** e perguntar qual leitura vale.
   - `ALERTAS` → verificações de consistência (soma dos componentes, PGC, IMC, massa livre de gordura, TMB) que falharam. O script já acrescenta `possível_erro` em `status_observacoes`. Reconferir esses campos na imagem antes de responder.

5. **Registrar no log**
   - Acrescentar uma linha em `bioimpedancias/processamento.md` para cada exame: inserido, duplicata, conflito ou alerta.

6. **Responder** conforme o modo (silencioso por padrão).

## Common Pitfalls

1. **Inventar valor ilegível.** Nunca completar por plausibilidade.
2. **Usar anotação à caneta como dado.**
3. **Confundir `pgc_percentual` (%) com `massa_gordura_kg` (kg).**
4. **Trocar esquerda/direita** no desenho segmentar.
5. **Ler `..._percentual` segmentar como % de gordura do membro.** É % em relação ao padrão do aparelho.
6. **Gravar sem o script.** Editar o CSV à mão pula a deduplicação e a validação.
7. **Resolver conflito sozinho.** Conflito sempre volta para o usuário.
8. **Mostrar os dados sem pedido.** O padrão é silencioso.

## Verification Checklist

- [ ] Escritos à caneta foram ignorados.
- [ ] Todo dado impresso visível está no JSON ou justificado em `status_observacoes`.
- [ ] Laudo arquivado em `bioimpedancias/laudos/` e caminho em `fonte_imagem`.
- [ ] Inserção feita pelo script; resultado (INSERIDO/DUPLICATA/CONFLITO/ALERTAS) tratado.
- [ ] Log `processamento.md` atualizado.
- [ ] Resposta no modo correto, sem interpretação nem diagnóstico.
