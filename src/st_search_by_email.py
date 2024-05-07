import streamlit as st

import sys
sys.path.append('.')
sys.path.append('src')

from src.director import Director

if __name__ == '__main__':
    st.set_page_config(layout="wide")
    if "director" not in st.session_state:
        # Following two were for 2022-23
        # gold_ans_sheet_url="https://docs.google.com/spreadsheets/d/1a3bLl2gMv1Ns_91sRcSTaKfKuTxM_LWPacYJ3RnhF40/edit?usp=sharing&headers=1"
        # student_ans_sheet_url="https://docs.google.com/spreadsheets/d/1dIALjbxmOYP5A8hyevMRLA6fbV4fhY9g8cb_qFMITvk/edit?usp=sharing&headers=1"
        
        # These should be for 2023-24
        # gold_ans_sheet_url="https://docs.google.com/spreadsheets/d/1a3bLl2gMv1Ns_91sRcSTaKfKuTxM_LWPacYJ3RnhF40/edit?usp=sharing&headers=1"
        # # OLD: student_ans_sheet_url="https://docs.google.com/spreadsheets/d/1dIALjbxmOYP5A8hyevMRLA6fbV4fhY9g8cb_qFMITvk/edit?usp=sharing&headers=1"
        # student_ans_sheet_url="https://docs.google.com/spreadsheets/d/1Y4nLkTxDGMaDYj3quIMDwUjDjGdCpIHj8KS5I2eOwWc/edit?usp=sharing&headers=1"
        gold_ans_sheet_url="https://docs.google.com/spreadsheets/d/1a3bLl2gMv1Ns_91sRcSTaKfKuTxM_LWPacYJ3RnhF40/edit?usp=sharing&headers=1"
        # (OLD ONE) student_ans_sheet_url="https://docs.google.com/spreadsheets/d/10PQd-zF7uWTv8EkZtVjTyoTT-sMt_kx7M9Kwa8W0kOk/edit?usp=sharing"
        
        # TODO (Niket) use gsheet_names to get the correct sheet
        student_ans_sheet_url="https://docs.google.com/spreadsheets/d/1Y4nLkTxDGMaDYj3quIMDwUjDjGdCpIHj8KS5I2eOwWc/edit?usp=sharing&headers=1"
        # https://docs.google.com/spreadsheets/d/1a3bLl2gMv1Ns_91sRcSTaKfKuTxM_LWPacYJ3RnhF40/edit?usp=sharing&headers=1
        
        director = Director(in_localhost= False,gold_ans_sheet_url=gold_ans_sheet_url,student_ans_sheet_url=student_ans_sheet_url, override_prev_answers=True)
        # cache director in streamlit cache
        st.session_state["director"] = director

    with st.form("form1"):
        st.title("Results.")
        student_query = st.text_input("Look up by parent email ids (separate by comma if you used multiple email ids)")
        user_clicked = st.form_submit_button(label="Generate report")
        if user_clicked:
            student_query = student_query.replace("  "," ").strip().lower()
            results = st.session_state["director"].search_scorecard_history_by_email(query_email_ids=[x.lower().strip() for x in student_query.split(",")])
            for decorated_result in st.session_state["director"].prepare_results(results):
                st.write(" ")
                st.write("----------------------------------------")
                st.write(f"**{decorated_result.student_info.f_name}** {decorated_result.student_info.l_name} - {decorated_result.student_info.grade} - School {decorated_result.student_info.school}")
                st.write("----------------------------------------")
                try:
                    st.table(decorated_result.pd_styler)
                except Exception as exc:
                    print(f"Exception in displaying decorated table: {exc}.")
                    st.table(decorated_result.pd_df)
