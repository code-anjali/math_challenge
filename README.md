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

List of potential classes
Student
Math_challenge
mc_response
    student
    math_challenge
    list_of_mc_responses (response)
mc_gold
    dict_of_mc_goldans (math_challenge -> ans)
    def load_from_file(file_path)
scorecard
    student
    dict_of_mc_gradings (math_challenge -> grading)
    def pass_fail(student, math_challenge, mc_evaluation)
mc_evaluator
    mc_gold
    mc_response
    question_gradings
    def evaluate(student_ans,gold_ans) -> yes_no



    





