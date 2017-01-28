from flask import Flask
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw

reddit = praw.Reddit(client_id='KKt5S-SgmLgf4g',
                     client_secret='B8FpLDncJ5fv1FfKhxDBKDyiTD4',
                     user_agent='web:com.caleb.massivewaffle:v1.0.0')


app = Flask(__name__)

sid = SentimentIntensityAnalyzer()

@app.route('/reddit/<id>')
def score(submission_id):
    submission = reddit.submission(id=submission_id)
    comments = [c.body for c in submission.comments.list()]
    scores = [score_sentence(comment) for comment in comments]
    avg = sum(scores)/len(scores)
    return avg


def score_sentence(sentence):
    scores = sid.polarity_scores(sentence)
    return scores['compound']

if __name__ == "__main__":
    x = score('5qmtpo')
    print(x)
