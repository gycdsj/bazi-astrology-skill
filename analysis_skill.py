import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

from prompt_config import DEEPSEEK_CONFIG, PROMPT_TEMPLATES, SYSTEM_PROMPTS


class BaziAnalysisSkill:
    def __init__(self, api_key=None, base_url=None, model=None):
        load_dotenv()
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY", "")
        self.base_url = base_url or os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        self.model = model or os.getenv("DEEPSEEK_MODEL", DEEPSEEK_CONFIG["model"])
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY 未配置")
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    @staticmethod
    def build_bazi_info_string(bazi_data, gender):
        return (
            "八字信息：\n"
            f"年柱：{bazi_data['nian']['tian_gan']['char']}{bazi_data['nian']['di_zhi']['char']}\n"
            f"月柱：{bazi_data['yue']['tian_gan']['char']}{bazi_data['yue']['di_zhi']['char']}\n"
            f"日柱：{bazi_data['ri']['tian_gan']['char']}{bazi_data['ri']['di_zhi']['char']}\n"
            f"时柱：{bazi_data['shi']['tian_gan']['char']}{bazi_data['shi']['di_zhi']['char']}\n"
            f"性别：{gender}\n"
            f"日主：{bazi_data['ri']['tian_gan']['char']}"
        )

    @staticmethod
    def format_complete_dayun(complete_dayun):
        if not complete_dayun:
            return "未提供完整大运信息。"
        lines = []
        for i, yun in enumerate(complete_dayun, start=1):
            lines.append(
                f"{i}. {yun.get('gan_zhi', '')}（起始年份：{yun.get('year', '')}，对应年龄：{yun.get('age', '')}岁）"
            )
        return "\n".join(lines)

    @staticmethod
    def build_current_time_context():
        now = datetime.now()
        return (
            "当前时序信息：\n"
            f"当前公历日期：{now:%Y-%m-%d}\n"
            "本月干支：请由调用侧传入或在业务层补充\n"
            "今日干支：请由调用侧传入或在业务层补充"
        )

    def build_chat_context_string(
        self,
        bazi_data,
        gender,
        da_yun=None,
        complete_dayun=None,
        mingge_analysis=None,
        current_month_ganzhi=None,
        current_day_ganzhi=None,
    ):
        parts = [self.build_bazi_info_string(bazi_data, gender)]
        parts.append(
            "当前时序信息：\n"
            f"当前公历日期：{datetime.now():%Y-%m-%d}\n"
            f"本月干支：{current_month_ganzhi or '未提供'}\n"
            f"今日干支：{current_day_ganzhi or '未提供'}"
        )
        if complete_dayun:
            parts.append("完整大运（10步）：\n" + self.format_complete_dayun(complete_dayun))
        if da_yun:
            lines = ["当前展示大运："]
            for y in da_yun:
                lines.append(f"- {y.get('year', '')}年 {y.get('gan_zhi', '')}")
            parts.append("\n".join(lines))
        if mingge_analysis:
            lines = ["命格分析结果："]
            if mingge_analysis.get("shengchen"):
                lines.append(f"生辰解读：{mingge_analysis['shengchen']}")
            if mingge_analysis.get("shishen"):
                lines.append(f"十神格局：{mingge_analysis['shishen']}")
            if mingge_analysis.get("xiji"):
                lines.append(f"五行喜忌：{mingge_analysis['xiji']}")
            parts.append("\n".join(lines))
        return "\n\n".join(parts)

    def _chat(self, system_prompt, user_prompt, temperature=None):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=DEEPSEEK_CONFIG["temperature"] if temperature is None else temperature,
            stream=False,
            timeout=DEEPSEEK_CONFIG["timeout"],
        )
        return response.choices[0].message.content or ""

    def build_bazi_analysis_prompt(self, bazi_info, complete_dayun=None):
        return PROMPT_TEMPLATES["bazi_analysis"].format(
            bazi_info=bazi_info,
            complete_dayun=self.format_complete_dayun(complete_dayun),
        )

    def build_dayun_analysis_prompt(self, bazi_info, dayun_ganzhi, complete_dayun=None):
        return PROMPT_TEMPLATES["dayun_analysis"].format(
            bazi_info=bazi_info,
            dayun_ganzhi=dayun_ganzhi,
            complete_dayun=self.format_complete_dayun(complete_dayun),
        )

    def parse_ai_analysis(self, content):
        analysis = {"shengchen": "", "shishen": "", "xiji": "", "element_like": [], "element_dislike": []}
        lines = [l.strip() for l in content.split("\n") if l.strip()]
        section = None
        buf = []

        def flush():
            if section and buf:
                analysis[section] = " ".join(buf).strip()

        for line in lines:
            if "1. 生辰解读" in line:
                flush()
                section = "shengchen"
                buf = [line.split("：", 1)[-1].strip()] if "：" in line else []
                continue
            if "2. 十神格局" in line:
                flush()
                section = "shishen"
                buf = [line.split("：", 1)[-1].strip()] if "：" in line else []
                continue
            if "3. 五行喜忌" in line:
                flush()
                section = "xiji"
                buf = [line.split("：", 1)[-1].strip()] if "：" in line else []
                continue
            if "【五行喜忌】" in line:
                flush()
                section = None
                buf = []
                continue
            if line.startswith("喜用五行："):
                for c in line:
                    if c in ["金", "木", "水", "火", "土"]:
                        analysis["element_like"].append(c)
                continue
            if line.startswith("忌讳五行："):
                for c in line:
                    if c in ["金", "木", "水", "火", "土"]:
                        analysis["element_dislike"].append(c)
                continue
            if section:
                buf.append(line)
        flush()
        analysis["element_like"] = sorted(set(analysis["element_like"]))
        analysis["element_dislike"] = sorted(set(analysis["element_dislike"]))
        return analysis

    def analyze_mingge(self, bazi_data, gender, complete_dayun=None):
        bazi_info = self.build_bazi_info_string(bazi_data, gender)
        prompt = self.build_bazi_analysis_prompt(bazi_info, complete_dayun=complete_dayun)
        content = self._chat(SYSTEM_PROMPTS["bazi_analysis"], prompt)
        return self.parse_ai_analysis(content)

    def analyze_dayun_detail(self, bazi_data, gan_zhi, gender="男", complete_dayun=None):
        bazi_info = self.build_bazi_info_string(bazi_data, gender)
        prompt = self.build_dayun_analysis_prompt(bazi_info, gan_zhi, complete_dayun=complete_dayun)
        content = self._chat(SYSTEM_PROMPTS["bazi_analysis"], prompt)
        return content

