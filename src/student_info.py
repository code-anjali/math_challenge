from dataclasses import dataclass

@dataclass
class StudentInfo:
    email:str
    f_name:str
    l_name:str
    grade:str
    teacher:str
    school:str
    school_district="ISD"
    wants_to_be_on_leaderboard:bool=True
