import pandas as pd
import re

keywords = {
    'exam_heavy': ['exam', 'exams', 'midterm', 'final', 'test', 'tests', 'proctored', 'proctoru'],
    'project_based': ['project', 'projects', 'mp', 'mps', 'assignment', 'assignments', 'programming', 'coding'],
    'reading_heavy': ['reading', 'readings', 'textbook', 'book', 'papers'],
    'group_work': ['group', 'team', 'partner', 'collaborative', 'group project'],
    'autograded': ['autograder', 'autograded', 'auto-graded', 'automated'],
    'math_heavy': ['math', 'mathematical', 'equations', 'formula', 'proofs', 'proof'],
    'easy_grading': ['easy a', 'easy grading', 'generous', 'extra credit', 'lenient']
}

def check_aspect(text, aspect):
    text = str(text).lower()
    for kw in keywords.get(aspect, []):
        if re.search(r'\b' + re.escape(kw) + r'\b', text):
            return True
    return False

def get_aspects(text):
    return {asp: check_aspect(text, asp) for asp in keywords}

def analyze_course(reviews_df, cid):
    course_revs = reviews_df[reviews_df['course_id'].str.strip() == cid.strip()]
    if len(course_revs) == 0:
        return {}
    
    counts = {asp: 0 for asp in keywords}
    for _, row in course_revs.iterrows():
        for asp in keywords:
            if check_aspect(row['review'], asp):
                counts[asp] += 1
    
    n = len(course_revs)
    return {asp: (cnt / n) * 100 for asp, cnt in counts.items()}

def get_all_course_aspects(reviews_df, courses_df):
    result = {}
    for cid in courses_df['course_id'].unique():
        result[cid] = analyze_course(reviews_df, cid)
    return result