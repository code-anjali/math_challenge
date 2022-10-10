from dataclasses import dataclass
from typing import Dict

from src.math_challenge import MathChallenge
from src.student_ans import StudentAns
from src.student_info import StudentInfo


@dataclass

class StudentAnsHistory:
    student : StudentInfo
    list_of_mc_responses : Dict[MathChallenge,StudentAns]