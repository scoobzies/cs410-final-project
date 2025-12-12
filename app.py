import streamlit as st
import pandas as pd
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src import recommender
from src.query_parser import parse_query

st.set_page_config(page_title="FALL Online MCS Course Scheduler", layout="wide")

st.title("FALL Online MCS Course Scheduler")
st.write("*MCS course recommendations using NLP*")

recommender.init()

st.header("What course are you looking for?")

query = st.text_area("Describe the course you want:", height=100, 
    placeholder="Example: I want an easy AI course with no exams")

n_results = st.selectbox("Number of results", [1,2, 3, 4, 5], index=1)

if st.button("Search", type="primary"):
    if query.strip():
        parsed = parse_query(query)
        
        with st.expander("NLP Analysis"):
            if parsed['difficulty']:
                st.write(f"Difficulty: {parsed['difficulty']}")
            if parsed['areas']:
                st.write(f"Areas: {', '.join(parsed['areas'])}")
            if parsed['want']:
                st.write(f"Looking for: {', '.join(parsed['want'])}")
            if parsed['avoid']:
                st.write(f"Avoiding: {', '.join(parsed['avoid'])}")
            if parsed['workload']:
                st.write(f"Workload: {parsed['workload']}")
        
        st.header("Results")
        
        results = recommender.recommend(query, n=n_results)
        
        if len(results) == 0:
            st.warning("No matches found")
        else:
            for _, row in results.iterrows():
                cid = row['course_id']
                details = recommender.get_details(cid)
                
                with st.expander(f"{cid}: {row['course_name']}", expanded=True):
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Difficulty", row['diff_label'].title())
                    c2.metric("Workload", f"{row['workload']:.0f} hrs/wk")
                    c3.metric("Reviews", row['n_reviews'])
                    
                    if row['description'] and row['description'] != 'N/A':
                        st.write(f"**Description:** {str(row['description'])[:300]}...")
                    
                    st.write(f"**Breadth Area:** {row['breadth_area']}")
                    
                    if row['has_prerequisites'] != 'none':
                        st.write(f"**Prerequisites:** {row['has_prerequisites']}")
                    
                    if details and details.get('aspects'):
                        asp = details['aspects']
                        tags = []
                        if asp.get('exam_heavy', 0) > 50: tags.append("Exam-heavy")
                        if asp.get('project_based', 0) > 50: tags.append("Project-based")
                        if asp.get('group_work', 0) > 50: tags.append("Group work")
                        if asp.get('math_heavy', 0) > 30: tags.append("Math-heavy")
                        if tags:
                            st.write("**Tags:** " + " | ".join(tags))
                    
                    if details and details.get('sample_reviews'):
                        st.write("**Sample review:**")
                        rev = details['sample_reviews'][0]
                        st.write(f"> {rev[:400]}..." if len(rev) > 400 else f"> {rev}")
    else:
        st.warning("Enter a query first")

st.markdown("---")

t1, t2 = st.tabs(["All Courses", "Stats"])

with t1:
    df = recommender.courses_df.copy()
    df['Difficulty'] = df['course_id'].apply(recommender.get_difficulty)
    df['Workload'] = df['course_id'].apply(lambda x: f"{recommender.get_workload(x):.0f}")
    st.dataframe(df[['course_id', 'course_name', 'Difficulty', 'Workload', 'breadth_area']], use_container_width=True)

with t2:
    rows = []
    for cid in recommender.courses_df['course_id']:
        s = recommender.course_stats.get(cid, {})
        a = recommender.course_aspects.get(cid, {})
        rows.append({
            'Course': cid,
            'Reviews': s.get('n_reviews', 0),
            'Difficulty': f"{s.get('diff', 0):.1f}/5",
            'Workload': f"{s.get('workload', 0):.0f}h",
            'Exams': f"{a.get('exam_heavy', 0):.0f}%",
            'Projects': f"{a.get('project_based', 0):.0f}%",
            'Group': f"{a.get('group_work', 0):.0f}%"
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True)