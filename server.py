from flask import Flask
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw
from hackernews import HackerNews

reddit = praw.Reddit(client_id='KKt5S-SgmLgf4g',
                     client_secret='B8FpLDncJ5fv1FfKhxDBKDyiTD4',
                     user_agent='web:com.caleb.massivewaffle:v1.0.0')

hn = HackerNews()


app = Flask(__name__)

sid = SentimentIntensityAnalyzer()

@app.route('/reddit/<id>')
def score_reddit(submission_id):
    submission = reddit.submission(id=submission_id)
    comments = [c.body for c in submission.comments.list()]
    scores = [score_sentence(comment) for comment in comments]
    return avg(scores)

@app.route('/hn/<id>')
def score_hn(page_id):
    page = hn.get_item(page_id)
    scores = [score_sentence(hn.get_item(x).text) for x in page.kids]
    return avg(scores)

def score_sentence(sentence):
    if sentence is None: 
        return 0
    scores = sid.polarity_scores(sentence)
    return scores['compound']

def avg(scores):
    return sum(scores)/len(scores)

if __name__ == "__main__":
    x = score_hn('13506670')
    print(x)
