---
name: bazi-astrology
description: 提供八字排盘、大运分析、完整报告生成与聊天上下文构建，面向命理占星类用户问题。
disable-model-invocation: true
---

# 八字占星技能

## 使用说明

1. 从 `analysis_skill.py` 使用 `BaziAnalysisSkill`。
2. 面向用户的请求优先调用 `analyze_user_request(user_message, ...)`。
3. 用户侧需提供出生年月日时（`birth_year`、`birth_month`、`birth_day`、`birth_hour`，可选 `birth_minute`）以及 `gender`；若缺失，Skill 会提示用户补充。
4. Skill 内部区分：泛化完整报告、具体问题、以及带时间指向的问题。
5. 若用户仅提出泛化分析需求（例如「帮我分析这个生辰八字」「帮我分析」），`analyze_user_request()` 会输出一份完整报告。报告先展示八字详情表（天干、天干十神、地支、地支藏干十神、神煞），再涵盖命格分析、当前三步大运详解、五行喜忌与转运建议；报告所用提示词中包含已计算的十神与神煞上下文。
6. 若用户提出具体问题，`analyze_user_request()` 通过 `build_chat_context_string()` 构建的 `/chat` 上下文作答，并携带已计算的十神与神煞上下文。
7. 若 `/chat` 问题中出现时间表述（如「下个月」「明年」或具体公历日期），Skill 会推算目标流年、流月、流日干支以及该日所属大运干支，并写入聊天提示词。

## 备注

- 本 Skill 不包含任何 HTML/JS 界面逻辑。
- 模型默认参数见 `prompt_config.py`。
