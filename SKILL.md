---
name: bazi-analysis-skill
description: Extracts and runs bazi analysis logic (mingge analysis, dayun detail analysis, and chat context building) without any frontend. Use when the user wants backend-only analysis capability from the suibiansuansuan website.
disable-model-invocation: true
---

# Bazi Analysis Skill

## Instructions

1. Use `BaziAnalysisSkill` from `analysis_skill.py`.
2. Input should provide precomputed `bazi_data` and optional `complete_dayun`.
3. For命格分析, call `analyze_mingge()`.
4. For单步大运详情, call `analyze_dayun_detail()`.
5. For对话首轮上下文, call `build_chat_context_string()`.

## Notes

- This skill intentionally excludes any HTML/JS UI logic.
- Model defaults are in `prompt_config.py`.

