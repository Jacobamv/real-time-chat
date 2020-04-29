from peewee import *

db = SqliteDatabase('db.db')

class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel):
	id = IntegerField(primary_key=True)
	name = CharField()
	password = CharField()


class Messages(BaseModel):
	id = IntegerField(primary_key=True)
	message = TextField()
	From = CharField()
	to = CharField()
	room = CharField()

Users.create_table()
Messages.create_table()