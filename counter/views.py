import json
from flask import Blueprint, jsonify
from flask_cors import CORS

from scripts.snscraper import update_tweets

from counter.models import Counter, Accounts, Audience, Tweets, Reply

counter_app = Blueprint("counter_app", __name__)
cors = CORS(counter_app)

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
    return "<h1>Views: " + str(counter.count) + "</h1>"


@counter_app.route("/accounts")
def accounts():
    accounts = Accounts.objects.all()
    if  len(accounts) > 0:
        return jsonify(accounts)
    
    Accounts(name='Elon Musk', username='elonmusk').save()
    Accounts(name='Barack Obama', username='barackobama').save()
    Accounts(name='Yann Lecun', username='ylecun').save()
    return jsonify(Accounts.objects.all())



@counter_app.route('/audience/<username>')
def audience(username):
    account = Accounts.objects(username=username).first()

    return jsonParse(account.audience)


@counter_app.route('/sentiment/<username>')
def sentiment(username):
    account = Accounts.objects(username=username).first()

    positive_tweets = len([x for x in account.tweets if x.sentiment == 1]) or 0
    negative_tweets = len(account.tweets) - positive_tweets

    positive_replies = 0
    negative_replies = 0
    for tweet in account.tweets:
        for reply in tweet['replies']:
            if reply['sentiment'] == 1:
                positive_replies += 1
            else:
                negative_replies += 1

    return jsonParse(
        {"positive_tweets": positive_tweets, "negative_tweets": negative_tweets, "positive_replies": positive_replies,
         "negative_replies": negative_replies})


@counter_app.route('/tweets/<username>')
def tweets(username):
    account = Accounts.objects(username=username).first()

    return jsonParse(account.tweets)


@counter_app.route('/replies/<tweetId>')
def replies(tweetId):
    account = Accounts.objects(tweets__tweetId=tweetId).first()
    tweet = [x for x in account.tweets if x.tweetId == tweetId][0] or {replies: []}

    return jsonParse(tweet.replies)


@counter_app.route('/update/<username>')
def update(username):
    account = Accounts.objects(username=username).first()

    try:
        since = account["tweets"][0].date if len(account["tweets"]) else None
        since = since[0:10]
    except:
        since = '2023-02-01'
    print(since)

    update_account_tweets = update_tweets(username, since)
   
    update_account = get_update_account(update_account_tweets['tweets'], update_account_tweets['replies'])
    update_account["tweets"] += account.tweets
    update_account["audiences"] += account.audience  # todo : must be unique

    account.update(set__tweets=update_account["tweets"], set__audience=update_account["audiences"])
    account.reload()

    return jsonParse(account)


@counter_app.route("/data/<username>")
def data(username):
    original_tweets = open(f'./data/{username}.json')
    original_data = json.load(original_tweets)

    reply_tweets = open(f'./data/replyTo-{username}.json')
    reply_data = json.load(reply_tweets)

    update_account = get_update_account(original_data, reply_data)

    account = Accounts.objects(username=username).first()
    account.tweets = update_account["tweets"]
    account.audience = update_account["audiences"]
    account.save()

    original_tweets.close()
    reply_tweets.close()

    return jsonParse(account)


def get_update_account(original_data, reply_data):
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
            tweet_replies.append(
                Reply(username=reply['username'], avatar='/barackobama.jpg', text=reply['text'], date=reply['date'],
                      sentiment=reply['sentiment']))

        tweets.append(
            Tweets(tweetId=str(tweet['id']), text=tweet['text'], date=tweet['date'], sentiment=tweet['sentiment'],
                   replies=tweet_replies))

    return {"tweets": tweets, "audiences": accountAudiences}


def jsonParse(query_set):
    return jsonify(query_set)