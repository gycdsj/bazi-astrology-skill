# bazi-analysis-skill

将“随便算算”网站中的分析能力抽离为可复用的 Python Skill（不包含前端）。

## 包含能力

- 命格分析 Prompt 组装（生辰解读 / 十神格局 / 五行喜忌）
- 大运详情 Prompt 组装
- 对话上下文组装（八字、完整大运、命格分析结果、当前时序信息）
- 命格分析结果解析（含结构化五行喜忌提取）
- 通过 DeepSeek(OpenAI SDK 兼容) 调用模型

## 快速开始

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python example_cli.py
```

## 主要文件

- `analysis_skill.py`：核心 Skill 类
- `prompt_config.py`：Prompt 模板
- `example_cli.py`：最小调用示例

