#!/usr/bin/env bash
# Ativa a criptografia (git-crypt) do repositório da Maya.
# Rodar UMA vez, NO SERVIDOR DA MAYA, na raiz do repositório (/srv/hermes),
# depois de copiar os dados para saude/, estudo/, MEMORY.md e CONTEXTO.md.
#
# Uso: scripts/ativar-criptografia.sh [caminho-da-chave]
#      padrão da chave: /root/.config/hermes-maya/git-crypt.key  (FORA do repositório)
set -euo pipefail

CHAVE="${1:-/root/.config/hermes-maya/git-crypt.key}"
RAIZ="$(git rev-parse --show-toplevel)"
cd "$RAIZ"
GITDIR="$(git rev-parse --git-dir)"

command -v git-crypt >/dev/null || { echo "git-crypt não instalado: sudo apt install git-crypt" >&2; exit 1; }

case "$(realpath -m "$CHAVE")/" in
  "$RAIZ"/*) echo "ERRO: a chave não pode ficar dentro do repositório ($RAIZ)." >&2; exit 1 ;;
esac

# 1) trava de segurança (pre-commit) neste clone
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit

# 2) cria a chave simétrica (só se ainda não existir neste clone)
if [ ! -d "$GITDIR/git-crypt/keys" ]; then
  git-crypt init
fi

# 3) exporta a chave para fora do repositório, legível só pelo dono
if [ ! -f "$CHAVE" ]; then
  install -d -m 700 "$(dirname "$CHAVE")"
  ( umask 077; git-crypt export-key "$CHAVE" )
  echo "Chave exportada para: $CHAVE"
  echo ">>> Guarde uma cópia offline AGORA (ex.: gerenciador de senhas): base64 -w0 \"$CHAVE\""
else
  echo "Chave já existe em $CHAVE (não sobrescrita)."
fi

# 4) libera os dados pessoais para versionamento (agora criptografados)
sed -i '/^# >>> dados-sensiveis/,/^# <<< dados-sensiveis/d' .gitignore
git add -A

# 5) confere: nada que deveria estar criptografado pode estar em texto claro
if git-crypt status 2>&1 | grep -q 'NOT ENCRYPTED'; then
  echo "ERRO: há arquivos em texto claro que deveriam estar criptografados:" >&2
  git-crypt status 2>&1 | grep -B1 'NOT ENCRYPTED' >&2
  exit 1
fi

echo
echo "Arquivos que irão CRIPTOGRAFADOS:"
git-crypt status -e | sed 's/^/  /'
echo
echo "Tudo certo. Próximos passos:"
echo "  git commit -m 'feat: dados pessoais versionados com git-crypt'"
echo "  git push"
echo "Teste: clone o repositório em outra pasta SEM a chave e confira que saude/ está ilegível."
