import json
from flask import Blueprint, jsonify
from flask_cors import CORS

from counter.models import Counter, Accounts, Audience, Tweets, Reply

counter_app = Blueprint("counter_app", __name__)
cors = CORS(counter_app)

@counter_app.route("/data/<username>")
def data(username):
    original_tweets = open(f'./data/{username}.json')
    original_data = json.load(original_tweets)

    reply_tweets = open(f'./data/replyTo-{username}.json')
    reply_data = json.load(reply_tweets)

    map_to_original = {}
    usernames = []
    for reply in reply_data['replies']:
        map_to_original[reply['tweetId']] = reply['replies']

        for aud in reply['replies']:
            usernames.append(aud['username'])

    usernamesSet = set(usernames)
    audienceReplyCount = {}

    for uname in usernamesSet:
        repliesCount = usernames.count(uname)
        audienceReplyCount[uname] = repliesCount

    audiences = sorted(audienceReplyCount.items(), key=lambda item: item[1], reverse=True)
    filteredAudiences = audiences[:20]
    accountAudiences = []
    for aud in filteredAudiences:
        accountAudiences.append(Audience(username=aud[0], avatar='', replyCount=aud[1]))

    replies = []
    tweets = []
    for tweet in original_data['tweets']:
        tweet_replies = [] 
        for reply in map_to_original[tweet['id']]:
            tweet_replies.append(Reply(username=reply['username'], avatar='/barackobama.jpg', text=reply['text'], date=reply['date'], sentiment=reply['sentiment']))

        tweets.append(Tweets(text=tweet['text'], date=tweet['date'], sentiment=tweet['sentiment'], replies=tweet_replies))

    account = Accounts.objects(username=username).first()
    account.tweets = tweets
    account.audience = accountAudiences
    account.save()
    
    original_tweets.close()
    reply_tweets.close()

    return jsonParse(account)


@counter_app.route("/")
def init():
    counter = Counter.objects.all().first()
    if counter:
        counter.count += 1
        counter.save()
    else:
        counter = Counter()
        counter.count = 1
        counter.save()
    return "<h1>Counter: " + str(counter.count) + "</h1>"

@counter_app.route("/accounts")
def accounts():
    accounts = Accounts.objects.all()

    return jsonParse(accounts)    
    
@counter_app.route("/update")
def update():
    Accounts.objects(username="yannlecun").update(set__username='ylecun')
    return jsonParse(Accounts.objects.all())

@counter_app.route('/audience/<username>')
def audience(username):
    account = Accounts.objects(username=username).first()
    
    return jsonParse(account.audience)

@counter_app.route('/sentiment')
def sentiment():
    return 'sentiment'

@counter_app.route('/tweets/<username>')
def tweets(username):
    account = Accounts.objects(username=username).first()

    return jsonParse(account.tweets)
  
def jsonParse(query_set):
    return jsonify(query_set)