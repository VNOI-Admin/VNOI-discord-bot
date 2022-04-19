from peewee import *
import peewee

db = SqliteDatabase('database.db')


class Question(Model):
    thread_id = IntegerField()
    judge = CharField()
    problem_name = CharField()
    problem_link = CharField()

    class Meta:
        database = db


db.connect()
db.create_tables([Question])


def insert(*, thread_id, judge, name, link):
    Question.create(thread_id=thread_id, judge=judge,
                    problem_name=name, problem_link=link)


def select(*, thread_id=None, name=None, link=None):
    exp = True

    if thread_id:
        exp = exp & (Question.thread_id == thread_id)
    if name:
        exp = exp & (Question.problem_name == name)
    if link:
        exp = exp & (Question.problem_link == link)

    return Question.select().where(exp)
