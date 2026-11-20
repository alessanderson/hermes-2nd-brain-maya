---
name: interpretacao-bioimpedancia
description: Lê, explica e registra laudos de bioimpedância (InBody).
version: 1.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [bioimpedancia, inbody, ocr, saude, acompanhamento]
    related_skills: [biometric-tracking, relatorio-bioimpedancia, calculos-corporais]
---

# Interpretação de Bioimpedância / InBody

## Quando usar
Imagem, PDF ou print de laudo com pedido de leitura, extração, interpretação ou comparação. Não ativar armazenamento ou visualizações apenas porque um laudo foi enviado. Para série já registrada e relatório solicitado, usar `relatorio-bioimpedancia`.

## Procedimento
1. Identificar o objetivo e extrair **somente os campos necessários**. Usar visão/OCR disponível; ampliar a região relevante se houver dúvida. Não exigir todas as seções, QR, tabela ou schema fixo. Para extração integral explicitamente pedida, consultar `references/campos-e-qualidade.md`.
2. Preservar valor, unidade, data/hora e método/equipamento quando informados. Diferenciar PGC (%) de gordura (kg), massa magra de músculo esquelético e lados conforme rótulos. Não inferir identificação pessoal nem coletar ID/QR sem necessidade.
3. Não completar números por plausibilidade. Marcar ilegível, incompleto ou inconclusivo; pedir recorte só quando indispensável. Distinguir campos ausentes de zero.
4. **Manuscritos:** preservar anotações relevantes como observação separada, com origem manual e incerteza. Se divergirem do impresso, mostrar ambos e pedir confirmação quando necessário; não descartar nem substituir silenciosamente. Não tomar manuscrito por medição do aparelho. Ao registrar, transcrever em `anotacoes_manuscritas`.
5. Comparar histórico apenas quando pedido, usando a série real autorizada; a série fica em `/srv/hermes/saude/bioimpedancia/bioimpedancias.csv` (colunas em `DICIONARIO.md`, regras de dados no `README.md` da mesma pasta). Verificar existência e acesso. Não varrer toda a saúde. Histórico embutido em laudo é fonte secundária, não prova de acesso aos originais.
6. Separar valores lidos, deltas calculados com ferramenta e interpretação informativa. Métodos diferentes não formam uma única série comparável. Hidratação, horário e protocolo podem explicar flutuações; não concluir ganho/perda de gordura apenas por uma oscilação.
7. **Persistir somente com pedido/autorização específica**, com uma exceção permanente: **laudo InBody enviado pelo usuário** já tem autorização para arquivar o original e registrar na série (ver `/srv/hermes/config/memorias/preferencias.md`). Nesse caso, responder só que o exame foi processado (ou que era duplicata/conflito); mostrar valores ou interpretação apenas se pedido. Outros documentos e correções seguem a regra geral.
   Como registrar:
   1. Copiar o original para `/srv/hermes/saude/bioimpedancia/laudos/AAAA-MM-DD_HHMM.<ext>` (sem hora impressa: `AAAA-MM-DD.<ext>`; nunca inventar hora).
   2. Montar um JSON só com colunas existentes no CSV; campos não visíveis ficam vazios, com motivo em `status_observacoes`.
   3. Rodar `python3 /srv/hermes/skills/saude/interpretacao-bioimpedancia/scripts/bioimpedancia.py inserir --json <arquivo>`. Ele deduplica pela `data_hora`, confere a consistência (soma dos componentes, PGC, IMC, massa livre de gordura, TMB), marca `possível_erro` e ordena.
   4. Tratar a saída: `INSERIDO`; `DUPLICATA` (nada gravado); `CONFLITO` (nada gravado: **sempre** perguntar ao usuário); `ALERTA` (reconferir o campo na imagem). Nunca corrigir valor automaticamente.
   5. Acrescentar uma linha em `/srv/hermes/saude/bioimpedancia/processamento.md` e reler a linha gravada no CSV.
   Não criar outros artefatos, nem gerar gráfico por conta própria.
8. Entregar o resultado no formato e tamanho pedidos, sem dados identificadores desnecessários. Armazenar não autoriza gerar gráficos; carregar `relatorio-bioimpedancia` apenas se houver pedido visual.

## Segurança e verificação
IA informativa, não profissional habilitado; não diagnosticar, prescrever dieta, tratamento ou medicação. Faixas do laudo são referências do equipamento, não metas pessoais universais; indicar validação profissional quando pertinente.
Antes de responder: escopo mínimo atendido? Fontes e unidades claras? Impresso, manuscrito e cálculo separados? Lacunas e duplicatas honestas? Nenhum dado inventado, registro ou gráfico não autorizado?
