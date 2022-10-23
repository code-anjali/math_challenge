from dataclasses import dataclass
from typing import List

from src.math_challenge import MathChallenge
from src.student_info import StudentInfo

@dataclass
class StudentAns:
    student: StudentInfo
    math_challenge: MathChallenge
    list_of_student_answers: List[str]
