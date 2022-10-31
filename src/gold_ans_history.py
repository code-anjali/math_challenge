from dataclasses import dataclass
from typing import Dict

from src.gold_ans import GoldAns
from src.math_challenge import MathChallenge

@dataclass
class GoldAnsHistory:
    dict_of_mc_gold_answers: Dict[MathChallenge,GoldAns]

    def lookup_gold_ans_for(self, mc_challenge: MathChallenge) -> GoldAns:
        return self.dict_of_mc_gold_answers.get(mc_challenge, GoldAns(mc_challenge))


    @staticmethod
    def create_obj(db_conn, gold_sheet_url)-> Dict[MathChallenge,GoldAns]:
        golds: Dict[MathChallenge,GoldAns] = {}
        questions_csv = ", ".join([f'"Question {x}"' for x in range(1, 19)])  # Question 1, Question 2, ... Question 18
        query = f'SELECT "Math Challenge name", {questions_csv} FROM "{gold_sheet_url}"'
        rows = db_conn.execute(query)

        for r in rows:
            is_display_ans = "display" in r[0] or "original" in r[0]
            mc = MathChallenge(mc_name=r[0].split("_")[-1])  # r[0] = MC1, r[0] = display_MC1 =>extract MC1
            if mc not in golds:
                value = GoldAns(math_challenge=mc)
                golds[mc] = value

            answers = [x for x in r[1:]]
            if is_display_ans:
                golds[mc].set_display_answers(answers)
            else:
                golds[mc].set_gold_answers(answers)

        return golds
