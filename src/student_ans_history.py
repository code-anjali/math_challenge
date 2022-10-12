from dataclasses import dataclass
from typing import Dict

from src.math_challenge import MathChallenge
from src.student_ans import StudentAns
from src.student_info import StudentInfo


@dataclass

class StudentAnsHistory:
    student : StudentInfo
    dict_of_mc_responses : Dict[MathChallenge, StudentAns]

    def insert_mc_response(self, math_challenge: MathChallenge, student_ans: StudentAns):
        if not self.dict_of_mc_responses:
            self.dict_of_mc_responses = {}
        if math_challenge not in self.dict_of_mc_responses:
            self.dict_of_mc_responses[math_challenge] = student_ans