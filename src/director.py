from typing import Dict, List

from src.gold_ans_history import GoldAnsHistory
from src.gsheet_db_connector import establish_connection
from src.math_challenge import MathChallenge
from src.student_ans import StudentAns
from src.student_ans_history import StudentAnsHistory
from src.student_info import StudentInfo
from src.student_scorcard_history import StudentScorecardHistory


class Director:

    def __init__(self,in_localhost: bool, gold_ans_sheet_url: str, student_ans_sheet_url: str):
        self.db_conn = establish_connection(in_localhost=in_localhost)
        self.gold_ans_history: GoldAnsHistory = self.load_gold_ans_history(gold_ans_sheet_url=gold_ans_sheet_url)
        self.dict_student_ans_history: Dict[StudentInfo,StudentAnsHistory] = self.load_student_ans_history(student_ans_sheet_url=student_ans_sheet_url)
        self.dict_student_scorecard_history: Dict[StudentInfo,StudentScorecardHistory] = {}


    def load_student_ans_history(self, student_ans_sheet_url) -> Dict[StudentInfo,StudentAnsHistory]:
        dict_student_ans_history: Dict[StudentInfo,StudentAnsHistory] = {}

        # ans_csv = ", ".join([f'"Question {x}"' for x in range(1, 19)])  # Question 1, Question 2, ... Question 18
        # query = f'SELECT "Math Challenge name, Email Address, First Name, Last Name, School Name, Discovery Elementary Teacher name,	Grand Ridge Elementary Teacher name, "{ans_csv} FROM "{student_ans_sheet_url}"'
        query = f'SELECT * FROM "{student_ans_sheet_url}"'
        rows = self.db_conn.execute(query)
        for r in rows:
            num_cols = len(r)
            num_schools = num_cols - 24 # MC, Q1...Q18 = 19 and timestamp, email, first name, last name, school = 5
            all_schools_grade_teachers = ["" if not x else x for x in r[5:5 + num_schools]]
            grade_teacher = "".join(all_schools_grade_teachers)
            grade, teacher = grade_teacher.split(" - ")
            mc_name=r[5+num_schools]
            stud_info = StudentInfo(email= r[1], f_name=r[2], l_name=r[3], school=r[4],
                                    grade = grade, teacher = teacher, wants_to_be_on_leaderboard=True)
            stud_ans = r[1+5+num_schools: ]
            stud_ans_obj = StudentAns(student=stud_info,
                                      math_challenge=MathChallenge(mc_name=mc_name),
                                      list_of_student_answers=stud_ans)

            if stud_info not in dict_student_ans_history:
                dict_student_ans_history[stud_info] = StudentAnsHistory(student=stud_info, dict_of_mc_responses = {})
            dict_student_ans_history[stud_info].insert_mc_response(math_challenge=stud_ans_obj.math_challenge,
                                                                   student_ans=stud_ans_obj)
        return dict_student_ans_history

    def load_gold_ans_history(self, gold_ans_sheet_url) -> GoldAnsHistory:
        input_to_create_obj = GoldAnsHistory.create_obj(db_conn=self.db_conn, gold_sheet_url=gold_ans_sheet_url)
        return GoldAnsHistory(dict_of_mc_gold_answers=input_to_create_obj)

    def generate_all_student_scorecard_history(self) -> Dict[StudentInfo,StudentScorecardHistory]:
        pass


if __name__ == '__main__':
    gold_ans_sheet_url="https://docs.google.com/spreadsheets/d/1a3bLl2gMv1Ns_91sRcSTaKfKuTxM_LWPacYJ3RnhF40/edit?usp=sharing&headers=1"
    student_ans_sheet_url="https://docs.google.com/spreadsheets/d/1dIALjbxmOYP5A8hyevMRLA6fbV4fhY9g8cb_qFMITvk/edit?usp=sharing&headers=1"
    director = Director(in_localhost= True,gold_ans_sheet_url=gold_ans_sheet_url,student_ans_sheet_url=student_ans_sheet_url)