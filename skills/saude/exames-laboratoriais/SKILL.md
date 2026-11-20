---
name: exames-laboratoriais
description: Explica exames de sangue/laboratoriais sob demanda e registra na série quando autorizado.
version: 3.0.0
author: Alessanderson
license: MIT
metadata:
  hermes:
    tags: [exames, laboratorio, sangue, marcadores, saude]
    related_skills: [nutricionista-pessoal, nutrition-planning]
---

# Exames laboratoriais

## Quando usar
O usuário enviou um laudo (PDF, foto) ou digitou valores e quer entender, comparar ou guardar. Não ativar só porque um exame foi mencionado.

## Procedimento
1. **Ler só o necessário ao pedido.** Marcador, valor, unidade e faixa de referência **do próprio laudo** (variam por laboratório e método). Anotação manual fica separada, com a origem; nunca substitui o impresso. Não completar números por plausibilidade.
2. **Explicar** cada marcador pertinente: resultado × referência do laudo; o que significa para o objetivo do usuário (ótica nutricional e de performance); quando procurar avaliação médica. Considerar contexto (jejum, treino intenso na véspera, suplementos). Creatinina tende a ser mais alta em quem tem mais massa muscular ou usa creatina: considerar antes de alarmar.
3. **Comparar com exames anteriores só quando pedido**, lendo `/srv/hermes/saude/exames-laboratoriais/exames.csv`. Comparar apenas unidades e métodos compatíveis; diferenças calculadas por ferramenta.
4. **Gravar só com pedido ou autorização** de conteúdo e destino:
   - Original em `/srv/hermes/saude/exames-laboratoriais/laudos/AAAA-MM-DD_laboratorio.<ext>`.
   - Uma linha por marcador em `exames.csv`: `data_coleta` (`YYYY-MM-DD`), `marcador` (nome padronizado, ex.: `vitamina_d_25oh`, `hba1c`, `ldl`), `valor`, `unidade`, `ref_min`, `ref_max`, `ref_texto` (quando a referência não é um intervalo simples), `laboratorio`, `arquivo_laudo`, `status_observacoes`.
   - Chave `data_coleta + marcador`: igual = duplicata (não grava); diferente = conflito (não grava; perguntar).
   - Reler as linhas gravadas.
5. **Ajuste alimentar ou suplementação**, se pedido: informativo, via `nutrition-planning` (referência `estrutura-plano.md`).

## Marcadores de interesse frequentes
Glicose e HbA1c; lipidograma; hemograma; ferritina e ferro; vitamina D (25-OH); TSH e T4 livre; testosterona total e livre; TGO e TGP; creatinina e TFG; PCR ultrassensível.

## Segurança
IA informativa, não profissional habilitado. Não diagnosticar, não prescrever medicamento, suplemento ou dieta terapêutica, não sugerir mudar tratamento. Valor muito alterado ou sintomas: orientar avaliação médica, sem alarmismo; sintomas graves ou agudos: urgência.

## Verificação
Só o pedido foi atendido? Faixas do próprio laudo? Unidades compatíveis? Nada gravado sem autorização? Sem diagnóstico nem prescrição?
