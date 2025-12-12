import pandas as pd
from src.aspect_analyzer import get_all_course_aspects
from src.query_parser import parse_query

diff_to_num = {'very easy': 1, 'easy': 2, 'medium': 3, 'hard': 4, 'very hard': 5}
num_to_label = {1: 'easy', 2: 'easy', 3: 'medium', 4: 'hard', 5: 'hard'}

courses_df = None
reviews_df = None
course_aspects = None
course_stats = None

def init(courses_path='data/courses.csv', reviews_path='data/reviews.csv'):
    global courses_df, reviews_df, course_aspects, course_stats
    
    courses_df = pd.read_csv(courses_path)
    reviews_df = pd.read_csv(reviews_path)
    course_aspects = get_all_course_aspects(reviews_df, courses_df)
    course_stats = {}
    
    for cid in courses_df['course_id'].unique():
        revs = reviews_df[reviews_df['course_id'].str.strip() == cid.strip()]
        
        if len(revs) == 0:
            course_stats[cid] = {'diff': 3, 'diff_label': 'medium', 'workload': 10, 'n_reviews': 0}
            continue
        
        diffs = revs['difficulty_rating'].str.lower().str.strip().map(diff_to_num)
        avg_diff = diffs.mean() if not diffs.isna().all() else 3
        
        wls = pd.to_numeric(revs['workload'], errors='coerce')
        avg_wl = wls.mean() if not wls.isna().all() else 10
        
        course_stats[cid] = {
            'diff': avg_diff,
            'diff_label': num_to_label.get(round(avg_diff), 'medium'),
            'workload': avg_wl,
            'n_reviews': len(revs)
        }

def get_difficulty(cid):
    if course_stats is None:
        init()
    return course_stats.get(cid, {}).get('diff_label', 'medium')

def get_workload(cid):
    if course_stats is None:
        init()
    return course_stats.get(cid, {}).get('workload', 10)

def recommend(query, n=5):
    if courses_df is None:
        init()
    
    parsed = parse_query(query)
    
    df = courses_df.copy()
    df['diff_label'] = df['course_id'].apply(get_difficulty)
    df['workload'] = df['course_id'].apply(get_workload)
    df['n_reviews'] = df['course_id'].apply(lambda x: course_stats.get(x, {}).get('n_reviews', 0))
    
    if not parsed['prereqs_ok']:
        df = df[df['has_prerequisites'] == 'none']
    
    if parsed['areas']:
        mask = df['breadth_area'].apply(lambda x: any(a.lower() in str(x).lower() for a in parsed['areas']))
        if mask.any():
            df = df[mask]
    
    if parsed['difficulty']:
        df = df[df['diff_label'] == parsed['difficulty']]
    
    df['score'] = 0.0
    
    if parsed['workload'] == 'low':
        df['score'] -= df['workload'] / 5
    elif parsed['workload'] == 'high':
        df['score'] += df['workload'] / 5
    
    for asp in parsed['avoid']:
        df['score'] += df['course_id'].apply(lambda x: -3 if course_aspects.get(x, {}).get(asp, 0) > 30 else 0)
    
    for asp in parsed['want']:
        df['score'] += df['course_id'].apply(lambda x: 2 if course_aspects.get(x, {}).get(asp, 0) > 30 else 0)
    
    df['score'] += df['n_reviews'] / 100
    
    if len(df) == 0:
        df = courses_df.copy()
        df['diff_label'] = df['course_id'].apply(get_difficulty)
        df['workload'] = df['course_id'].apply(get_workload)
        df['n_reviews'] = df['course_id'].apply(lambda x: course_stats.get(x, {}).get('n_reviews', 0))
        df['score'] = 0.0
        
        if parsed['difficulty']:
            diff_scores = {'easy': 1, 'medium': 2, 'hard': 3}
            target = diff_scores.get(parsed['difficulty'], 2)
            df['score'] += df['diff_label'].apply(lambda x: -abs(diff_scores.get(x, 2) - target) * 5)
    
    return df.sort_values('score', ascending=False).head(n)

def get_details(cid):
    if courses_df is None:
        init()
    
    info = courses_df[courses_df['course_id'] == cid]
    if len(info) == 0:
        return None
    
    result = info.iloc[0].to_dict()
    result['stats'] = course_stats.get(cid, {})
    result['aspects'] = course_aspects.get(cid, {})
    
    revs = reviews_df[reviews_df['course_id'].str.strip() == cid.strip()]
    result['sample_reviews'] = revs['review'].tolist()[:3]
    
    return result