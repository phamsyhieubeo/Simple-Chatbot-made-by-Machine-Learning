import nltk
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.stem import PorterStemmer

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import json

with open("Data/Data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

texts = data["prompts"]
labels = data["labels"]
responses = data["responses"]

try:
    nltk.data.find("corpora/stopwords")

except:
    nltk.download("stopwords", quiet= True)


stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()

def preprocessor(text: str):
    text = text.lower()
    token = wordpunct_tokenize(text)

    cleaned_token = []

    for word in token:
        if word.isalpha() and word not in stop_words:
            word = stemmer.stem(word)
            cleaned_token.append(word)

    return " ".join(cleaned_token)

model = Pipeline([
    ("tfidf", TfidfVectorizer(preprocessor= preprocessor,  ngram_range= (1, 2))),
    ("lr", LogisticRegression())
])

model.fit(texts, labels)
y_predict = model.predict(texts)

acc = accuracy_score(labels, y_predict) * 100
print(f"Accuracy Score: {acc:2f}%")

joblib.dump(model, "Model\\KaylaGPT.pkl")
