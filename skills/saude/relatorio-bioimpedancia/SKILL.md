---
name: relatorio-bioimpedancia
description: Gera relatórios da série biométrica real autorizada.
version: 1.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [bioimpedancia, relatorio, dashboard, graficos]
    related_skills: [interpretacao-bioimpedancia, biometric-tracking, pdf]
---

# Relatório de Bioimpedância

## Quando usar
Somente quando solicitado relatório, gráfico, dashboard ou visualização da evolução. Atualizar/armazenar dados **não é gatilho** para gerar ou regenerar gráficos. Não faz OCR de laudos nem altera registros clínicos; para extração necessária usar `interpretacao-bioimpedancia`.

## Fontes e pré-requisitos
- Usar a série **real, acessível e autorizada**: `/srv/hermes/saude/bioimpedancia/bioimpedancias.csv` (InBody) e, para cintura e US Navy, `/srv/hermes/saude/checkins/checkins.csv`. Se a localização necessária não estiver clara, consultar `/srv/hermes/base/MAPA-MEMORIAS.md` e apenas a fonte pertinente.
- Verificar existência/acesso antes de afirmar conteúdo. Gerador do dashboard: `scripts/gerar_dashboard.py` desta skill (precisa de matplotlib; venv sugerido `/srv/hermes/.venv`). Conferir se o ambiente existe antes de usar; não instalar nada sem autorização. Anexo de referência visual: `assets/` (vazio até o usuário fornecer).
- Se a fonte estiver ausente ou sem valores suficientes, informar a limitação e pedir somente os dados faltantes. Nunca inventar pontos, faixas, progresso, exames ou respostas de ferramentas.

## Procedimento
1. Delimitar métricas, período e formato solicitados. Se apenas relatório textual foi pedido, entregar texto. Não exigir PDF+PNG ou dashboard. Para pedido visual sem formato definido, escolher um único formato suportado, sem perguntar detalhes irrelevantes.
2. Ler somente a série autorizada necessária. **Converter em estrutura apenas em memória**, preservando data original, valores, unidades, fonte e método. Não exigir nem criar CSV intermediário; não migrar, reformatar ou sobrescrever a fonte. Scripts, se necessários à renderização, não devem conter a série clínica persistida.
3. Ordenar, contar e calcular com ferramenta. Verificar duplicatas pela procedência, data/método e valores disponíveis; campos incompletos não identificam um exame. Duplicatas confirmadas podem ser excluídas apenas em memória, com nota. Valores conflitantes continuam identificados, sem correção silenciosa.
4. Cobrir todo o período solicitado, ou toda a série autorizada quando não houver recorte; informar lacunas e limites. Com um exame, mostrar estado atual sem inventar tendência. Deixar ausências como lacunas, sem interpolar. Separar métodos (InBody, US Navy etc.) e não conectar séries incompatíveis. Não fabricar horário se só houver data.
5. Usar unidades e escalas legíveis. Deltas são cálculos, não medições; diferença entre percentuais em pontos percentuais. Metas/faixas somente quando fornecidas por fonte pertinente, com atribuição e limites; nunca aplicar faixas pessoais universais. Sem referência válida, omitir status/gauge ou mostrar apenas o valor.
6. Para dashboard ou reprodução visual solicitada, consultar `references/layout-dashboard.md`. Anexo só orienta reprodução quando realmente disponível; sem ele não alegar fidelidade. Adaptar layout aos dados existentes, sem preencher cards com valores fictícios.
7. Dashboard padrão: `/srv/hermes/.venv/bin/python /srv/hermes/skills/saude/relatorio-bioimpedancia/scripts/gerar_dashboard.py [--saida PASTA]`. Ele lê o CSV, ignora duplicatas só em memória, deixa lacunas sem interpolar, não inventa hora e usa apenas as faixas de referência do InBody, rotuladas como tal (ajustáveis na constante `FAIXAS`). Saída padrão: `/srv/hermes/saude/bioimpedancia/relatorios/` (fora do Git). Para outros formatos, descobrir ferramentas e bibliotecas já disponíveis. Não presumir gerador/ambiente prontos nem instalar pacotes/criar venv automaticamente. Se faltar recurso, usar alternativa instalada compatível ou informar bloqueio e pedir autorização para instalação. Gerar somente artefatos solicitados em destino de saída permitido, fora das fontes clínicas; não sobrescrever arquivos existentes sem autorização.
8. Verificar arquivo final existente/não vazio e abrir/renderizar para inspeção visual: sem sobreposição, corte ou texto ilegível. Conferir pontos, contagem e período contra a série em memória. Se não puder validar visualmente, declarar limitação, não afirmar aprovação. Para texto, verificar fatos, cálculos e escopo.
9. Entregar somente o resultado pedido, indicando fonte, número real de exames, período e limitações relevantes; usar link/`MEDIA:` apenas para arquivo realmente criado. Nenhum gráfico, segunda exportação, envio externo ou gravação de saúde adicional por padrão.

## Verificação
Série real e autorizada? Conversão só em memória? Fontes intactas? Sem pressupor venv ou anexo? Formato pedido respeitado? Métodos separados, ausências honestas e cálculos verificados? Artefato solicitado realmente validado ou bloqueio explicitado? Sem diagnóstico nem dados fabricados?
