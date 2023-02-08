import streamlit as st

import sys
sys.path.append('.')
sys.path.append('src')

from src.director import Director

def leaderboard_html_tbl(out_fp, leaderboard_data):
    with open(out_fp, 'w') as o_table_handle:
        o_table_handle.write(""" <html> 
                <head>
                <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <style>
    
    table {
      border-collapse: collapse;
      width: 80%;
    }
    
    th, td {
      padding: 8px;
      text-align: left;
      border-bottom: 1px solid #DDD;
    }
    
    tr:hover {background-color: #D6EEEE;}
    
    #search_query {
      background-image: url('/css/searchicon.png');
      background-position: 10px 10px;
      background-repeat: no-repeat;
      width: 80%;
      font-size: 16px;
      padding: 12px 20px 12px 40px;
      border: 1px solid #ddd;
      margin-bottom: 12px;
    }
    
    div.gallery {
      margin: 5px;
      border: 1px solid #ccc;
      float: left;
      width: 180px;
    }
    
    div.gallery:hover {
      border: 1px solid #777;
    }
    
    table td, table td * {
        vertical-align: top;
    }
    </style>
    
    <script>
    function search_by_any_column() {
      var input, filter, table, tr, td, i, txtValue;
      input = document.getElementById("search_query");
      filter = input.value.toUpperCase();
      table = document.getElementById("finalists");
      tr = table.getElementsByTagName("tr");
      for (i = 0; i < tr.length; i++) {
        td_studentname = tr[i].getElementsByTagName("td")[0];
        td_grade = tr[i].getElementsByTagName("td")[1];
        td_teacher = tr[i].getElementsByTagName("td")[2];
        td_score = tr[i].getElementsByTagName("td")[3];
        
        if (td_studentname) {
          studentValue = td_studentname.textContent || td_studentname.innerText;
          gradeValue = td_grade.textContent || td_grade.innerText;
          teacherValue = td_teacher.textContent || td_teacher.innerText;
          scoreValue = td_score.textContent || td_score.innerText;
          
          if (studentValue.toUpperCase().indexOf(filter) > -1 || gradeValue.toUpperCase().indexOf(filter) > -1 || teacherValue.toUpperCase().indexOf(filter) > -1 || scoreValue.toUpperCase().indexOf(filter) > -1 ) {
            tr[i].style.display = "";
          } else {
            tr[i].style.display = "none";
          }
        }
        
               
      }
    }
    </script>
    
    </head>
                
                <body> <br>
                <h3><h3>Math challenge 2022-23 Leaderboard 🏆 (Discovery Elementary)</h3><br></h3>
                <br>
                
                <input type="text" id="search_query" onkeyup="search_by_any_column()" placeholder="Search..." title="Type in a name">
    
                <table id="finalists" style="border: 1px"> 
                    <tr>
                        <th>Student name</th> 
                        <th>Grade</th>
                        <th>Teacher</th>
                        <th>Score</th>
                    </tr>
                    """)
        for ld in leaderboard_data:
            o_table_handle.write(f"""<tr>
                    <td>{ld['name']}</td>
                    <td>{ld['grade']}</td> 
                    <td>{ld['teacher']}</td> 
                    <td>{ld['score']}</td> 
                    </tr>""")
        o_table_handle.write("\n</table><br><br><hr><br>")
        o_table_handle.write("</body></html>")

    print(f"Saving results file to {out_fp}")


def main():
    st.set_page_config(layout="wide")
    if "director" not in st.session_state:
        gold_ans_sheet_url="https://docs.google.com/spreadsheets/d/1a3bLl2gMv1Ns_91sRcSTaKfKuTxM_LWPacYJ3RnhF40/edit?usp=sharing&headers=1"
        student_ans_sheet_url="https://docs.google.com/spreadsheets/d/1dIALjbxmOYP5A8hyevMRLA6fbV4fhY9g8cb_qFMITvk/edit?usp=sharing&headers=1"
        director = Director(in_localhost= False,gold_ans_sheet_url=gold_ans_sheet_url,student_ans_sheet_url=student_ans_sheet_url, override_prev_answers=True)
        # cache director in streamlit cache
        st.session_state["director"] = director

    whitelisted = {"Shreya Bulusu"}
    with st.form("form1"):
        st.title("Leaderboard.")
        min_scorecard = int(st.number_input("min. qualification for leaderboard", min_value=1, max_value=20, step=1))
        school = st.selectbox(label="school", options=["Discovery Elementary", "Grand Ridge Elementary"])
        user_clicked = st.form_submit_button(label="Generate leaderboard")
        if user_clicked:
            scorecards = {student: scorecard.num_accepted_mcs() for student, scorecard in st.session_state["director"].dict_student_scorecard_history.items()}
            scorecards_sorted = sorted(scorecards.items(), key=lambda x: x[1], reverse=True)
            finalists = []

            for student_score in scorecards_sorted:
                if student_score[0].school != school:
                    continue
                if f"{student_score[0].f_name} {student_score[0].l_name}" in whitelisted:
                    continue
                if int(student_score[1]) >= min_scorecard:
                    finalists.append({"name": f"{student_score[0].f_name} {student_score[0].l_name[0]}.",
                                     "grade": student_score[0].grade,
                                     "teacher": student_score[0].teacher,
                                     "score": 100*student_score[1]})


            st.json(finalists)
            out_fp = f"/tmp/{school.lower().replace(' ', '-')}-leaderboard.html"
            leaderboard_html_tbl(out_fp=out_fp, leaderboard_data=finalists)
            st.write()
            st.write(f"Number of finalists = {len(finalists)}")
            st.write(f"Output in file://{out_fp}")



if __name__ == '__main__':
    main()
