from flask import Blueprint

from counter.models import Counter, Accounts 

counter_app = Blueprint("counter_app", __name__)


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
    if  len(accounts) > 0:
        return accounts
    
    Accounts(name='Elon Musk', username='elonmusk').save()
    Accounts(name='Barack Obama', username='barackobama').save()
    Accounts(name='Yann Lecun', username='yannlecun').save()
    return Accounts.objects.all()



@counter_app.route('/audience/<username>')
def audience(username):
    return [
        { "id": "elonmusk", "avatar": "/elonmusk.jpg" },
        { "id": "barackobama", "avatar": "/barackobama.jpg" },
        { "id": "yannlecun", "avatar": "/yannlecun.jpg" }
    ]


@counter_app.route('/sentiment')
def sentiment():
    return 'sentiment'


@counter_app.route('/tweets/<username>')
def tweets(username):
    return [
        {
            "username": username,
            "id": "1234567",
            "avatar": "/elonmusk.jpg",
            "date": "10h",
            "text": 'just human rights',
            "sentiment": 1
        },
        {
            "username": username,
            "id": "8765432",
            "avatar": "/elonmusk.jpg",
            "date": "1d",
            "text": 'you are bad',
            "sentiment": 0
        },
        {
            "username": username,
            "id": "12345678",
            "avatar": "/elonmusk.jpg",
            "date": "2d",
            "text": 'normal tweet message',
            "sentiment": 1
        }
    ]
   
