#!/usr/bin/env python3
"""Base de bioimpedância: inserir exame (com deduplicação e validação) e validar a base.

Uso:
  bioimpedancia.py inserir --json exame.json [--dry-run]
  bioimpedancia.py validar

O JSON pode ser um objeto (um exame) ou uma lista de objetos. Chaves = colunas do CSV.
CSV padrão: $SAUDE_DIR/bioimpedancia/bioimpedancias.csv (SAUDE_DIR padrão: /srv/hermes/saude).
Use --csv para outro arquivo. Só biblioteca padrão.

Saídas por exame: INSERIDO | DUPLICATA | CONFLITO, seguidas de ALERTA: ... quando houver.
Código de saída: 0 ok, 2 se houve CONFLITO ou erro de dados.
"""
import argparse
import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path

SAUDE_DIR = Path(os.environ.get("SAUDE_DIR", "/srv/hermes/saude"))
CSV_PADRAO = SAUDE_DIR / "bioimpedancia" / "bioimpedancias.csv"
CHAVE = "data_hora"
CAMPOS_DUP = ("peso_kg", "pgc_percentual", "massa_muscular_esqueletica_kg")


def num(v):
    try:
        return float(v) if v not in (None, "") else None
    except ValueError:
        return None


def data_valida(s):
    """Aceita 'YYYY-MM-DD HH:MM' ou só 'YYYY-MM-DD' (hora não registrada; nunca inventar hora)."""
    for f in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            datetime.strptime(s, f)
            return True
        except ValueError:
            pass
    return False


def checar(r):
    """Retorna lista de alertas de consistência de uma linha."""
    al = []
    if not data_valida(r.get(CHAVE, "")):
        al.append(f"data_hora fora do formato YYYY-MM-DD HH:MM (ou YYYY-MM-DD sem hora): {r.get(CHAVE)!r}")
    peso, mg = num(r.get("peso_kg")), num(r.get("massa_gordura_kg"))
    comp = [num(r.get(c)) for c in ("agua_corporal_total_l", "proteina_kg", "minerais_kg")]
    if peso and mg is not None and None not in comp:
        s = sum(comp) + mg
        if abs(s - peso) > 0.3:
            al.append(f"água+proteína+minerais+gordura={s:.2f} difere do peso {peso}")
    pgc = num(r.get("pgc_percentual"))
    if peso and mg is not None and pgc is not None and abs(mg / peso * 100 - pgc) > 0.3:
        al.append(f"PGC {pgc} difere de massa_gordura/peso={mg / peso * 100:.1f}")
    alt, imc = num(r.get("altura_cm")), num(r.get("imc"))
    if peso and alt and imc is not None and abs(peso / (alt / 100) ** 2 - imc) > 0.2:
        al.append(f"IMC {imc} difere de peso/altura²={peso / (alt / 100) ** 2:.1f}")
    mlg = num(r.get("massa_livre_gordura_kg"))
    if peso and mg is not None and mlg is not None and abs(peso - mg - mlg) > 0.2:
        al.append(f"massa livre de gordura {mlg} difere de peso−gordura={peso - mg:.1f}")
    tmb = num(r.get("tmb_kcal"))
    if mlg is not None and tmb is not None and abs(370 + 21.6 * mlg - tmb) > 5:
        al.append(f"TMB {tmb:.0f} difere de Katch-McArdle {370 + 21.6 * mlg:.0f} (MLG {mlg})")
    return al


def ler(path):
    with open(path, encoding="utf-8", newline="") as f:
        rd = csv.DictReader(f)
        return rd.fieldnames, list(rd)


def gravar(path, campos, linhas):
    linhas.sort(key=lambda r: r[CHAVE])
    tmp = Path(str(path) + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos, lineterminator="\n")
        w.writeheader()
        w.writerows(linhas)
    os.replace(tmp, path)


def marcar(r, alertas):
    obs = r.get("status_observacoes", "") or ""
    for a in alertas:
        tag = f"possível_erro: {a}"
        if tag not in obs:
            obs = f"{obs}; {tag}" if obs else tag
    r["status_observacoes"] = obs


def cmd_inserir(a):
    campos, linhas = ler(a.csv)
    novos = json.load(open(a.json, encoding="utf-8"))
    if isinstance(novos, dict):
        novos = [novos]
    rc, mudou = 0, False
    for n in novos:
        extras = set(n) - set(campos)
        if extras:
            print(f"ERRO: colunas fora do schema: {sorted(extras)}")
            rc = 2
            continue
        r = {c: "" if n.get(c) is None else str(n.get(c)) for c in campos}
        k = r[CHAVE]
        exist = next((x for x in linhas if x[CHAVE] == k), None)
        if exist:
            dif = [c for c in CAMPOS_DUP if num(exist[c]) != num(r[c])]
            if dif:
                print(f"CONFLITO {k}: já existe com valores diferentes em {dif} "
                      f"(base: {[exist[c] for c in dif]}, novo: {[r[c] for c in dif]}). Nada gravado.")
                rc = 2
            else:
                print(f"DUPLICATA {k}: já está na base. Nada gravado.")
            continue
        alertas = checar(r)
        marcar(r, alertas)
        linhas.append(r)
        mudou = True
        print(f"INSERIDO {k}")
        for x in alertas:
            print(f"  ALERTA: {x}")
    if mudou and not a.dry_run:
        gravar(a.csv, campos, linhas)
    elif mudou:
        print("(dry-run: CSV não alterado)")
    return rc


def cmd_validar(a):
    campos, linhas = ler(a.csv)
    rc = 0
    vistos = {}
    for i, r in enumerate(linhas, start=2):
        if r[CHAVE] in vistos:
            print(f"linha {i}: data_hora {r[CHAVE]} repetida (também na linha {vistos[r[CHAVE]]})")
            rc = 2
        vistos.setdefault(r[CHAVE], i)
        for x in checar(r):
            print(f"linha {i} ({r[CHAVE]}): {x}")
    datas = [r[CHAVE] for r in linhas]
    if datas != sorted(datas):
        print("base fora de ordem cronológica")
    print(f"{len(linhas)} exames; período {min(datas) if datas else '-'} → {max(datas) if datas else '-'}")
    return rc


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--csv", type=Path, default=CSV_PADRAO)
    sub = p.add_subparsers(dest="cmd", required=True)
    pi = sub.add_parser("inserir")
    pi.add_argument("--json", required=True)
    pi.add_argument("--dry-run", action="store_true")
    sub.add_parser("validar")
    a = p.parse_args(argv)
    return cmd_inserir(a) if a.cmd == "inserir" else cmd_validar(a)


if __name__ == "__main__":
    sys.exit(main())
