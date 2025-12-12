import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('punkt_tab', quiet=True)
stop_words = set(stopwords.words('english'))
grouper = WordNetLemmatizer()

def clean(text):
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', '', text)
    return ' '.join(text.split())

def preprocess(text):
    text = clean(text)
    tokens = word_tokenize(text)
    tokens = [grouper.lemmatize(t) for t in tokens if t not in stop_words]
    return ' '.join(tokens)

def preprocess_reviews(df):
    df = df.copy()
    df['processed_text'] = df['review'].apply(preprocess)
    return df

def preprocess_dataframe(df, text_column='review'):
    df = df.copy()
    df['processed_text'] = df[text_column].apply(preprocess)
    return df
