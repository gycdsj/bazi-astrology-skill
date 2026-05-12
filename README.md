# bazi-fortuneteller-skill

一个用于八字排盘与命理问答的 Python Skill。输入出生信息和问题，返回适合用户阅读的中文分析。

## 能做什么

- 根据出生年月日时和性别生成八字分析。
- 输出完整报告，包括命盘详情、命格分析、当前三步大运、五行喜忌和转运建议。
- 回答具体问题，例如事业、财运、感情、健康、考试、副业、投资等。
- 回答带时间的问题，例如“明天运势如何”“下个月是否顺利”“今年能不能挣钱”。
- 如果出生信息不完整，会提示用户补充出生年月日时和性别。

## 安装

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 模型配置

使用 OpenClaw / OpenAI SDK 兼容的大模型接口。运行前请配置以下任一组环境变量：

- `OPENCLAW_API_KEY` / `OPENCLAW_BASE_URL` / `OPENCLAW_MODEL`
- 兼容 `OPENAI_API_KEY` / `OPENAI_BASE_URL` / `OPENAI_MODEL`
- 也兼容 `LLM_API_KEY` / `LLM_BASE_URL` / `LLM_MODEL`

如果运行环境没有注入这些变量，可以复制 `.env.example` 后填写本地配置：

```bash
cp .env.example .env
```

不要提交真实 token。`.env` 已被 `.gitignore` 忽略。

## 使用方式

### 完整报告

用户只说“帮我分析一下”“帮我分析这个生辰八字”等，没有限定具体方面时，会返回完整报告。

```python
from analysis_skill import BaziAnalysisSkill

skill = BaziAnalysisSkill()
answer = skill.analyze_user_request(
    user_message="我出生时间是1992年8月9日11:50，女，分析一下",
    gender="女",
    birth_year=1992,
    birth_month=8,
    birth_day=9,
    birth_hour=11,
    birth_minute=50,
)
```

完整报告会先展示命盘详情表，再输出命格分析、当前三步大运详解、五行喜忌和转运建议。

### 具体问题

用户问具体事项时，会直接围绕这个问题回答。

```python
answer = skill.analyze_user_request(
    user_message="我今年副业能挣钱吗？",
    gender="女",
    birth_year=1992,
    birth_month=8,
    birth_day=9,
    birth_hour=11,
    birth_minute=50,
)
```

### 时间类问题

用户问题涉及时间时，可以直接把时间写在问题里。

```python
answer = skill.analyze_user_request(
    user_message="我下个月生孩子会不会顺利？",
    gender="女",
    birth_year=1992,
    birth_month=8,
    birth_day=9,
    birth_hour=11,
    birth_minute=50,
)
```

回答会直接说明对应时间的运势，不会机械列出大运、流年、流月、流日清单。

### 出生信息不完整

如果用户没有提供出生年月日时，直接调用也可以：

```python
answer = skill.analyze_user_request(user_message="帮我分析一下")
```

返回内容会提示用户补充出生年月日时、性别，以及公历/农历信息。

## 输入字段

常用字段如下：

| 字段 | 说明 |
|---|---|
| `user_message` | 用户原始问题 |
| `gender` | 性别，影响大运顺逆 |
| `birth_year` | 出生年 |
| `birth_month` | 出生月 |
| `birth_day` | 出生日 |
| `birth_hour` | 出生小时，24 小时制 |
| `birth_minute` | 出生分钟，默认 `0` |
| `is_lunar` | 是否农历，默认 `False` |
| `leap_month` | 农历是否闰月，默认 `False` |

