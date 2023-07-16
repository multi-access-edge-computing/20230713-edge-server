import joblib
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
import redis
from scipy.sparse import vstack

redis_client = redis.Redis(host='localhost', port=6379)
titles = {}

redis_keys = redis_client.keys()
topics = redis_client.mget(redis_keys)

for idx, item in enumerate(topics):
    titles[redis_keys[idx]] = eval(item.decode('utf-8'))['title']['S']

stop_words = set(stopwords.words('english'))

def remove_stopwords(text):
    tokens = word_tokenize(text)
    tokens = [token for token in tokens if token.lower() not in stop_words]
    return ' '.join(tokens)

def find_similar_sentences(query):
    query = query.lower()
    results = []
    for doc_id, document in titles.items():
        if query in document.lower() or any(word.lower() in document.lower() for word in query.split()):
            results.append({ doc_id.decode('utf-8'): document })
        if len(results) >= 10:
            break
    return results[:10]

def search(query, history):
    history.append(query)
    processed_query = remove_stopwords(query)
    vectorizer = joblib.load('vectorizer.pkl')
    tfidf_matrix_original = joblib.load('tfidf_matrix.pkl')
    tfidf_matrix_history = vectorizer.transform(history)
    tfidf_matrix = vstack((tfidf_matrix_original, tfidf_matrix_history))
    query_vector = vectorizer.transform([processed_query])
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix[:-len(history)])
    results_with_score = list(zip(list(titles.values()), similarity_scores.flatten()))
    results_with_score.sort(key=lambda x: x[1], reverse=True)
    displayed_sentences = find_similar_sentences(query)
    sorted_results = sorted(displayed_sentences, key=lambda x: history[-1] in x, reverse=True)
    displayed_sentences = sorted_results[:10]
    return displayed_sentences

def find_detail(key):
    result = redis_client.get(key)
    return eval(result.decode('utf-8'))
