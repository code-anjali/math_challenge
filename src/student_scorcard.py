from dataclasses import dataclass
from typing import List

from src.gold_ans import GoldAns
from src.math_challenge import MathChallenge
from src.student_ans import StudentAns
from src.student_info import StudentInfo


@dataclass
class StudentScorecard:
    student: StudentInfo
    math_challenge: MathChallenge
    mc_gold: GoldAns
    mc_response: StudentAns
    list_of_scores: List[bool]