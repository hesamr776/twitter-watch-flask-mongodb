import json
from flask import Blueprint, jsonify
from flask_cors import CORS

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