---
titulo: Bioimpedância
tipo: indice
status: ativo
tags: [saude, bioimpedancia, inbody]
resumo: "Série de exames InBody, regras de dados e ferramentas"
---

# Bioimpedância

| Arquivo | Conteúdo |
|---|---|
| `bioimpedancias.csv` | Série de exames, uma linha por exame (fonte principal) |
| `DICIONARIO.md` | Significado, unidade e observações de cada coluna |
| `processamento.md` | Log: exames inseridos, duplicatas, conflitos e alertas |
| `laudos/` | Original de cada laudo, nome `AAAA-MM-DD_HHMM.<ext>` (ou `AAAA-MM-DD.<ext>` sem hora) |
| `relatorios/` | Painéis gerados sob pedido (fora do Git; podem ser recriados) |

## Regras de dados

1. **Só valor impresso é medição do aparelho.** Anotação manual (caneta, seta, círculo) vai em `anotacoes_manuscritas`, com a origem; nunca substitui o impresso. Se divergir, mostrar os dois e pedir confirmação.
2. **Nunca inventar nem completar por plausibilidade.** Campo ilegível ou ausente fica vazio, com o motivo em `status_observacoes`.
3. **Nunca corrigir automaticamente.** Divergência vira marcação (`possível_erro: ...`).
4. **Chave = `data_hora`.** Mesma chave e mesmos peso/PGC/MME = duplicata (não grava). Mesma chave com valores diferentes = conflito (não grava; perguntar ao usuário).
5. **Formato:** `YYYY-MM-DD HH:MM`, ou só `YYYY-MM-DD` quando a hora não foi registrada (nunca inventar hora). Decimal com ponto; unidade no nome da coluna; UTF-8 com LF.
6. **Métodos separados:** % de gordura do InBody (`pgc_percentual`) e da Marinha (`pgc_navy_percentual`, em `saude/checkins/checkins.csv`) são séries diferentes.
7. **TMB:** a do InBody já é Katch-McArdle (`370 + 21,6 × massa livre de gordura`). Sem InBody recente (até 60 dias), estimar com `calculos-corporais`.

## Ferramentas

- Inserir/validar: `python3 /srv/hermes/skills/saude/interpretacao-bioimpedancia/scripts/bioimpedancia.py inserir --json exame.json` (ou `validar`). Deduplica, confere consistência e ordena.
- Painel: `/srv/hermes/.venv/bin/python /srv/hermes/skills/saude/relatorio-bioimpedancia/scripts/gerar_dashboard.py` (só sob pedido).

## Pendências

- [ ] Laudos originais: nenhum arquivado. Os exames de 03/09 e 28/10/2026 estão incompletos (vieram de um resumo, sem hora nem equipamento). Se houver as fotos, reprocessar e completar.
- [ ] Os 9 exames de 2024–07/2026 apontam `fonte_imagem` para o cache antigo do Hermes; recuperar as imagens se ainda existirem.
- [ ] Exame de 12/06/2026: TMB marcada como `possível_erro` (1810 × 1804 calculado); conferir na imagem.
