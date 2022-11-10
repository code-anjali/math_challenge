import logging
from dataclasses import dataclass
from typing import Dict, List

import pandas as pd
from pandas import DataFrame
from pandas.io.formats.style import Styler

from src import student_info
from src.evaluator import Evaluator
from src.gold_ans_history import GoldAnsHistory
from src.gsheet_db_connector import establish_connection
from src.math_challenge import MathChallenge
from src.student_ans import StudentAns
from src.student_ans_history import StudentAnsHistory
from src.student_info import StudentInfo
from src.student_scorcard import StudentScorecard
from src.student_scorcard_history import StudentScorecardHistory


@dataclass
class DecoratedResult:
    student_info: StudentInfo
    pd_df: DataFrame
    pd_styler: Styler
    diagnostics: Dict[MathChallenge, StudentScorecard]


class Director:

    def __init__(self,
                 in_localhost: bool,
                 gold_ans_sheet_url: str,
                 student_ans_sheet_url: str,
                 override_prev_answers: bool):
        self.db_conn = establish_connection(in_localhost=in_localhost)
        self.evaluator = Evaluator(evaluator_name= "math_evaluator")
        self.gold_ans_history: GoldAnsHistory = self.load_gold_ans_history(gold_ans_sheet_url=gold_ans_sheet_url)
        self.dict_student_ans_history: Dict[StudentInfo,StudentAnsHistory] = self.load_student_ans_history(student_ans_sheet_url=student_ans_sheet_url, override_prev_answers=override_prev_answers)
        self.dict_student_scorecard_history: Dict[StudentInfo,StudentScorecardHistory] = self.generate_all_student_scorecard_history()


    def load_student_ans_history(self, student_ans_sheet_url: str, override_prev_answers:bool) -> Dict[StudentInfo,StudentAnsHistory]:
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
                                      list_of_student_answers=["" if not x else str(x) for x in stud_ans])

            if stud_info not in dict_student_ans_history:
                dict_student_ans_history[stud_info] = StudentAnsHistory(student=stud_info, dict_of_mc_responses = {})
            dict_student_ans_history[stud_info].insert_mc_response(math_challenge=stud_ans_obj.math_challenge,
                                                                   student_ans=stud_ans_obj,
                                                                   override_prev_answers=override_prev_answers)
        return dict_student_ans_history

    def load_gold_ans_history(self, gold_ans_sheet_url) -> GoldAnsHistory:
        input_to_create_obj = GoldAnsHistory.create_obj(db_conn=self.db_conn, gold_sheet_url=gold_ans_sheet_url)
        return GoldAnsHistory(dict_of_mc_gold_answers=input_to_create_obj)

    def generate_all_student_scorecard_history(self) -> Dict[StudentInfo,StudentScorecardHistory]:
        dict_student_scorecard_hist: Dict[StudentInfo,StudentScorecardHistory] = {}

        for student_info, student_ans_history in self.dict_student_ans_history.items():
            dict_of_mc_scorecards: Dict[MathChallenge, StudentScorecard] = {}
            for mc_challenge, student_ans in student_ans_history.dict_of_mc_responses.items():
                gold_ans = self.gold_ans_history.lookup_gold_ans_for(mc_challenge)
                student_scorecard = StudentScorecard(student=student_info, math_challenge=mc_challenge, mc_gold=gold_ans, mc_response=student_ans)
                student_scorecard.compute(evaluator=self.evaluator)
                if mc_challenge not in dict_of_mc_scorecards:
                    dict_of_mc_scorecards[mc_challenge]= student_scorecard


            student_scorecard_history = StudentScorecardHistory(student=student_info,
                                                                dict_of_mc_scorecards=dict_of_mc_scorecards)
            if student_info not in dict_student_scorecard_hist:
                dict_student_scorecard_hist[student_info] = student_scorecard_history

        return dict_student_scorecard_hist


    def search_scorecard_history_by_email(self,query_email_ids : List[str]) -> List[StudentScorecardHistory]:
        searched_student_history : List[StudentScorecardHistory] = []
        for student_info, student_scorecard_history in self.dict_student_scorecard_history.items():
            if student_info.email in query_email_ids:
                searched_student_history.append(student_scorecard_history)
        return searched_student_history


    def decorated_student_ans(self, answers : List[str], marking : List[bool], mc_passed):
        # U+2714 -> \U00002714
        return ["\U0001F44D" if mc_passed else "\U0001F44E"] + \
               [(ans or "") + "  " + ("\U00002714" if corr else "\N{cross mark}") for ans, corr in zip(answers, marking)]


    def prepare_results(self, matching_records: List[StudentScorecardHistory]) -> List[DecoratedResult]:
        """
        format the results for display
        :param matching_records: all mc scorecard history matched by searched email
        :return: for every scorecard history return a decorated result

        StudentScorecardHistory (student: StudentInfo, dict_of_mc_scorecards: Dict[MathChallenge, StudentScorecard])
        e.g.
        "MC1" -> StudentScoreCard
                    student : StudentInfo
                    math_challenge : MathChallenge
                    mc_gold : GoldAns
                    mc_response : StudentAns
                    list_of_scores: List[bool]
                    list_of_scores_with_diagnostics: List[Dict]
                    passed_mc_as_per_grade : bool

        "MC2" -> StudentScoreCard
                   ....

        DecoratedResult
            student_info: StudentInfo
            pd_df: DataFrame
            pd_styler: Styler
            diagnostics: Dict[MathChallenge, StudentScorecard]

        Note: If        : this error is encountered --
                          ValueError: could not convert string to float: '6,931'
              Then      : Google sheets- Format -> number -> plain text
        """

        list_of_decorated_results : List[DecoratedResult] = []
        for undecorated_result in matching_records:
            try:
                pd_df, pd_styler = self.write_to_pd_frame(undecorated_result.dict_of_mc_scorecards)
                d = DecoratedResult(student_info = undecorated_result.student,
                                    diagnostics= undecorated_result.dict_of_mc_scorecards,
                                    pd_df=pd_df,
                                    pd_styler=pd_styler)
                list_of_decorated_results.append(d)
            except Exception as exc:
                print(f"Exception {exc} in decorating result: {undecorated_result}")
        return list_of_decorated_results

    def write_to_pd_frame(self, dict_of_mc_scorecards : Dict[MathChallenge, StudentScorecard])-> (DataFrame, Styler):
        """

        :param dict_of_mc_scorecards:
        :return:
        """
        final_rows = []
        num_ques = 18
        header_row = ["MC"] + [f'"Q {x}"' for x in range(1, num_ques+1)]
        empty_row  = [""]* (num_ques + 1)
        final_rows.append(header_row)

        for mc, scorecard in dict_of_mc_scorecards.items():
            final_rows.append([mc.mc_name] + scorecard.mc_gold.list_of_display_gold_answers)
            final_rows.append(self.decorated_student_ans(
                answers=scorecard.mc_response.list_of_student_answers,
                marking=scorecard.list_of_scores,
                mc_passed=scorecard.passed_mc_as_per_grade
            ))
            final_rows.append(empty_row)

        undecorated_data = pd.DataFrame([row for row in final_rows], columns=header_row)

        decorated_data = undecorated_data.style.set_table_styles([{
            'selector': 'tr:hover',
            'props': 'font-size: 1.01em;'
        }])

        decorated_df = decorated_data.applymap(lambda x: 'background-color : lightblue' if len(x) < 1 else '')
        return undecorated_data, decorated_df


if __name__ == '__main__':
    gold_ans_sheet_url="https://docs.google.com/spreadsheets/d/1a3bLl2gMv1Ns_91sRcSTaKfKuTxM_LWPacYJ3RnhF40/edit?usp=sharing&headers=1"
    student_ans_sheet_url="https://docs.google.com/spreadsheets/d/1dIALjbxmOYP5A8hyevMRLA6fbV4fhY9g8cb_qFMITvk/edit?usp=sharing&headers=1"
    director = Director(in_localhost= True,gold_ans_sheet_url=gold_ans_sheet_url,student_ans_sheet_url=student_ans_sheet_url, override_prev_answers=True)
    print("done.")
    user_query = ""
    while user_query!= "quit":
        user_query = input("\n\nEnter parent email id (csv) to view scorecard history: ")
        results = director.search_scorecard_history_by_email(query_email_ids=[x.lower().strip() for x in user_query.split(",")])
        for r in director.prepare_results(results):
            print(r.pd_df)
