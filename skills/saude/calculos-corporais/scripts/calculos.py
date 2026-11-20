#!/usr/bin/env python3
"""Cálculos corporais: % gordura (US Navy, cm), massa gorda/magra, TMB Katch-McArdle, TDEE.

Uso:
  calculos.py --sexo M --altura 180 --peso 86.1 --cintura 92 --pescoco 40 \
              [--quadril 100] [--massa-magra 66.5] [--atividade moderado] [--ajuste -500]
Saída: JSON. Só biblioteca padrão.
"""
import argparse
import json
import math
import sys

FATORES = {"sedentario": 1.2, "leve": 1.375, "moderado": 1.55, "muito": 1.725, "extremo": 1.9}


def pgc_navy(sexo, altura, cintura, pescoco, quadril=None):
    if sexo == "M":
        base = cintura - pescoco
        if base <= 0:
            raise ValueError("cintura deve ser maior que pescoço")
        return 495 / (1.0324 - 0.19077 * math.log10(base) + 0.15456 * math.log10(altura)) - 450
    if quadril is None:
        raise ValueError("--quadril é obrigatório para sexo F")
    base = cintura + quadril - pescoco
    if base <= 0:
        raise ValueError("cintura + quadril deve ser maior que pescoço")
    return 495 / (1.29579 - 0.35004 * math.log10(base) + 0.22100 * math.log10(altura)) - 450


def tmb_katch(massa_magra):
    return 370 + 21.6 * massa_magra


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--sexo", choices=["M", "F"], required=True)
    p.add_argument("--altura", type=float, required=True, help="cm")
    p.add_argument("--peso", type=float, required=True, help="kg")
    p.add_argument("--cintura", type=float, help="cm")
    p.add_argument("--pescoco", type=float, help="cm")
    p.add_argument("--quadril", type=float, help="cm (obrigatório para F)")
    p.add_argument("--massa-magra", type=float, help="kg, ex.: do InBody; substitui a estimativa da Marinha na TMB")
    p.add_argument("--atividade", choices=sorted(FATORES))
    p.add_argument("--ajuste", type=float, default=0, help="kcal somadas ao TDEE para a meta (ex.: -500)")
    a = p.parse_args(argv)

    if a.altura < 120:
        p.error("altura parece estar em polegadas ou metros; informe em cm")
    for nome in ("cintura", "pescoco", "quadril"):
        v = getattr(a, nome)
        if v is not None and v < 25:
            p.error(f"{nome}={v} parece estar em polegadas; informe em cm")

    out = {"entradas": {k: v for k, v in vars(a).items() if v is not None}}

    if a.cintura is not None and a.pescoco is not None:
        g = pgc_navy(a.sexo, a.altura, a.cintura, a.pescoco, a.quadril)
        mg = a.peso * g / 100
        out["navy"] = {
            "pgc_percentual": round(g, 1),
            "massa_gorda_kg": round(mg, 1),
            "massa_magra_kg": round(a.peso - mg, 1),
        }

    if a.massa_magra is not None:
        mm, origem = a.massa_magra, "informada (InBody)"
    elif "navy" in out:
        mm, origem = out["navy"]["massa_magra_kg"], "estimada (Marinha)"
    else:
        mm, origem = None, None

    if mm is not None:
        tmb = tmb_katch(mm)
        out["tmb"] = {"kcal": int(round(tmb, -1)), "formula": "Katch-McArdle", "massa_magra_origem": origem}
        if a.atividade:
            tdee = tmb * FATORES[a.atividade]
            out["tdee"] = {"kcal": int(round(tdee, -1)), "fator": FATORES[a.atividade], "nivel": a.atividade}
            if a.ajuste:
                out["meta"] = {"kcal": int(round(tdee + a.ajuste, -1)), "ajuste_kcal": a.ajuste}
    elif a.atividade:
        out["aviso"] = "TDEE precisa de massa magra: informe cintura+pescoço ou --massa-magra"

    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
