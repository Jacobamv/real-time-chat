from peewee import *

db = SqliteDatabase('db.db')

class BaseModel(Model):
    class Meta:
        database = db


class Messages(BaseModel):
	id = IntegerField(primary_key=True)
	message = TextField()
	From = CharField()

Messages.create_table()