# Segundo Cérebro — Maya (assistente pessoal)

> Repositório **exclusivamente pessoal**, operado pela **Maya** (Hermes Agent) em um computador dedicado, em `/srv/hermes`.
> Tudo o que é de trabalho (Funpresp, coordenação, equipe, contratos, fornecedores) é da **Julia**, em outro
> repositório e outro computador. A Maya encaminha esses assuntos à Julia pelo grupo Telegram Hermes, com
> autorização e dados mínimos (protocolo em `base/FLUXOS.md`), e nunca envia dados de saúde a ela.

## Como a Maya funciona

1. **Persona:** `SOUL.md` (no Hermes, `/home/maya/.hermes/SOUL.md` é um link para `/srv/hermes/SOUL.md`).
2. **Entrada:** na primeira tarefa da sessão, lê `base/INICIO.md` e `base/REGRAS-SEGURANCA.md`.
3. **Navegação:** `base/MAPA-MEMORIAS.md` é o **único** catálogo de rotas (fontes e skills). Lê só o necessário.
4. **Execução:** `base/FLUXOS.md` antes de gravar, gerar artefatos ou falar com a Julia.
5. **Princípios:** analisar não autoriza gravar; nada de diagnóstico; não inventar dados; cada informação tem uma fonte principal.

## Estrutura

```
/srv/hermes/
├── SOUL.md                 persona da Maya
├── base/                   entrada, segurança, fluxos, mapa, contexto, objetivos
├── config/
│   ├── memorias/           preferências, estado operacional, contextos temáticos, cópia da memória nativa
│   └── cronjobs/           estado das automações (documentação, não prova de execução)
├── saude/
│   ├── PERFIL.md           dados básicos, objetivos, restrições, rotina
│   ├── bioimpedancia/      série InBody (CSV), dicionário, log, laudos/
│   ├── checkins/           medidas de fita, US Navy, check-ins (CSV)
│   ├── exames-laboratoriais/  exames (CSV) e laudos/
│   └── registros/          registros pessoais por data
├── estudo/                 estudos pessoais
├── rascunhos/              temporários (fora do Git)
├── skills/saude/           13 skills
└── scripts/                ativar-criptografia.sh
```

## Skills (`skills/saude/`)

| Área | Skills |
|---|---|
| Composição corporal | `interpretacao-bioimpedancia` (lê e registra laudos; script `bioimpedancia.py`), `biometric-tracking`, `relatorio-bioimpedancia` (script `gerar_dashboard.py`), `calculos-corporais` (script `calculos.py`) |
| Nutrição | `nutrition-planning` (refeições, receitas, plano), `nutricionista-pessoal` (check-in e perfil) |
| Exames | `exames-laboratoriais` |
| Apoio emocional | `apoio-terapeutico` (roteador), `tcc-reflexao`, `gestalt-dialogo`, `gestalt-experimentos`, `gestalt-integracao`, `preparo-para-terapia` |

## Criptografia (git-crypt)

- **Tudo é criptografado por padrão.** Em texto claro só ficam `README.md`, `.gitattributes`, `.gitignore`, `.githooks/`, `scripts/` e `skills/`.
- No GitHub os arquivos protegidos são ilegíveis; no computador da Maya, com a chave, aparecem normais.
- **A chave nunca vai para o GitHub:** fica em `/root/.config/hermes-maya/git-crypt.key` (permissão 600, fora do repositório) e numa cópia offline.
- **Trava:** `.githooks/pre-commit` bloqueia arquivo protegido em texto claro e qualquer chave do git-crypt.
- **O GitHub ainda vê** nomes de arquivos e pastas, tamanhos, datas e mensagens de commit. Não usar nomes de pessoas ou detalhes sensíveis nesses lugares.
- **Perdeu a chave, perdeu os dados do GitHub.** Guarde a cópia offline.

## Instalação no computador da Maya (uma vez)

```bash
sudo apt install git git-crypt python3-venv
git clone https://github.com/alessanderson/hermes-2nd-brain-maya.git /srv/hermes
cd /srv/hermes
# copiar o conteúdo pessoal para dentro do clone:
#   SOUL.md, base/, config/, saude/, estudo/, rascunhos/README.md
scripts/ativar-criptografia.sh                         # cria a chave, exporta para fora do repo e confere
base64 -w0 /root/.config/hermes-maya/git-crypt.key     # copiar para o gerenciador de senhas
git commit -m "feat: conteúdo pessoal versionado com git-crypt"
git push

python3 -m venv /srv/hermes/.venv && /srv/hermes/.venv/bin/pip install matplotlib
ln -sf /srv/hermes/SOUL.md /home/maya/.hermes/SOUL.md
```

Depois: configurar o Hermes para enxergar as skills de `/srv/hermes/skills/saude/` e conferir a memória nativa
(há uma cópia de referência em `config/memorias/backup-memoria-nativa.md`).

## Outra máquina (ler ou restaurar)

```bash
git clone https://github.com/alessanderson/hermes-2nd-brain-maya.git
cd hermes-2nd-brain-maya
git-crypt unlock /caminho/da/git-crypt.key
git config core.hooksPath .githooks
```
