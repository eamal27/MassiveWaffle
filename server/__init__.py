from nltk.sentiment.vader import SentimentIntensityAnalyzer
from flask import Flask

app = Flask(__name__)

sid = SentimentIntensityAnalyzer()

@app.route('/')
def hello():
    return 'hello world'

def score_sentence(sentence):
    scores = sid.polarity_scores(sentence)
    return scores['compound']

if __name__ == "__main__":
    test_sentence = 'this is fucked'
    score = score_sentence(test_sentence)
    print(score)
