---
name: nutrition-planning
description: "Use when planning practical nutrition for a user."
version: 1.0.0
author: Hermes Agent
created_by: agent
---

# Nutrition Planning

Use when a user asks for meals, calorie/protein/macronutrient targets, a diet structure, or daily food tracking. For an informative habits/weekly check-in without meal planning, prefer `nutricionista-pessoal`. Do not assume the identity of a licensed nutritionist.

## Principles

- Lead with the usable recommendation; do not stall with repeated intake questions.
- Personalize only from verified user-provided data. Label provisional plans and assumptions clearly.
- Do not present estimates, calorie needs, or body-composition conclusions as exact clinical facts.
- Favor simple, low-friction meals, accessible ingredients, and substitutions that match the user's restrictions and budget.
- Track daily food totals only when requested, in the current conversation, not a durable file/memory; do not silently create a log when the user merely mentions a meal. Reset totals for a new day.
- Saving even stable restrictions, goals or preferences requires specific authorization for content and destination. No automatic health recording.

## Workflow

1. **Use current context first.** Reuse relevant information already supplied. Access persistent health/preferences only when necessary and authorized; check `/srv/hermes/saude/PERFIL.md` (goals, restrictions, intolerances, routine) or locate the specific source through `/srv/hermes/base/MAPA-MEMORIAS.md`. Do not read all memories or presume records exist.
2. **Identify the decision.** Is the user asking for a single meal, a daily plan, calorie target, or intake log update?
3. **Handle missing inputs without blocking unnecessarily.**
   - For a calculated BMR/TDEE estimate, request only missing essential inputs once; no estimate is an exact clinical target.
   - If the user still wants a plan, provide a practical provisional meal structure with adjustable portions instead of repeatedly withholding a result.
4. **Calculate transparently.** Use a calculation tool for arithmetic. State inputs, assumptions, target calories/macros, and that TDEE changes with real activity and progress data.
5. **Build for adherence.** Offer short preparation paths, batch-cooking options, and inexpensive alternatives. Prioritize protein in each meal.
6. **For nausea, reflux, or reduced appetite,** recommend smaller portions, low-fat/easy-to-tolerate choices, and avoiding the user's known triggers. Include only meaningful medical escalation warnings.
7. **Track updates only when requested.** Estimate portions and current-day totals in conversation from actual reported consumption, stating uncertainty about weights, sauces and preparation. Do not treat a proposed/ordered meal as consumed.

## Bioimpedance Reports and Progress

When a user provides an InBody or similar body-composition report:

1. For requested report reading, route to `interpretacao-bioimpedancia`; extract only values necessary for the nutrition question. Do not extract identification, QR or all sections by default. Preserve divergent handwritten notes separately rather than silently replacing printed values.
2. Treat a historical chart embedded in a later report as a summary, not as the original report for that historical date. Do not claim access to an original form unless that form was actually provided.
3. If the user corrects dates/values, update the current answer and affected calculations. Editing a durable record requires an explicit correction request/authorization for the target; preserve provenance and read back an authorized change. Do not silently overwrite a disputed source.
4. Separate reported measurements from computed deltas; label the latter as calculations.
5. Generate charts only when requested; use the authorized series within the requested period for each requested metric. If body-fat methods differ (for example, InBody and US Navy), plot them as separate, clearly labeled series; never connect or compare them as though they were interchangeable. Leave missing measurements as visible gaps rather than estimating them.

## Response Shape

- When the user asks for meals one at a time, give only the next meal. Do not pre-emptively list later meals; adapt them after the user confirms the current one.
- When the user requests one optimized suggestion, choose one concrete option rather than presenting alternatives. Include only the quantities and caveat needed to use it.
- For plans involving appetite-affecting medication or active gastrointestinal symptoms, prioritize a modest portion, protein, low-to-moderate fat, and the user's tolerated foods. Do not recommend adding or combining medicines without individualized medical confirmation.

## Pitfalls

- Do not repeatedly ask for data already given or available in prior context.
- Do not claim a plan is based on BMR if the BMR or equivalent inputs are unavailable.
- Do not recommend foods that conflict with known intolerances, restrictions, or stated dislikes.
- For restaurant or fast-food requests, distinguish a one-off fallback from the planned diet; do not call an option optimized if it conflicts with the user's current gastrointestinal triggers or medication context.
- Do not use dairy as a default protein suggestion when lactose intolerance is known.
- Do not over-format operational nutrition updates with empty status labels or filler.

## Reference

Read `references/nutrition-intake-checklist.md` only when essential inputs/calculation planning need clarification. For a recipe, use the format and cheap substitutions in `references/formato-receita.md`. For a full-day or weekly plan, or a supplement question, consult `references/estrutura-plano.md` (optional principles, never imposed rules). For BMR/TDEE/deficit, run the `calculos-corporais` script. For requests such as “one suggestion”, “one meal at a time”, or a concise actionable plan without repeated intake questions, consult `references/response-patterns.md` as needed.

## Safety
Informative meal planning, not licensed clinical care. Do not prescribe medicines, supplements or therapeutic diets, change treatment, diagnose from labs/body measurements, or promise outcomes. Pregnancy, minors, eating-disorder concerns or medical conditions need qualified individualized support; avoid unsupervised restrictive/weight-loss targets in these contexts. For severe or persistent symptoms, prioritize professional assessment; acute danger requires urgent care. Use source-appropriate reference ranges, not universal personal targets.
