import re

diff_words = {
    'easy': ['easy', 'simple', 'light', 'straightforward', 'chill', 'relaxed'],
    'medium': ['medium', 'moderate', 'balanced', 'manageable'],
    'hard': ['hard', 'difficult', 'challenging', 'intense', 'demanding', 'tough', 'rigorous']
}

area_words = {
    'Database and Information Systems': ['data', 'database', 'information', 'text', 'mining'],
    'Artificial Intelligence': ['ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning', 'nlp', 'neural'],
    'Systems and Networking': ['systems', 'network', 'networking', 'distributed', 'cloud', 'iot'],
    'Security and Privacy': ['security', 'privacy', 'cyber', 'cryptography'],
    'Programming Languages, Formal Methods, Software Engineering': ['software engineering', 'software', 'programming', 'formal'],
    'Scientific Computing': ['numerical', 'scientific'],
    'Interactive Computing': ['graphics', 'interactive', 'visualization', '3d'],
    'Theory and Algorithms': ['theory', 'algorithm', 'automata'],
    'Architectire, Compilers, Parallel Computing': ['parallel', 'compiler', 'architecture', 'concurrent'],
    'Elective' : ['elective'],
    'Advanced Coursework' : ['advanced coursework'],
}

aspect_avoid = {
    'exam_heavy': ['no exam', 'no exams', 'without exam', 'avoid exam', 'hate exam', "don't want exam", 'dont want exam'],
    'project_based': ['no project', 'avoid project'],
    'group_work': ['no group', 'no team', 'avoid group', "don't want group"],
    'math_heavy': ['no math', 'avoid math', 'not math'],
    'reading_heavy': ['no reading', 'avoid reading']
}

aspect_want = {
    'exam_heavy': ['exam', 'exams', 'test based'],
    'project_based': ['project', 'hands on', 'practical', 'mp'],
    'group_work': ['group', 'team', 'group project'],
    'math_heavy': ['math', 'mathematical', 'theoretical',],
    'reading_heavy': ['reading', 'textbook', 'papers']
}

def parse_query(q):
    q = q.lower()
    
    result = {
        'difficulty': None,
        'areas': [],
        'want': [],
        'avoid': [],
        'workload': None,
        'prereqs_ok': True
    }
    
    for diff, words in diff_words.items():
        for w in words:
            if re.search(r'\b' + w + r'\b', q):
                result['difficulty'] = diff
                break
        if result['difficulty']:
            break
    
    for area, words in area_words.items():
        for w in words:
            if re.search(r'\b' + re.escape(w) + r'\b', q):
                if area not in result['areas']:
                    result['areas'].append(area)
                break
    
    for asp, phrases in aspect_avoid.items():
        for p in phrases:
            if p in q:
                result['avoid'].append(asp)
                break
    
    for asp, words in aspect_want.items():
        if asp in result['avoid']:
            continue
        for w in words:
            if re.search(r'\b' + w + r'\b', q):
                result['want'].append(asp)
                break
    
    if 'low workload' in q or 'light workload' in q or 'few hours' in q:
        result['workload'] = 'low'
    elif 'heavy workload' in q or 'high workload' in q:
        result['workload'] = 'high'
    
    if 'no prerequisite' in q or 'no prereq' in q or 'without prerequisite' in q:
        result['prereqs_ok'] = False
    
    return result