from typing import List, Dict

from src.evaluator import Evaluator
from src.gold_ans import GoldAns
from src.math_challenge import MathChallenge
from src.student_ans import StudentAns
from src.student_info import StudentInfo



class StudentScorecard:
    def __init__(self,
                 student: StudentInfo,
                 math_challenge: MathChallenge,
                 mc_gold: GoldAns,
                 mc_response: StudentAns):
        self.student = student
        self.math_challenge=math_challenge
        self.mc_gold = mc_gold
        self.mc_response = mc_response
        self.list_of_scores: List[bool] = []
        self.list_of_scores_with_diagnostics: List[Dict] = []

    def compute(self, evaluator: Evaluator):
        assert self.mc_gold.math_challenge == self.mc_response.math_challenge, f"student scorecard requested for mismatching mc"
        for gold, stud in zip(self.mc_gold.list_of_gold_answers, self.mc_response.list_of_student_answers):
            eval_d = evaluator.evaluate(gold=gold, stud=stud)
            self.list_of_scores_with_diagnostics.append(eval_d)
            self.list_of_scores.append(eval_d["is_correct"])