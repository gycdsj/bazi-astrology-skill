import unittest
from datetime import datetime

from analysis_skill import BaziAnalysisSkill


class ResolveTargetDatetimeTest(unittest.TestCase):
    def setUp(self):
        self.reference = datetime(2026, 5, 16, 14, 30)

    def test_invalid_full_date_clamps_to_month_end(self):
        target, note = BaziAnalysisSkill.resolve_target_datetime(
            "2026年2月30日考试怎么样",
            reference_datetime=self.reference,
        )

        self.assertEqual(target, datetime(2026, 2, 28, 14, 30))
        self.assertIn("日期不存在", note)

    def test_invalid_month_falls_back_to_reference_date(self):
        target, note = BaziAnalysisSkill.resolve_target_datetime(
            "13月1日考试怎么样",
            reference_datetime=self.reference,
        )

        self.assertEqual(target, self.reference)
        self.assertIn("月份无效", note)

    def test_temporal_context_handles_invalid_date_without_crashing(self):
        skill = BaziAnalysisSkill(client=object(), model="dummy")
        inputs = skill.build_analysis_inputs_from_birth(
            year=1992,
            month=8,
            day=9,
            hour=11,
            minute=50,
            gender="男",
            reference_datetime=self.reference,
        )

        context = skill.build_temporal_context_for_question(
            "2026年2月30日考试怎么样",
            bazi_data=inputs["bazi_data"],
            complete_dayun=inputs["complete_dayun"],
            reference_datetime=self.reference,
        )

        self.assertIn("目标公历日期：2026-02-28", context)
        self.assertIn("日期不存在", context)


if __name__ == "__main__":
    unittest.main()
