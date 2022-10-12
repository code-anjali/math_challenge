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

    def __hash__(self):
        return hash((self.email,self.f_name,self.l_name,self.grade, self.school))

    def __eq__(self, other):
        return (self.email,self.f_name,self.l_name,self.grade, self.school)== (other.email,other.f_name,other.l_name,other.grade, other.school)
