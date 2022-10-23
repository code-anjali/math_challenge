from dataclasses import dataclass
from typing import Dict

from src.math_challenge import MathChallenge
from src.student_info import StudentInfo
from src.student_scorcard import StudentScorecard

@dataclass
class StudentScorecardHistory:
    student: StudentInfo
    dict_of_mc_scorecards: Dict[MathChallenge, StudentScorecard]

    def __repr__(self):
        arr = [f"\n{mc}\n{sscard}" for mc, sscard in self.dict_of_mc_scorecards.items()]
        arr_str = "\n\n".join(arr)
        return f"Student = {self.student} \n{arr_str}"
