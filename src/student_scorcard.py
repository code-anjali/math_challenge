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
        """
        Don't forget to call student_scorecard.compute(evaluator=evaluator)
        :param student:
        :param math_challenge:
        :param mc_gold:
        :param mc_response:
        """
        self.student : StudentInfo = student
        self.math_challenge : MathChallenge =math_challenge
        self.mc_gold : GoldAns = mc_gold
        self.mc_response : StudentAns = mc_response
        self.list_of_scores: List[bool] = []
        self.list_of_scores_with_diagnostics: List[Dict] = []
        self.passed_mc_as_per_grade : bool = False

    def passed_as_per_grade(self, num_correct : int , grade : str ) -> bool:
        """
        checks if a student passed for a grade level
        :param num_correct: 8
        :param grade: Kindergarten
        :return: True
        """
        dict_pass_as_per_grade : Dict[str, int] = {
            "Kindergarten" : 3,
            "First grade" : 3,
            "Second grade" : 7,
            "Third grade" : 7,
            "Fourth grade" : 12,
            "Fifth grade" : 12
        } #grade -> number of correct answers
        passed = num_correct >= dict_pass_as_per_grade[grade.replace("  ", " ")]  #  8 >= 3 true
        return passed

    def compute(self, evaluator: Evaluator):
        assert self.mc_gold.math_challenge == self.mc_response.math_challenge, f"student scorecard requested for mismatching mc"
        for gold, stud in zip(self.mc_gold.list_of_gold_answers, self.mc_response.list_of_student_answers):
            stud = "" if not stud else str(stud)
            eval_d = evaluator.evaluate(gold=gold, stud=stud)
            self.list_of_scores_with_diagnostics.append(eval_d)
            self.list_of_scores.append(eval_d["is_correct"])
        self.passed_mc_as_per_grade = self.passed_as_per_grade(grade=self.student.grade,
                                       num_correct=len([x for x in self.list_of_scores if x]))

    def __repr__(self):
        return "\n".join([str(x) for x in self.list_of_scores_with_diagnostics])