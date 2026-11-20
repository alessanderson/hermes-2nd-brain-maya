---
name: biometric-tracking
description: Use when recording, comparing, or charting body metrics.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [health, biometrics, body-composition, visualization, tracking]
    related_skills: [nutrition-planning, calculos-corporais, interpretacao-bioimpedancia, relatorio-bioimpedancia]
---

# Biometric Tracking

## When to Use

Use for longitudinal body measurements: weight, circumferences, body-fat percentage, body-composition reports, and progress charts. The goal is faithful recordkeeping and clear trend visualization, not clinical diagnosis.

## Core rules

1. **Preserve the authorized series.** For trends/charts, cover the requested period or the entire authorized series when no period is specified. Do not silently omit earlier records, but never read unrelated health history just to expand coverage.
2. **Keep methods separate.** Body-fat values from InBody, US Navy, skinfolds, or other methods are not interchangeable. Plot each method as a distinct labeled series; never connect them as though they were one continuous measurement source.
3. **Represent missing values honestly.** If a metric was not recorded on a date, leave a gap. Do not interpolate or copy a nearby measurement.
4. **Record source and date.** Every extracted value must retain its measurement date and source/method when applicable.
5. **Separate observation from interpretation.** State factual changes first. Label any explanation as an assumption and avoid diagnosing medical conditions.

## Data model

For each dated entry, capture only known values:

| Field | Notes |
|---|---|
| `date` | ISO date preferred; preserve original date when reported. |
| `weight_kg` | Numeric, if measured. |
| `waist_cm` | Circumference; retain the stated protocol if known. |
| `body_fat_pct` | Numeric, if measured or estimated. |
| `body_fat_method` | `InBody`, `US Navy`, etc. Never infer. |
| `other_measurements` | Neck, hip, chest, arm, thigh, visceral-fat level, skeletal muscle mass. |
| `source` | User measurement, report, or professional assessment. |

## Workflow

1. Identify the requested outcome (recording, comparison, or visualization) from the current request; do not ask again when clear. Use current context first; if needed and authorized, read only the pertinent series: InBody in `/srv/hermes/saude/bioimpedancia/bioimpedancias.csv`; tape measurements, US Navy body fat and weekly check-ins in `/srv/hermes/saude/checkins/checkins.csv`; profile and goals in `/srv/hermes/saude/PERFIL.md`. Locate anything else through `/srv/hermes/base/MAPA-MEMORIAS.md`.
2. Extract only necessary fields; build the requested-period series in memory, keeping dates, sources, units and methods distinct. Do not force a table/schema for a simple answer.
3. Recording requires an explicit request/authorization for content and destination. Preserve the canonical source format, check duplicates/conflicts, and read back the exact target after an authorized write. Analysis or receiving measurements alone does not authorize saving. Never generate charts automatically after recording.
   - Tape measurements and check-ins: one row per date in `checkins.csv`, filling `fonte`; if the date already exists, ask whether to replace it. Leave unknown fields empty.
   - InBody rows: only through `interpretacao-bioimpedancia` (its script deduplicates and validates).
   - US Navy body fat: only when requested or when the user supplies neck + waist and wants it; calculate with `calculos-corporais` (never mentally) and store in `pgc_navy_percentual`.
4. Only for a requested multi-metric chart, prefer separate aligned panels for:
   - body-fat percentage (one line per method);
   - weight;
   - waist circumference.
5. Use a legend and source note. Annotate point values only when legibility permits.
6. Call out measurement gaps in the caption or chart note.
7. Before delivery, verify the requested coverage and that no method was merged incorrectly. Use tools for all calculations. For a requested bioimpedance dashboard/report, use `relatorio-bioimpedancia`; no automatic exports.

## Interpretation guardrails

- A short-term weight or waist change can be influenced by hydration, meal timing, bowel contents, and measurement technique; do not label it fat gain/loss without supporting evidence.
- Use body-composition results as tracking information, not a substitute for medical assessment.
- When medical targets are mentioned, quote the professional guidance accurately and do not convert it into a diagnosis.

## Chart acceptance checklist

- [ ] The timeline begins at the oldest authorized record within the requested scope.
- [ ] The timeline ends at the latest authorized record within the requested scope.
- [ ] Each body-fat method is visually distinct and named.
- [ ] Weight and waist use their own axes/panels.
- [ ] Missing values appear as gaps, not fabricated points.
- [ ] The legend/caption identifies sources and limitations.
