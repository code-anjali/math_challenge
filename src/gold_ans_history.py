from dataclasses import dataclass
from typing import Dict

from src.gold_ans import GoldAns
from src.math_challenge import MathChallenge

@dataclass
class GoldAnsHistory:
    dict_of_mc_gold_answers: Dict[MathChallenge,GoldAns]

    def lookup_gold_ans_for(self, mc_name: str) -> GoldAns:
        key =  MathChallenge(mc_name=mc_name)
        return self.dict_of_mc_gold_answers[key]


    @staticmethod
    def create_obj(db_conn, gold_sheet_url)-> Dict[MathChallenge,GoldAns]:
        golds: Dict[MathChallenge,GoldAns] = {}
        questions_csv = ", ".join([f'"Question {x}"' for x in range(1, 19)])  # Question 1, Question 2, ... Question 18
        query = f'SELECT "Math Challenge name", {questions_csv} FROM "{gold_sheet_url}"'
        rows = db_conn.execute(query)
        for r in rows:
            mc = MathChallenge(mc_name=r[0])
            value = GoldAns(list_of_gold_answers = [x for x in r[1:]], math_challenge=mc)
            golds[mc] = value
        return golds
