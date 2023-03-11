from application import db

class Counter(db.Document):
    count = db.IntField(db_field="c")


class Audience(db.EmbeddedDocument):
    username = db.StringField(required=True)
    avatar = db.StringField()
    replyCount = db.IntField()
    sentiment = db.BooleanField()

class Reply(db.EmbeddedDocument):
    text = db.StringField(required=True)
    date = db.StringField()
    sentiment = db.BooleanField()
    username = db.StringField(required=True)
    avatar = db.StringField(required=True)

      
class Tweets(db.EmbeddedDocument):
    text = db.StringField(required=True)
    date = db.StringField()
    sentiment = db.BooleanField()
    replies = db.ListField(db.EmbeddedDocumentField(Reply))

class Accounts(db.Document):
    name = db.StringField(required=True)
    username = db.StringField(required=True)
    sentiment = db.BooleanField()
    audience = db.ListField(db.EmbeddedDocumentField(Audience))
    tweets = db.ListField(db.EmbeddedDocumentField(Tweets))