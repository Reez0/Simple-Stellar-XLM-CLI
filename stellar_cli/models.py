from peewee import *

db = SqliteDatabase('accounts.db')

class Account(Model):
    public = CharField()
    secret = CharField()
    type = CharField()
    
    class Meta:
        database = db