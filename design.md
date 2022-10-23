# math_challenge

math challenge has 5 major tasks
1. Promotion
2. Submission
3. Evaluation and assignment review
4. Leaderboard
5. Celebration

This repository contains code to perform evaluation of the submissions and to generate a leaderboard as well as reviewing assignments.

Functionality for evaluation
- A student submits answers for a math challenge.
- There is an answer sheet against which every submission must be evaluated.
- To evaluate an MC response an evaluator compares the student answer with gold answer for every question.
- Based on the grade of the student a passing score is determined and MC is considered successful if the student scores are at or above the passing score.

#To-do
read gold file and student answers from sheet url


Director
dict_student_ans_history: Dict[StudentInfo,StudentAnsHistory]
dict_student_scorecard_history: Dict[StudentInfo,StudentScorecardHistory]
dict_gold_ans_history: GoldAnsHistory
def load_student_ans_history(file_path_or_sheet_url) -> Dict[StudentInfo,StudentAnsHistory]
def load_gold_ans_history(file_path_or_sheet_url) -> Dict[MathChallenge,GoldAnsHistory]
def generate_all_student_scorecard_history() -> Dict[StudentInfo,StudentScorecardHistory]
def search_scorecard_history_by_email(List of email ids) -> List[StudentRecords]

StudentInfo
email: str
f_name : str
l_name : str
grade : str
teacher : str
school : str
school_district : str
wants_to_be_on_leaderboard: bool= True


MathChallenge
mc_name: str
questions: List[str]

StudentAnsHistory
student: StudentInfo
list_of_mc_responses: Dict[MathChallenge, StudentAns]

StudentAns (prev called Challenge)
student: StudentInfo    
math_challenge: MathChallenge
list_of_student_answers: List[str]


GoldAnsHistory
dict_of_mc_gold_answers: Dict[MathChallenge, GoldAns]
def load_from_file(file_path) -> GoldAnsHistory
def lookup_gold_ans_for(mc_name) -> GoldAns

GoldAns
math_challenge: MathChallenge
list_of_gold_answers: List[str]

StudentScorecardHistory (from MathChallengeResult.summarize)
student: StudentInfo
dict_of_mc_scorecards: Dict[MathChallenge, Scorecard]

StudentScorecard
student: StudentInfo
math_challenge: MathChallenge
mc_gold: GoldAns
mc_response: StudentAns
list_of_scores: List[bool]
def is_passed() -> bool

QuesEvaluator
def evaluate(student_ans, gold_ans) -> bool


Note: previous code: https://github.com/code-anjali/gsheetdb_tutorial/blob/08201d3f1d877ecccf6e147c0fc1e9e86286a756/math_challenge_related/challenge_result_checker.py


    





