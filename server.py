from flask import Flask, jsonify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw
from hackernews import HackerNews

reddit = praw.Reddit(client_id='KKt5S-SgmLgf4g',
                     client_secret='B8FpLDncJ5fv1FfKhxDBKDyiTD4',
                     user_agent='web:com.caleb.massivewaffle:v1.0.0')

hn = HackerNews()


app = Flask(__name__)

sid = SentimentIntensityAnalyzer()


@app.route('/reddit/<submission_id>')
def score_reddit(submission_id):
    submission = reddit.submission(id=submission_id)
    submission.comments.replace_more(limit=16, threshold=10)
    comments = [c.body for c in submission.comments.list()]
    scores = [score_sentence(comment) for comment in comments]
    return jsonify(id=submission_id, score=avg(scores))


@app.route('/hn/<page_id>')
def score_hn(page_id):
    page = hn.get_item(page_id)
    comment_ids = []
    score = 0
    if page.kids is not None:
        comments = get_hn_comments(page.kids)
        scores = [score_sentence(x) for x in comments]
        score = avg(scores)
    return jsonify(id=page_id, score=avg(scores))

def get_hn_comments(kid_ids):
    kids = [hn.get_item(x) for x in kid_ids]
    comments = []
    for kid in kids:
        comments.append(kid.text)
        if kid.kids is not None:
            comments.extend(get_hn_comments(kid.kids))
    return comments


def score_sentence(sentence):
    if sentence is None: 
        return 0
    scores = sid.polarity_scores(sentence)
    return scores['compound']


def avg(scores):
    return sum(scores)/len(scores)


if __name__ == "__main__":
    x = score_hn('13508038')
    print(x)
