# Segundo Cérebro — Maya (assistente pessoal)

> Repositório **exclusivamente pessoal**, operado pela **Maya** (Hermes Agent) em um computador dedicado.
> Tudo o que é de trabalho (Funpresp, coordenação de infraestrutura, equipe, contratos, fornecedores)
> fica com a **Julia**, em outro repositório e outro computador. Os dois não compartilham arquivos.

## Escopo

| A Maya cuida | A Maya não trata (é da Julia) |
|---|---|
| Saúde, composição corporal, nutrição, treino, exames | Funpresp, cargo de coordenador, equipe, terceirizados |
| Estudos e cursos pessoais | Contratos, fornecedores, fiscalização, tarefas TAR-### |
| Futuras áreas pessoais (finanças, casa, viagens…) | Capacitação ligada ao cargo |

Se o assunto for de trabalho, a Maya só responde que isso é com a Julia.

## Estrutura

```
/srv/hermes/
├── README.md          ← este arquivo (texto claro)
├── CONTEXTO.md        ← quem é o usuário como pessoa e limites da Maya        [criptografado]
├── MEMORY.md          ← cópia versionada da memória do perfil no Hermes        [criptografado]
├── MAPA.md            ← índice gerado por scripts/atualizar_mapa.py           [criptografado]
├── saude/             ← dados e regras de saúde; índice em saude/README.md   [criptografado]
├── estudo/            ← estudos pessoais                                      [criptografado]
├── skills/saude/      ← 9 skills de saúde (texto claro, sem dado pessoal)
├── scripts/           ← atualizar_mapa.py, ativar-criptografia.sh (texto claro)
└── .githooks/         ← trava pre-commit contra vazamento (texto claro)
```

Áreas novas: criar a pasta na raiz quando houver conteúdo real e incluí-la em `scripts/atualizar_mapa.py`.
Ela já nasce criptografada (regra padrão do `.gitattributes`).

## Criptografia (git-crypt)

- **Padrão: tudo é criptografado.** Só `README.md`, `.gitattributes`, `.gitignore`, `.githooks/`, `scripts/` e `skills/` vão em texto claro.
- No GitHub, os arquivos protegidos são binários ilegíveis. No servidor da Maya, com a chave, aparecem normais: o agente lê e escreve sem nenhum passo extra.
- **A chave nunca vai para o GitHub.** Ela fica em `/root/.config/hermes-maya/git-crypt.key` (permissão 600, fora do repositório) e numa cópia offline (gerenciador de senhas).
- **Trava:** `.githooks/pre-commit` bloqueia commit de arquivo protegido em texto claro e de qualquer chave do git-crypt.
- **O que o GitHub ainda vê:** nomes de arquivos e pastas, tamanhos, datas e mensagens de commit. Não coloque dado sensível nesses lugares.
- **Se perder a chave, os dados no GitHub ficam irrecuperáveis.** Guarde a cópia offline.

## Instalação no computador da Maya (uma vez)

```bash
sudo apt install git git-crypt python3-venv
git clone https://github.com/alessanderson/hermes-2nd-brain-maya.git /srv/hermes
cd /srv/hermes

# copiar os dados pessoais para dentro do clone (saude/, estudo/, MEMORY.md, CONTEXTO.md, MAPA.md)
# ex.: scp -r usuario@pc:/caminho/hermes-2nd-brain-maya/{saude,estudo,MEMORY.md,CONTEXTO.md,MAPA.md} /srv/hermes/

scripts/ativar-criptografia.sh          # cria a chave, exporta para fora do repo e confere
base64 -w0 /root/.config/hermes-maya/git-crypt.key   # copie para o gerenciador de senhas
git commit -m "feat: dados pessoais versionados com git-crypt"
git push

python3 -m venv /srv/hermes/.venv && /srv/hermes/.venv/bin/pip install matplotlib
```

Depois, configurar o perfil da Maya no Hermes para usar as skills de `/srv/hermes/skills/saude/`
e carregar a memória com o conteúdo de `MEMORY.md`.

## Outra máquina (ler ou restaurar)

```bash
git clone https://github.com/alessanderson/hermes-2nd-brain-maya.git
cd hermes-2nd-brain-maya
git-crypt unlock /caminho/da/git-crypt.key   # sem a chave, os arquivos ficam ilegíveis
git config core.hooksPath .githooks
```

## Regras

1. Não inventar: o que o usuário não informou fica como "a preencher".
2. Dados vêm de documentos ou do usuário; laudos só com dado impresso.
3. Cálculos sempre por script.
4. Linguagem de acompanhamento, nunca diagnóstico.
5. Nunca registrar senhas, tokens ou chaves, nem mesmo criptografados.
6. Nada de trabalho neste repositório.

## Versionamento

- Repositório privado e independente: `alessanderson/hermes-2nd-brain-maya`, branch `main`.
- Sem relação de histórico com o repositório da Julia.
