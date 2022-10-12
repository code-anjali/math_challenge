from typing import List, Dict

DEFAULT_EMPTY_ANS=-1000000  # if an answer cannot be parsed as an int (e.g., two ducklings or ducklings)


class Evaluator:
    evaluator_name : str

    def __init__(self, student: "StudentInfo",
                 answers:List[str],
                 challenge_name: str,
                 is_student_resp: bool,
                 list_of_text_retain_dict: List[Dict[str, int]] = {},
                 split_ans_on = "__OR__"):
        # One can add functionality here to reject a late submission (based on its timestamp, and a deadline dict)
        # but an easier solution is to not disable previous MC id in the form.
        self.is_student_resp = is_student_resp
        self.orig_answers = answers
        self.challenge_name = challenge_name
        self.answers: List[int] = []
        self.list_of_text_retain_dict = list_of_text_retain_dict
        self.student = student
        if list_of_text_retain_dict:
            assert len(list_of_text_retain_dict) == len(answers), f"Challenge.init (question wise text to retain) not " \
                                                                  f"passed correctly (length of this array must be equal " \
                                                                  f"to number of answers i.e. {len(answers)}) and not " \
                                                                  f"{len(list_of_text_retain_dict)}: {list_of_text_retain_dict}"

        for a_id, a in enumerate(answers):
            text_retain_dict = {}
            if list_of_text_retain_dict:
                text_retain_dict = list_of_text_retain_dict[a_id]
            if a and split_ans_on in a:
                a_s = [self.ans_to_int(a=x, text_retain_dict=text_retain_dict) for x in a.split(split_ans_on)]
                self.answers.append(a_s)  # answers can be a list [int] or an int
            else:
                self.answers.append(self.ans_to_int(a=a, text_retain_dict=text_retain_dict))


    @classmethod
    def load_gold_answers(cls, challenge_name_and_answers_dict, pattern_to_retain="\{(.*?)\}") -> (Dict[str, "Challenge"], Dict[str, List[Dict[str, int]]]):
        alls = {}
        challenge_wise_retaining: Dict[str, List[Dict[str, int]]] = {}
        for challenge_nm, correct_answers in challenge_name_and_answers_dict.items():
            # challenge_nm = d['Math Challenge name']
            # correct_answers = [d[f"Question {x}"] for x in range(1, 19)]
            list_of_text_retain_dict = []
            for x in correct_answers:
                list_of_text_retain_dict.append({x:x_id+1 for x_id, x in enumerate(re.findall(string=x, pattern=pattern_to_retain))})
                # text_retain_matches = re.findall(pattern=text_retain_regex, string=a) #  "\{(.*?)\}"
            #Todo
            # alls[challenge_nm] = Challenge(student=None,  # gold does not have a student name.
            #                                answers=correct_answers,
            #                                challenge_name=challenge_nm,
            #                                is_student_resp=False,
            #                                list_of_text_retain_dict=list_of_text_retain_dict)
            # challenge_wise_retaining[challenge_nm] = list_of_text_retain_dict
        return alls, challenge_wise_retaining

    @classmethod
    def ans_to_int(cls, a: str, text_retain_dict: Dict[str, int]={}) -> int:
        ans = ""
        a = a or ""
        a = a.strip().lower()
        if a.count("=") == 1:
            a = a.split("=")[-1]
        # answer is 25 ducklings
        # output = 25

        # text_retain_matches = re.findall(pattern=text_retain_regex, string=a) #  "\{(.*?)\}"
        # answer is 25 blue
        # output is 25 blue
        # if gold = 25 {blue}
        for t, t_id in text_retain_dict.items():
            replace_str = t.lower().strip()
            replace_with= f"{t_id}"
            a = a.replace(replace_str, replace_with)

        # The following code causes problems in other answers such as: a. 37th floor, b. 42nd floor, c. 39th floor, d. 40th floor
        # which becomes 3seventh floor... etc. which is wrong.
        # Instead we now have __OR__ in the gold sheet.
        # 1st bag: 20, 2nd bag:14, 3rd bag: 8, 4th bag: 18
        # Some kids write first instead of 1st
        # for k, v in {"1st": "first", "2nd": "second", "3rd": "third", "4th": "fourth", "5th": "fifth", "6th": "sixth", "7th": "seventh", "8th": "seventh"}.items():
        #     a = a.replace(k,v)

        if a:
            for ch in a:
                if ord('0') <= ord(ch) <= ord('9'):
                    ans += ch
            if not ans and len(a) > 0:
                print(f"Check for preprocessing answer: input = {a}, output = {ans}")
        return int(ans) if ans else DEFAULT_EMPTY_ANS