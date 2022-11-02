import re
from typing import List, Dict, Any

DEFAULT_EMPTY_ANS=-1000000  # if an answer cannot be parsed as an int (e.g., two ducklings or ducklings)


class Evaluator:
    def __init__(self, evaluator_name):
        self.evaluator_name : str = evaluator_name

    def evaluate(self, gold:str, stud:str, split_ans_on = "__OR__", pattern_to_retain="\{(.*?)\}") -> Dict[str, Any]:
        gold_answers = gold.split(split_ans_on)
        gold_txt_to_retain_dict = self.ans_to_ans_with_text_retain(a=gold, pattern_to_retain=pattern_to_retain)
        gold_ints = [self.ans_with_text_retain_to_int(a=gold_answer, text_retain_dict= gold_txt_to_retain_dict) for gold_answer in gold_answers]
        stud_int = self.ans_with_text_retain_to_int(a=stud, text_retain_dict= gold_txt_to_retain_dict)
        return {"is_correct": stud_int in gold_ints,
                "stud": stud_int,
                "gold": gold_ints,
                "gold_str": gold,
                "stud_str": stud
                }

    # def ans_to_ints(self, a: str, split_ans_on = "__OR__", pattern_to_retain="\{(.*?)\}") -> List[int]:
    #     answers = a.split(split_ans_on)
    #
    #     ints = [self.ans_with_text_retain_to_int(a=x,
    #                                              text_retain_dict=self.ans_to_ans_with_text_retain(
    #                                                  a=a, pattern_to_retain=pattern_to_retain)
    #                                              )
    #             for x in answers]
    #     return ints

        # for a in answers:
        #     a_s = [self.ans_to_int(a=x, text_retain_dict=text_retain_dict) for x in a.split(split_ans_on)]
        #     text_retain_dict = self.ans_to_ans_with_text_retain(a=a, pattern_to_retain=pattern_to_retain)
        #     int_ans = self.ans_with_text_retain_to_int(a=a, text_retain_dict=text_retain_dict)
        #     ints.append(int_ans) # ints can be a list [int] or an int
        #
        # if a and split_ans_on in a:
        #     a_s = [self.ans_to_int(a=x, text_retain_dict=text_retain_dict) for x in a.split(split_ans_on)]
        #     answers.append(a_s)  # answers can be a list [int] or an int
        # else:
        #     answers.append(self.ans_to_int(a=a, text_retain_dict=text_retain_dict))

    def ans_to_ans_with_text_retain(self, a: str, pattern_to_retain) -> Dict[str, int]:
        # if list_of_text_retain_dict:
        #     assert len(list_of_text_retain_dict) == len(answers), f"Challenge.init (question wise text to retain) not " \
        #                                                       f"passed correctly (length of this array must be equal " \
        #                                                       f"to number of answers i.e. {len(answers)}) and not " \
        #                                                       f"{len(list_of_text_retain_dict)}: {list_of_text_retain_dict}"
        return {x: x_id+1 for x_id, x in enumerate(re.findall(string=a, pattern=pattern_to_retain))}

    def ans_with_text_retain_to_int(self, a: str, text_retain_dict: Dict[str, int]) -> int:
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
            # if not ans and len(a) > 0:
            #     print(f"Check for preprocessing answer: input = {a}, output = {ans}")
        return int(ans) if ans else DEFAULT_EMPTY_ANS

if __name__ == '__main__':
    e = Evaluator(evaluator_name="testing")
    e.evaluate(gold="12 ducks", stud="12 duckies")