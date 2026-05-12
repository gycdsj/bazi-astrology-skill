---
name: bazi-fortuneteller
description: Runs bazi chart generation, dayun analysis, full-report generation, and chat context building for user-facing fortune-telling questions.
disable-model-invocation: true
---

# Bazi Fortuneteller Skill

## Instructions

1. Use `BaziAnalysisSkill` from `analysis_skill.py`.
2. Prefer `analyze_user_request(user_message, ...)` for user-facing requests.
3. Pass birth date/time and gender when available; if they are missing, the skill will ask the user to provide them.
4. The skill handles generic full reports, concrete questions, and time-related questions internally.

## Notes

- This skill intentionally excludes any HTML/JS UI logic.
- Model defaults are in `prompt_config.py`.

