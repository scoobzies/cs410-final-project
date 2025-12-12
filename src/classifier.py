import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
from src.preprocess import preprocess_reviews

diff_map = {
    'very easy': 'easy',
    'easy': 'easy', 
    'medium': 'medium',
    'hard': 'hard',
    'very hard': 'hard'
}

def load_and_prep(path):
    df = pd.read_csv(path)
    df['label'] = df['difficulty_rating'].apply(lambda x: diff_map.get(str(x).lower().strip(), 'medium'))
    df = preprocess_reviews(df)
    return df

def train_model(reviews_path='data/reviews.csv'):
    df = load_and_prep(reviews_path)
    
    X = df['processed_text'].tolist()
    y = df['label'].tolist()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y)
    
    vec = TfidfVectorizer(max_features=800, ngram_range=(1,2))
    X_train_tfidf = vec.fit_transform(X_train)
    X_test_tfidf = vec.transform(X_test)
    
    clf = MultinomialNB()
    clf.fit(X_train_tfidf, y_train)
    
    preds = clf.predict(X_test_tfidf)
    print(f"Accuracy: {accuracy_score(y_test, preds):.2%}")
    print(classification_report(y_test, preds))
    
    vec_full = TfidfVectorizer(max_features=800, ngram_range=(1,2))
    X_full = vec_full.fit_transform(X)
    clf_full = MultinomialNB()
    clf_full.fit(X_full, y)
    
    with open('models/classifier.pkl', 'wb') as f:
        pickle.dump({'clf': clf_full, 'vec': vec_full}, f)
    
    print("saved model to models/classifier.pkl")

def load_model():
    with open('models/classifier.pkl', 'rb') as f:
        data = pickle.load(f)
    return data['clf'], data['vec']

def predict_difficulty(text, clf, vec):
    from src.preprocess import preprocess
    processed = preprocess(text)
    tfidf = vec.transform([processed])
    return clf.predict(tfidf)[0]

if __name__ == "__main__":
    train_model()