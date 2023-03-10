from application import db

class Counter(db.Document):
    count = db.IntField(db_field="c")

class Accounts(db.Document):
    name = db.StringField(required=True)
    username = db.StringField(required=True)
    sentiment = db.BooleanField()

# class Replies(db.EmbeddedDocument):
#     author = db.StringField(required=True)
#     text = db.StringField(max_length=120, required=True)
#     sentiment = db.BooleanField()

# class Tweets(db.Document):
#     owner = db.ReferenceField(Accounts)
#     title = db.StringField(max_length=120, required=True)
#     sentiment = db.BooleanField()
#     replies = db.ListField(db.EmbeddedDocumentField(Replies))
      