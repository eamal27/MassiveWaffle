from flask import Flask, jsonify, request
from flask_cache import Cache
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw
from bs4 import BeautifulSoup
from urllib.request import urlopen

reddit = praw.Reddit(client_id='KKt5S-SgmLgf4g',
                     client_secret='B8FpLDncJ5fv1FfKhxDBKDyiTD4',
                     user_agent='web:com.caleb.massivewaffle:v1.0.0')


app = Flask(__name__)

app.config['DEBUG'] = True

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

sid = SentimentIntensityAnalyzer()

CACHE_TIMEOUT = 300  # Seconds


@app.route('/reddit/<submission_id>')
@cache.cached(timeout=CACHE_TIMEOUT)
def score_reddit(submission_id):
    submission = reddit.submission(id=submission_id)
    submission.comments.replace_more(limit=16, threshold=10)
    comments = [c.body for c in submission.comments.list()]
    scores = [score_sentence(comment) for comment in comments]
    return jsonify(id=submission_id, score=avg(scores))


@app.route('/score_comment', methods=['POST'])
@cache.cached(timeout=3600)
def score_comment():
    comment = request.form.get('comment', '')
    score = score_sentence(comment)
    return jsonify(score=score)


@app.route('/hn/<page_id>')
@cache.cached(timeout=CACHE_TIMEOUT)
def score_hn(page_id):
    url = 'https://news.ycombinator.com/item?id=' + page_id
    page = urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')
    comment_divs = soup.findAll("div", {"class": "comment"})
    scores = [score_sentence(div.text) for div in comment_divs]
    return jsonify(id=page_id, score=avg(scores))


def score_sentence(sentence):
    if sentence is None: 
        return 0
    scores = sid.polarity_scores(sentence)
    return scores['compound']


def avg(scores):
    try:
        return sum(scores)/len(scores)
    except ZeroDivisionError:
        return 0


if __name__ == "__main__":
    x = score_hn('13506670')
    print(x)
