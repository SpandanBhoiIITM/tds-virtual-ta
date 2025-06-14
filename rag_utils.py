import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open("data/discourse_posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

corpus = [p["content"] for p in posts]

def get_top_k_relevant_context(query: str, k: int = 3) -> str:
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus + [query])
    
    query_vec = tfidf_matrix[-1]
    corpus_vecs = tfidf_matrix[:-1]

    similarities = cosine_similarity(query_vec, corpus_vecs).flatten()
    top_indices = similarities.argsort()[-k:][::-1]

    return "\n".join([corpus[i] for i in top_indices])
