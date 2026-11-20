import os
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(os.environ.get("HERMES_ROOT", "/srv/hermes"))
MAPA_PATH = ROOT_DIR / "MAPA.md"

IGNORE_DIRS = {".git", "__pycache__", "venv", "node_modules", "archive"}
IGNORE_FILES = {"MAPA.md", "CONTEXTO.md", "MEMORY.md"}

def extrair_resumo_frontmatter(arquivo_path: Path) -> str:
    """Lê as primeiras linhas do arquivo procurando pelo resumo no Frontmatter YAML."""
    try:
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            linhas = [f.readline() for _ in range(15)] # Lê até as 15 primeiras linhas
            
        conteudo = "".join(linhas)
        if conteudo.startswith("---"):
            for linha in linhas:
                if linha.lower().startswith("resumo:"):
                    # Remove a palavra 'resumo:', aspas e espaços extras
                    return linha.split(":", 1)[1].strip().strip('"\'')
    except Exception:
        pass
    return ""

def gerar_arvore(diretorio: Path, prefixo: str = "") -> list:
    """Varre recursivamente o diretório, extrai resumos e formata em Markdown."""
    linhas = []
    try:
        itens = sorted(diretorio.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
    except PermissionError:
        return [f"{prefixo}- *[Acesso Negado]*"]

    for item in itens:
        if item.name.startswith('.') or item.name in IGNORE_DIRS:
            continue
            
        if item.is_file():
            if item.name in IGNORE_FILES:
                continue
            if item.suffix in [".md", ".txt"]:
                resumo = extrair_resumo_frontmatter(item)
                if resumo:
                    linhas.append(f"{prefixo}- `{item.name}` — *{resumo}*")
                else:
                    linhas.append(f"{prefixo}- `{item.name}`")
                    
        elif item.is_dir():
            linhas.append(f"{prefixo}- **{item.name}/**")
            linhas.extend(gerar_arvore(item, prefixo + "  "))
            
    return linhas

def atualizar_mapa():
    print(f"Iniciando varredura inteligente em {ROOT_DIR}...")
    
    conteudo_mapa = [
        "# MAPA DO SEGUNDO CÉREBRO — MAYA (PESSOAL)",
        f"> *Atualizado automaticamente em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "> **Instrução para o Agente:** Este mapa contém índices e resumos rápidos das notas. Use-o para identificar o arquivo correto antes de ler o conteúdo completo.",
        ""
    ]

    # Repositório da Maya (assistente pessoal). Nada de trabalho aqui: isso é da Julia.
    subpastas_principais = ["saude", "estudo"]
    
    for sub in subpastas_principais:
        pasta_path = ROOT_DIR / sub
        if pasta_path.exists() and pasta_path.is_dir():
            permissao = "[Leitura e Escrita]"
            
            conteudo_mapa.append(f"## `/{sub}` - {permissao}")
            
            arvore = gerar_arvore(pasta_path, prefixo="")
            if arvore:
                conteudo_mapa.extend(arvore)
            else:
                conteudo_mapa.append("*(Pasta vazia)*")
            conteudo_mapa.append("")

    MAPA_PATH.write_text("\n".join(conteudo_mapa), encoding="utf-8")
    print(f"Sucesso! MAPA.md atualizado com resumos em: {MAPA_PATH}")

if __name__ == "__main__":
    atualizar_mapa()
