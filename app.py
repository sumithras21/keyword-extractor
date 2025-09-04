import pickle
from flask import Flask, render_template, request
import re
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

app = Flask(__name__)

# Load pickled files & data
cv = pickle.load(open('count_vectorizer.pkl', 'rb'))
tfidf_transformer = pickle.load(open('tfidf_transformer.pkl', 'rb'))
feature_names = pickle.load(open('feature_names.pkl', 'rb'))

# Cleaning data:
stop_words = set(stopwords.words('english'))
new_words = ["fig","figure","image","sample","using",
             "show", "result", "large",
             "also", "one", "two", "three",
             "four", "five", "seven","eight","nine"]
stop_words = list(stop_words.union(new_words))

def preprocessing_text(txt):
    # Lower case
    txt = txt.lower()
    # Remove HTML tags
    txt = re.sub(r"<.*?>", " ", txt)
    # Remove special characters and digits
    txt = re.sub(r"[^a-zA-Z]", " ", txt)
    # tokenization
    txt = nltk.word_tokenize(txt)
    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    txt = [word for word in txt if word not in stop_words]
    # Remove words less than three letters
    txt = [word for word in txt if len(word) >= 3]
    # Lemmatize
    stemming = PorterStemmer()
    txt = [stemming.stem(word) for word in txt]

    return " ".join(txt)

def get_keywords(docs, topN=10):
    # Transform the document to get its word counts
    docs_words_count = tfidf_transformer.transform(cv.transform([docs]))

    # Sorting the sparse matrix
    docs_words_count = docs_words_count.tocoo()
    tuples = zip(docs_words_count.col, docs_words_count.data)
    sorted_items = sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

    # Get top N keywords
    sorted_items = sorted_items[:topN]

    score_vals = []
    features_vals = []
    for idx, score in sorted_items:
        score_vals.append(round(score, 3))  # Append rounded score
        features_vals.append(feature_names[idx])  # Append feature name (word)

    results = {}
    for idx in range(len(features_vals)):
        results[features_vals[idx]] = score_vals[idx]
        
    return results
   
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract_keywords', methods=['POST','Get'])
def extract_keywords():
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error='No document selected')

    if file:
        file = file.read().decode('utf-8', errors='ignore')
        cleaned_file = preprocessing_text(file)
        keywords = get_keywords(cleaned_file,20)
        return render_template('keywords.html',keywords=keywords)
    return render_template('index.html',error='no files selected')

@app.route('/search_keywords', methods=['POST','Get'])
def search_keywords():
    search_query = request.form['search']
    if search_query:
        keywords = []
        for keyword in feature_names:
            if search_query.lower() in keyword.lower():
                keywords.append(keyword)
                if len(keywords) == 20:  # Limit to 20 keywords
                    break
        return render_template('keywordslist.html', keywords=keywords)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)