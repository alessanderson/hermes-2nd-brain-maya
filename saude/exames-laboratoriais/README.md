---
titulo: Exames laboratoriais
tipo: indice
status: ativo
tags: [saude, exames, laboratorio]
resumo: "Exames de sangue e laboratoriais: série em CSV e laudos originais"
---

# Exames laboratoriais

| Arquivo | Conteúdo |
|---|---|
| `exames.csv` | Série em formato longo: uma linha por marcador (`data_coleta, marcador, valor, unidade, ref_min, ref_max, ref_texto, laboratorio, arquivo_laudo, status_observacoes`) |
| `laudos/` | Original de cada exame, nome `AAAA-MM-DD_laboratorio.<ext>` |

Regras: gravar só com pedido ou autorização. Usar a faixa de referência **do próprio laudo**. Preservar data, unidade e fonte. Chave `data_coleta + marcador`: igual = duplicata; diferente = conflito para o usuário decidir. Dados sensíveis: ficam protegidos (criptografados no Git).
